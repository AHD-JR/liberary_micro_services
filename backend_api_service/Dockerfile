# Dockerfile for backend_api_service

# Use Python base image
FROM python:3.11.7-alpine

# Set working directory
WORKDIR /app

# Copy all files from the local directory to the container
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
