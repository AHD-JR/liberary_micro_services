# Dockerfile for frontend_api_service

# Use Python base image
FROM python:3.11.7-alpine

# Set working directory
WORKDIR /app

# Copy all files from the local directory to the container
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8001
EXPOSE 8001

# Command to run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
