# Multi-stage build for frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

# Backend stage
FROM python:3.11-slim AS backend
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# Final stage - combine both
FROM nginx:alpine
WORKDIR /usr/share/nginx/html

# Copy frontend build
COPY --from=frontend-build /app/frontend/build ./

# Copy backend and set up nginx to serve both
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir fastapi uvicorn && \
    mkdir -p /app/backend && \
    cp -r /app/backend/* /app/backend/

# Create nginx config to serve frontend and proxy backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
