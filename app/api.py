from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
import socket
import time
import os
from prometheus_client import generate_latest, Counter
from datetime import datetime
from flask_cors import CORS


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database config (assuming PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/queriesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('query_logger')

# Database model for storing queries
class QueryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Prometheus metric counter for queries
QUERY_COUNTER = Counter('queries_total', 'Total queries made to /v1/tools/lookup')

# Root endpoint providing version, UNIX epoch, and Kubernetes status
@app.route('/', methods=['GET'])
def query_status():
    is_kubernetes = 'KUBERNETES_SERVICE_HOST' in os.environ
    response = {
        "version": "0.1.0",
        "date": int(time.time()),  # UNIX epoch
        "kubernetes": is_kubernetes
    }
    return jsonify(response), 200

# Health check endpoint
@app.route('/health', methods=['GET'])
def query_health():
    return jsonify({"status": "healthy"}), 200

# /v1/tools/lookup endpoint to resolve IPv4 addresses
@app.route('/v1/tools/lookup', methods=['GET'])
def lookup_domain():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"message": "Domain parameter is required"}), 400
    try:
        ipv4_addresses = [ip for ip in socket.gethostbyname_ex(domain)[2] if '.' in ip]
        if ipv4_addresses:
            # Log query to database
            for ip in ipv4_addresses:
                log = QueryLog(domain=domain, ip=ip)
                db.session.add(log)
            db.session.commit()
            # Increment Prometheus counter
            QUERY_COUNTER.inc()
            response = {
                "addresses": [{"ip": ip, "queryID": log.id} for ip in ipv4_addresses],
                "client_ip": request.remote_addr,
                "created_time": int(time.time()),
                "domain": domain
            }
            return jsonify(response), 200
        else:
            return jsonify({"message": "No IPv4 address found for the domain"}), 404
    except socket.gaierror:
        return jsonify({"message": "Domain resolution failed"}), 500

# /v1/tools/validate endpoint to check if input is a valid IPv4 address
@app.route('/v1/tools/validate', methods=['POST'])
def validate_ip():
    data = request.json
    ip = data.get('ip')
    if not ip:
        return jsonify({"message": "IP parameter is required"}), 400

    try:
        socket.inet_pton(socket.AF_INET, ip)
        return jsonify({"status": True}), 200
    except socket.error:
        return jsonify({"status": False}), 400

# /v1/history endpoint to retrieve the latest 20 queries
@app.route('/v1/history', methods=['GET'])
def queries_history():
    latest_queries = QueryLog.query.order_by(QueryLog.timestamp.desc()).limit(20).all()
    results = [{
        "addresses": [{"ip": query.ip, "queryID": query.id}],
        "client_ip": request.remote_addr,
        "created_time": int(query.timestamp.timestamp()),
        "domain": query.domain
    } for query in latest_queries]
    return jsonify(results), 200

# Prometheus metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200

# Graceful shutdown
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server = request.environ.get('werkzeug.server.shutdown')
    if shutdown_server is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_server()
    return 'Server shutting down...'

# Main entry
if __name__ == '__main__':
    db.create_all()  # Ensure tables are created
    app.run(host='0.0.0.0', port=3000)  # Start the server on port 3000
