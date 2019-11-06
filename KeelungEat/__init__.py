from flask import Flask
from flask_socketio import SocketIO

app=Flask(__name__);
socketio=SocketIO(app,cors_allowed_origins='*')

import KeelungEat.http_route
import KeelungEat.ws_route
