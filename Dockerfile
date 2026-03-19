FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=api/app.py
ENV PYTHONUNBUFFERED=1

# Start the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api.app:app"]
