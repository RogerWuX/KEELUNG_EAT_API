from KeelungEat.models import Order

from flask import request

from . import app,socketio

@app.route('/order',methods=['post'])
def order_post():
	print('order_post')
	#message_queue.put({'order_name':request.args.get('order_name')})	
	order=Order(address=request.args.get('address'))
	order.save()
	socketio.emit('order_data',order.to_json(),namespace='admin',broadcast=True)
	return {'id':str(order.id)}

@app.route('/order',methods=['get'])
def get_all_post():
	print('all_order')	
	return {'orders':''};

	