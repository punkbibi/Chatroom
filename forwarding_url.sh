#!/bin/bash

# Start Flask app in background and save PID
echo "Starting Flask app..."
flask --app server/app run --host=0.0.0.0 --port=5000 &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"

# Give Flask a moment to start
sleep 2

# Start ngrok in background and save PID
echo "Starting ngrok..."
ngrok http 5000 > /dev/null &
NGROK_PID=$!
echo "ngrok PID: $NGROK_PID"

# Give ngrok a moment to initialize
sleep 2

# Get ngrok public URL
NGROK_URL=$(curl --silent http://127.0.0.1:4040/api/tunnels | \
  grep -oP '"public_url":"\Khttps?://[^\"]+')

echo "Public URL: $NGROK_URL"

# Function to cleanup processes on exit
cleanup() {
    echo "Stopping Flask ($FLASK_PID) and ngrok ($NGROK_PID)..."
    kill $FLASK_PID
    kill $NGROK_PID
    exit
}

# Trap CTRL+C (SIGINT) and EXIT to cleanup
trap cleanup SIGINT SIGTERM EXIT

# Keep script alive so background processes stay running
echo "Press Ctrl+C to stop..."
wait
