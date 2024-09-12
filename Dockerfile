FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Command to run the application
CMD ["python", "api.py"]
