#!/bin/bash
# Railway startup script for CSV Processor

# Get the port from Railway environment variable
PORT=${PORT:-8000}

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port $PORT