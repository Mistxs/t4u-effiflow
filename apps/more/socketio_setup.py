from flask_socketio import SocketIO

socketio = SocketIO(transports='websocket', ping_interval=60, ping_timeout=20)
