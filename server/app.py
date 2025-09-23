from flask import Flask
from flask import render_template
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def hello_world():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    socketio.send("A new user joined!")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    socketio.send("A user has left the chat")


@socketio.on('message')
def handle_message(message):
    socketio.send(message)
    print(f"Message received: {message}")


if __name__ == "__main__":
    socketio.run(app)
