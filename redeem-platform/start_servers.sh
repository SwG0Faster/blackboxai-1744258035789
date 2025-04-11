#!/bin/bash

# Kill any existing processes on ports 8000 and 8001
lsof -ti:8000,8001 | xargs kill -9 2>/dev/null || true

# Start Django backend server
cd redeem-platform/backend
python3 manage.py runserver 8001 &

# Wait for Django to start
sleep 2

# Start frontend server
cd ../..
python3 redeem-platform/server.py
