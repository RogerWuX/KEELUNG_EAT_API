from KeelungEat.models import Order

import json
from flask import request,jsonify

from . import app,socketio

@app.route('/order',methods=['post'])
def order_post():
	print('order_post')
	order=Order(
		recieve_time=request.json.get('recieve_time'),
		delivery_time=request.json.get('delivery_time'),
		district=request.json.get('district'),
		address=request.json.get('address'),
		consumer_id=request.json.get('consumer_id'),
		delivery_id=request.json.get('delivery_id'),		
		store_id=request.json.get('store_id'),
		foods=request.json.get('foods'),
		delivery_state='pending',
		store_state='unconfirmed'
	)
	order.save()
	socketio.emit('order_data',order.to_json(),namespace='/admin',broadcast=True)
	socketio.emit('order_data',order.to_json(),namespace='/delivery_man',broadcast=True)
	
	return jsonify({'id':str(order.id)})


@app.route('/delivery/<delivery_id>/current_orders',methods=['get'])
def current_order_delivery(delivery_id):
	print('delivery current_order')
	try:
		current_order=Order.objects(delivery_id=delivery_id,delivery_state__in=['accepted','delivering']).exclude('delivery_id').as_pymongo().get()
		for field in ['recieve_time','delivery_time','consumer_id','store_id']:
			current_order[field]=str(current_order[field])
		return jsonify(json.dumps(current_order))
	except :
		return jsonify({"message":'failed'})
	
	

@app.route('/consumer/<consumer_id>/current_orders',methods=['get'])
def current_order_consumer(consumer_id):
	print('consumer current_order')
	try:
		current_order=Order.objects(consumer_id=consumer_id,delivery_state__ne='finished').exclude('consumer_id').as_pymongo().get()
		for field in ['recieve_time','delivery_time','store_id','delivery_id']:
				current_order[field]=str(current_order[field])
		return jsonify(json.dumps(current_order))
	except:
		return jsonify({"message":'failed'})
	