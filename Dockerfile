# Use Python 3.13 slim image
FROM python:3.13-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set Python path to include the project root
ENV PYTHONPATH=/app

# Expose port 8000 for the Flask server
EXPOSE 8000

# Default command (can be overridden)
CMD ["python", "app.py"]