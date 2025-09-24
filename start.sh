#!/bin/bash

echo "Setting up the full-stack application..."

# Check if .env file exists in backend
if [ ! -f "./backend/.env" ]; then
    echo "⚠️  Please create a .env file in the backend directory with your GEMINI_API_KEY"
    echo "You can copy .env.example and update it with your API key"
    exit 1
fi

# Start backend server in the background
echo "🐍 Starting Python Flask backend..."
cd backend && python3 simple_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend development server
echo "⚛️  Starting React frontend..."
cd ..
npm run dev &
FRONTEND_PID=$!

echo "🚀 Application started!"
echo "Frontend: http://localhost:5174 (or whatever port Vite assigns)"
echo "Backend: http://localhost:7777"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup background processes
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap to cleanup when script is interrupted
trap cleanup INT TERM

# Wait for both processes
wait