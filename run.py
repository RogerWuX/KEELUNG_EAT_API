import config
from KeelungEat import app,socketio
from os import environ


if __name__=='__main__':
	app.config.from_object(config.config)
	socketio.run(app,host='0.0.0.0',port=environ.get('PORT'), cors_allowed_origins='http://localhost:8080');
# 
#, keyfile='key.pem', certfile='cert.pem'

	