# Simple single container with both frontend and backend
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y nginx

# Install Python dependencies
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Create nginx directory and copy frontend files
RUN mkdir -p /var/www/html
COPY frontend/ /var/www/html/

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start both services
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
