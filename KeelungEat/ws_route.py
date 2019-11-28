
from KeelungEat.models import Order

from flask import request
import json

from flask_socketio import send,emit,join_room,leave_room

from . import socketio


@socketio.on('connect',namespace='/admin')
def admin_connect_handler():
	print('admin connect')
	order_dicts=Order.objects().as_pymongo()
	order_dicts=sorted(order_dicts,key=lambda e :Order.delivery_state_key(e['delivery_state']))
	for order_dict in order_dicts:
		for field in ['_id','recieve_time','delivery_time','store_id','consumer_id','delivery_id']:
			order_dict[field]=str(order_dict[field])
	emit('order_data',json.dumps(order_dicts))

@socketio.on('order_delete',namespace='/admin')
def order_delete_handler(order_id):
	print('admin order_delete')
	if Order.objects(id=order_id).delete()==1 :
		emit('order_delete',{'message':'success'})
	else:
		emit('order_delete',{'message':'failed'})
		

@socketio.on('order_state_update',namespace='/admin')
def order_state_update_handler(request):
	print('admin order_state_update')
	if Order.objects(id=request['order_id']).update_one(set__delivery_state=request['delivery_state'],set__store_state=request['store_state'])==1:
		emit('order_state_update',{'message':'success'})
	else:
		emit('order_state_update',{'message':'failed'})

@socketio.on('disconnect',namespace='/admin')
def admin_disconnect_handler():
	print('admin disconnect')
	
	
@socketio.on('connect',namespace='/delivery_man')
def delivery_man_connect_handler():
	print('delivery_man connect')
	order_dicts=list(Order.objects(delivery_state='pending').as_pymongo())
	for order_dict in order_dicts:
		for field in ['_id','recieve_time','delivery_time','store_id','consumer_id','delivery_id']:
			order_dict[field]=str(order_dict[field])
	emit('order_data',json.dumps(order_dicts))


@socketio.on('order_accept',namespace='/delivery_man')
def order_accept_handler(order_id):
	print('delivery_man order_accept')
	#no delivery_man info
	if Order.objects(id=order_id,delivery_state='pending').update_one(set__delivery_state='accepted')==1 :
		emit('order_accept','success')
	else:
		emit('order_accept','failed')
	

@socketio.on('disconnect',namespace='/delivery_man')
def delivery_man_disconnect_handler():
	print('delivery_man disconnect')
	
	
@socketio.on('connect',namespace='/restaurant')
def delivery_man_connect_handler():
	print('restaurant connect')
	#no store_id
	order_dicts=list(Order.objects(delivery_state__in=['pending','accepted']).as_pymongo())
	for order_dict in order_dicts:
		for field in ['_id','recieve_time','delivery_time','store_id','consumer_id','delivery_id']:
			order_dict[field]=str(order_dict[field])
	emit('order_data',json.dumps(order_dicts))
	#join_room(room)


@socketio.on('order_confirm',namespace='/restaurant')
def order_accept_handler(order_id):
	print('restaurant order_confirm')
	#no delivery_man info
	if Order.objects(id=order_id).update_one(set__store_state='confirmed')==1 :
		emit('order_confirm','success')
	else:
		emit('order_confirm','failed')
	

@socketio.on('disconnect',namespace='/restaurant')
def delivery_man_disconnect_handler():
	print('restaurant disconnect')


