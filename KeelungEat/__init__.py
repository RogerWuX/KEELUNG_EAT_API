import eventlet
#eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app=Flask(__name__, static_folder='image', static_url_path='/image');
CORS(app)
UPLOAD_FOLDER = 'image/'
STATIC_FOLDER = 'http://localhost:5000/image/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

socketio=SocketIO(app,cors_allowed_origins='*')

import KeelungEat.http_route
import KeelungEat.ws_route
import KeelungEat.background_task