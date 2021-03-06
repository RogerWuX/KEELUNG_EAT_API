import eventlet
eventlet.monkey_patch(socket=False)
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app=Flask(__name__, static_folder='image', static_url_path='/image');
CORS(app, supports_credentials=True)
UPLOAD_FOLDER = 'image/'
STATIC_FOLDER = 'https://keelung-eat.herokuapp.com/image/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

socketio=SocketIO(app,cors_allowed_origins='*')

import KeelungEat.http_route
import KeelungEat.ws_route
import KeelungEat.background_task