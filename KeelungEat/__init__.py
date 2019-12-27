import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app=Flask(__name__);
CORS(app)
UPLOAD_FOLDER = 'C:/Users/cat/Desktop/KEELUNG_EAT_API/image/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio=SocketIO(app,cors_allowed_origins='*')

import KeelungEat.http_route
import KeelungEat.ws_route
import KeelungEat.background_task