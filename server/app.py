from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import emit
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


chat_history = []  # In-memory storage for chat history
active_users = set()  # In-memory storage for active users
sid_to_user = {}  # Mapping of session IDs to user names


@app.route("/")
def hello_world():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("active_users", list(active_users), to=request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    user = sid_to_user.get(request.sid, "Unknown")  # get before removing
    emit("user_disconnected", {"user": user}, broadcast=True)

    sid_to_user.pop(request.sid, None)
    if user in active_users:
        active_users.discard(user)

    emit("active_users", list(active_users), broadcast=True)


@socketio.on('message')
def handle_message(data):
    user = data.get("user", "Anon")
    text = data.get("text", "").strip()  # remove leading/trailing spaces
    if not text:
        return
    if len(text) > 500:
        emit("message", {"user": "Server", "text": "⚠️ Message too long!"}, to=request.sid)
        return

    emit("message", {"user": user, "text": text}, broadcast=True)
    chat_history.append({"user": user, "text": text})
    print(f"Message received: {text}")


@socketio.on('join')
def on_join(data):
    user = data.get("user", "Anon")

    if user not in active_users:
        active_users.add(user)

    sid_to_user[request.sid] = user

    emit("history", chat_history, to=request.sid)
    emit("user_connected", {"user": user}, broadcast=True)
    emit("active_users", list(active_users), broadcast=True)


@socketio.on('leave')
def on_leave(data):
    user = data.get("user", sid_to_user.get(request.sid, "Unknown"))
    emit("user_disconnected", {"user": user}, broadcast=True)
    active_users.discard(user)
    sid_to_user.pop(request.sid, None)
    emit("active_users", list(active_users), broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
