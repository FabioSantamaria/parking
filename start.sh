#!/bin/bash

# Start nginx in the background
nginx -g "daemon off;" &

# Wait a moment for nginx to start
sleep 2

# Start FastAPI backend
uvicorn main:app --host 0.0.0.0 --port 8000
