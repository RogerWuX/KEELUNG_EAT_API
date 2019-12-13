from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
socketio=SocketIO(app,cors_allowed_origins='*')

import KeelungEat.http_route
import KeelungEat.ws_route
