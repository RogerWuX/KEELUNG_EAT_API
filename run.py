import config
from KeelungEat import app,socketio



if __name__=='__main__':
	app.config.from_object(config.config)
	socketio.run(app,host='0.0.0.0');
	
	
	