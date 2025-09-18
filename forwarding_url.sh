#!/bin/bash

echo "Starting Flask app..."
flask --app server/app run --host=0.0.0.0 --port=5000 &
FLASK_PID=$!

sleep 2

echo "Starting ngrok in the background..."
ngrok http 5000 > /dev/null &
NGROK_PID=$!

# Wait a little for ngrok to initialize
sleep 2

# Get ngrok public URL
NGROK_URL=$(curl --silent http://127.0.0.1:4040/api/tunnels | \
  grep -oP '"public_url":"\Khttps?://[^\"]+')

# Print only the URL
echo $NGROK_URL
echo $NGROK_PID
echo $FLASK_PID
