# import json

from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import emit
from flask_socketio import send
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


chat_history = []  # In-memory storage for chat history
active_users = set()  # In-memory storage for active users


#! add function to load and update chat history from a file or database
#! from json, it should load the chat history when the server starts
#! and update the file or database when a new message is received
def load_and_update_chat_history():
    pass


@app.route("/")
def hello_world():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    send("A user has left the chat", broadcast=True)


@socketio.on('message')
def handle_message(data):
    user = data.get("user", "Anon")
    text = data.get("text", "")
    send(f"{user}: {text}", broadcast=True)
    chat_history.append(f"{user}: {text}")
    print(f"Message received: {text}")


@socketio.on('join')
def on_join(data):
    user = data.get("user", "Anon")
    active_users.add(user)
    emit("history", chat_history, to=request.sid)
    send(f"🔔 {user} has entered the room.", broadcast=True)


@socketio.on('leave')
def on_leave(data):
    user = data.get("user", "Anon")
    active_users.discard(user)
    send(f"🔔 {user} has left the room.", broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
