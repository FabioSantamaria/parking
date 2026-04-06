# Use Node.js to build frontend
FROM node:18-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Use nginx to serve static files
FROM nginx:alpine
WORKDIR /usr/share/nginx/html

# Copy built frontend
COPY --from=builder /app/build ./

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
