
from.models import *

from flask import request,g
import json

from flask_socketio import send,emit,join_room,leave_room

from . import socketio
from.auth import auth



@socketio.on('connect',namespace='/admin')
def admin_connect_handler():
	print('admin connect')
	print(request.cookies['token'])
	order_dicts=Order.objects().as_pymongo()
	order_dicts=sorted(order_dicts,key=lambda e :Order.delivery_state_key(e['delivery_state']))
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		order_dict['store_name']=Store.objects(id=order_dict['store_id']).only('name').first().name
	emit('order_data',json.dumps(order_dicts))

@socketio.on('order_delete',namespace='/admin')
def admin_order_delete_handler(order_id):
	print('admin order_delete')
	if Order.objects(id=order_id).delete()==1 :
		emit('order_delete',{'message':'success'})
	else:
		emit('order_delete',{'message':'failed'})
		

@socketio.on('order_state_update',namespace='/admin')
def admin_order_state_update_handler(request):
	print('admin order_state_update')
	if request['delivery_state'] not in Order.delivery_state_choice or request['store_state'] not in Order.store_state_choice:
		emit('order_state_update',{'message':'format problem'})
	if Order.objects(id=request['order_id']).update_one(set__delivery_state=request['delivery_state'],set__store_state=request['store_state'] )==1:
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
		Order.dict_to_string(order_dict)
		order_dict['store_name']=Store.objects(id=order_dict['store_id']).only('name').first().name
	emit('order_data',json.dumps(order_dicts))


@socketio.on('order_accept',namespace='/delivery_man')
def delivery_man_order_accept_handler(order_id):
	print('delivery_man order_accept')
	if Order.objects(id=order_id,delivery_state='pending').update_one(set__delivery_state='accepted',set__delivery_id=g.user.id)==1 :
		emit('order_accept','success')
	else:
		emit('order_accept','failed')
	

@socketio.on('disconnect',namespace='/delivery_man')
def delivery_man_disconnect_handler():
	print('delivery_man disconnect')
	
	
@socketio.on('connect',namespace='/restaurant')
def restaurant_connect_handler():
	print('restaurant connect')
	print(current_user)
	order_dicts=list(Order.objects(delivery_state__in=['pending','accepted'],owner_id=g.user.id).as_pymongo())
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
	emit('order_data',json.dumps(order_dicts))
	join_room(Store.objects(owner_id=g.user.id).only('id').first().id)


@socketio.on('order_confirm',namespace='/restaurant')
def restaurant_order_confirm_handler(order_id):
	print('restaurant order_confirm')	
	if Order.objects(id=order_id).update_one(set__store_state='confirmed')==1 :
		emit('order_confirm','success')
	else:
		emit('order_confirm','failed')
	

@socketio.on('disconnect',namespace='/restaurant')
def restaurant_disconnect_handler():
	print('restaurant disconnect')


