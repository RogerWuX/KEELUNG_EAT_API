from .models import *
import json

from flask import request,jsonify,g,session

from . import app,socketio
from datetime import datetime
from.auth import auth

@app.route('/',methods=['get'])
def test():
	return jsonify({'message':'hello_world'})
	


@app.route('/order',methods=['post'])
@auth.login_required
def order_post():
	print('order_post')
	print(request.json.get('foods'))
	if g.user.identity!=0 :
		return jsonify({'message':'failed'})
	order=Order(
		receive_time=datetime.strptime(request.json.get('receive_time'),"%Y-%m-%d %H:%M:%S"),#,
		delivery_time=None,
		district=request.json.get('district'),
		address=request.json.get('address'),
		consumer_id=request.json.get('consumer_id'),
		delivery_id=None,
		store_id=request.json.get('store_id'),
		foods=request.json.get('foods'),
		total_price=request.json.get('total_price'),
		delivery_state='pending',
		store_state='unconfirmed'
	)
	order.save()
	order=dict(order.to_mongo())
	Order.dict_to_string(order)
	order_json=json.dumps(order)
	socketio.emit('order_data',order_json,namespace='/admin',broadcast=True)
	socketio.emit('order_data',order_json,namespace='/restaurant',room=order['store_id'],broadcast=True)
	return jsonify({'_id':order['_id']})

'''
@app.route('/delivery/<delivery_id>/current_orders',methods=['get'])
def current_order_delivery(delivery_id):
	print('delivery current_order')
	try:
		current_order=Order.objects(delivery_id=delivery_id,delivery_state__in=['accepted','delivering']).exclude('delivery_id').as_pymongo().get()
		Order.dict_to_string(current_order)
		return jsonify(json.dumps(current_order))
	except :
		return jsonify({"message":'failed'})
'''
	

@app.route('/consumer/<consumer_id>/current_orders',methods=['get'])
def current_order_consumer(consumer_id):
	print('consumer current_order')
	#try:
	current_order_dicts=list(Order.objects(consumer_id=consumer_id,delivery_state__ne='finished').exclude('consumer_id').as_pymongo())
	for order_dict in current_order_dicts:
		Order.dict_to_string(order_dict)
	return jsonify(json.dumps(current_order_dicts))
	#except:
	#	return jsonify({"message":'failed'})
	