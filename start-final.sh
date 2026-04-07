#!/bin/bash

# Start nginx in background
nginx -g "daemon off;" &

# Wait for nginx to start
sleep 3

# Start FastAPI on Unix socket (no network port)
uvicorn main:app --host unix:/tmp/app.sock --fd 0
