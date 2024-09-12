## **REST API Project**

## **Description**
This project is a Python-based REST API that provides domain lookup, IP validation, query history, and health/status endpoints. The application includes Kubernetes support via Helm charts and uses Docker/Docker Compose for local development. It also includes a CI/CD pipeline to test, build, and package the application.

## **Features:**
- `/metrics`: Prometheus metrics endpoint for monitoring
- `/health`: Provides a health check
- `/`: Root endpoint with version, date, and Kubernetes detection
- `/v1/tools/lookup`: Resolves IPv4 addresses for the given domain
- `/v1/tools/validate`: Validates if the input is an IPv4 address
- `/v1/history`: Retrieves the latest 20 doma lookup queries

## **Tech Stack:**
- Backend: Python (Flask)
- Database: PostgreSQL
- Orchestration: Docker, Kubernetes (Helm)
- CI/CD: GitHub Actions
- Monitoring: Prometheus

### Prerequisites
- Docker
- Docker Compose
- Kubernetes for deployment
- Helm
- GitHub repository setup for CI/CD with secrets configured
- PostgreSQL

## **Setup Instructions**

### **1. Local Development (Docker Compose)**

To start the project in a local development environment using Docker and Docker Compose:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/interview-challenge.git
    cd interview-challenge
    ```

2. Build and run the application:

    ```bash
    docker-compose up -d --build
    ```

3. The app will be accessible at `http://localhost:3000`.

4. You can view logs using:

    ```bash
    docker-compose logs -f
    ```

5. To stop the containers:

    ```bash
    docker-compose down
    ```

### **2. Database Configuration**

The PostgreSQL database is set up in the `docker-compose.yml`. By default:
- Database: `queriesdb`
- Username: `postgres`
- Password: `postgres`


## **API Endpoints**

### **Root (`/`)**
- **Description**: Returns the current version, date (UNIX epoch), and Kubernetes status.
- **Method**: GET
- **Example Response**:
    ```json
    {
      "version": "0.1.0",
      "date": 1663534325,
      "kubernetes": false
    }
    ```

### **Health (`/health`)**
- **Description**: Provides a health check for the API.
- **Method**: GET
- **Example Response**:
    ```json
    {
      "status": "healthy"
    }
    ```

### **Metrics (`/metrics`)**
- **Description**: Prometheus metrics for monitoring.
- **Method**: GET

### **Domain Lookup (`/v1/tools/lookup`)**
- **Description**: Resolves IPv4 addresses for a given domain and logs the query in the database.
- **Method**: GET
- **Query Params**: `domain` (required)

### **IP Validation (`/v1/tools/validate`)**
- **Description**: Validates if the provided IP address is a valid IPv4 address.
- **Method**: POST
- **Request Body**:
    ```json
    {
      "ip": "192.168.1.1"
    }
    ```

### **Query History (`/v1/history`)**
- **Description**: Returns the latest 20 domain lookup queries.
- **Method**: GET


## **Deployment to Kubernetes (Helm)**

### **1. Pre-requisites**
- Ensure you have access to a Kubernetes cluster.
- Helm must be installed on your local machine.

### **2. Helm Deployment**

1. Build and push the Docker image:

    ```bash
    docker build -t your_dockerhub_username/leyline-app:latest .
    docker push your_dockerhub_username/leyline-app:latest
    ```

2. Deploy the application using Helm:

    ```bash
    helm install leyline-app ./helm/leyline-app
    ```

3. To upgrade the deployment after making changes:

    ```bash
    helm upgrade leyline-app ./helm/leyline-app
    ```

4. You can view the app logs using:

    ```bash
    kubectl logs -l app=leyline-app
    ```

5. To delete the application:

    ```bash
    helm delete leyline-app
    ```

### **Storing Sensitive Data**
Database credentials and other sensitive data are stored in Kubernetes secrets. You can define these secrets in the `helm/leyline-app/templates/secret.yaml` file. The password is base64-encoded.


## **CI Pipeline (GitHub Actions)**

This project includes a GitHub Actions CI pipeline to automate the process of testing, building, and pushing Docker images on every commit.

### **Pipeline Overview**
- **Test**: Runs unit tests and linters.
- **Build**: Builds the Docker image.
- **Push**: Pushes the Docker image to Docker Hub with the latest commit hash.

### **Pipeline Setup**
1. Set up your repository with the following GitHub secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username.
   - `DOCKER_PASSWORD`: Your Docker Hub password.

2. The pipeline will run automatically on each commit to the `main` branch.


## **Testing**

1. To run the unit tests locally (before committing to the repository):

    ```bash
    python -m unittest discover tests/
    ```

2. To view logs for Dockerized containers:

    ```bash
    docker-compose logs -f
    ```
