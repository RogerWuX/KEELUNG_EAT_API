
from.models import *

from flask import request,g,session
import json

from flask_socketio import send,emit,join_room,leave_room,disconnect

from . import socketio
from.auth import auth



@socketio.on('connect',namespace='/admin')
def admin_connect_handler():
	print('admin connect')
	user=User.objects(token=request.args.get('token')).first()
	print(user)
	if user==None or user.identity!='4':
		disconnect()
		return
	session['user']=user
	order_dicts=list(Order.objects().as_pymongo())

	if order_dicts==None:
		return
	#order_dicts=sorted(order_dicts,key=lambda e :Order.delivery_state_key(e['delivery_state']))
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		order_store=Store.objects(id=order_dict['store_id']).first()
		if order_store != None:
			order_dict['store_name']=order_store.name
			for food in order_dict['foods']:
				for food_info in order_store.foods:
					if food_info['id'] == food['food_id'] :
						food['name']=food_info['name']
						
	emit('order_data',json.dumps(order_dicts))

@socketio.on('order_delete',namespace='/admin')
def admin_order_delete_handler(order_id):
	print('admin order_delete')
	if Order.objects(id=order_id).delete()==1 :
		emit('order_delete',{'message':'success'})
	else:
		emit('order_delete',{'message':'failed'})
	order_dicts=Order.objects().as_pymongo()
	if order_dicts==None:
		return
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		order_dict['store_name']=Store.objects(id=order_dict['store_id']).only('name').first().name
		emit('order_data',json.dumps(order_dicts))
		

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
	user=User.objects(token=request.args.get('token')).first()
	if user==None  or user.identity!='1':
		disconnect()
		return
	session['user']=user
	order_dicts=list(Order.objects(delivery_state='pending').as_pymongo())
	print(order_dicts)
	if order_dicts==None:
		return
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		order_store=Store.objects(id=order_dict['store_id']).first()
		order_dict['store_name']=order_store.name
		for food in order_dict['foods']:
			for food_info in order_store.foods:
				if food_info['id'] == food['food_id'] :
					food['name']=food_info['name']
	emit('order_data',json.dumps(order_dicts))


@socketio.on('order_accept',namespace='/delivery_man')
def delivery_man_order_accept_handler(order_id):
	print('delivery_man order_accept')
	if Order.objects(id=order_id,delivery_state='pending').update_one(set__delivery_state='accepted',set__delivery_id=session['user'].id)==1 :
		emit('order_accept','success')
	else:
		emit('order_accept','failed')

@socketio.on('disconnect',namespace='/delivery_man')
def delivery_man_disconnect_handler():
	print('delivery_man disconnect')

@socketio.on('connect',namespace='/delivery_man_current')
def delivery_man_current_connect_handler():
	print('delivery_man_current connect')
	user=User.objects(token=request.args.get('token')).first()
	if user==None  or user.identity!='1':
		disconnect()
		return
	session['user']=user
	order_dicts=list(Order.objects(delivery_id=str(user.id)).as_pymongo())
	if order_dicts==None:
		return
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		consumer_doc=User.objects(id=order_dict['consumer_id']).first()
		order_dict['consumer_tel']=consumer_doc.tel
		order_dict['consumer_name']=consumer_doc.name
		order_store=Store.objects(id=order_dict['store_id']).first()
		order_dict['store_name']=order_store.name
		for food in order_dict['foods']:
			for food_info in order_store.foods:
				if food_info['id'] == food['food_id'] :
					food['name']=food_info['name']
	emit('order_data',json.dumps(order_dicts))

@socketio.on('delivery_man_state_update',namespace='/delivery_man_current')
def delivery_man_state_update_handler():
	print('delivery_man_state_update')
	user_doc=User.objects(id=session['user'].id).first()
	if user_doc.status=='1':
		user_doc.status='0'
	else:
		user_doc.status='1'
	user_doc.save()
	emit('delivery_man_state_update',str(user_doc.status))
	
	
@socketio.on('delivery_state_update',namespace='/delivery_man_current')
def delivery_man_delivery_state_update_handler(order_id):
	print('delivery_man_current delivery_state_update')
	order_doc=Order.objects(id=order_id).first()
	if order_doc==None :
		emit('delivery_state_update','failed, order not found')
		return
	for index in range(0,len(Order.delivery_state_choice)):
		if Order.delivery_state_choice[index]==order_doc.delivery_state and index < len(Order.delivery_state_choice)-1:
			order_doc.delivery_state=Order.delivery_state_choice[index+1]
			order_doc.save()
			socketio.emit('order_state_change',Order.delivery_state_choice[index+1],namespace='/consumer',room=str(order_doc.consumer_id),broadcast=True)
			emit('delivery_state_update','success')
			return
	emit('delivery_state_update','failed, fuck you')
		
@socketio.on('disconnect',namespace='/delivery_man_current')
def delivery_man_current_disconnect_handler():
	print('delivery_man_current disconnect')
	
	
@socketio.on('connect',namespace='/restaurant')
def restaurant_connect_handler():
	print('restaurant connect')
	user=User.objects(token=request.args.get('token')).first()
	if user==None or user.identity!='2':
		disconnect()
		return
	session['store']=Store.objects(owner_id=str(user.id)).first()
	
	order_dicts=list(Order.objects(store_id=session['store'].id,delivery_state__in=['pending','accepted']).as_pymongo())
	print(order_dicts)
	if order_dicts==None:
		return
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		order_store=Store.objects(id=order_dict['store_id']).first()
		order_dict['store_name']=order_store.name
		for food in order_dict['foods']:
			for food_info in order_store.foods:
				if food_info['id'] == food['food_id'] :
					food['name']=food_info['name']
	emit('order_data',json.dumps(order_dicts))
	join_room(session['store'].id)


@socketio.on('order_confirm',namespace='/restaurant')
def restaurant_order_confirm_handler(order_id):
	print('restaurant order_confirm')	
	if Order.objects(id=order_id,store_id=session['store'].id).update_one(set__store_state='confirmed')==1 :
		emit('order_confirm','success')
	else:
		emit('order_confirm','failed')
	

@socketio.on('disconnect',namespace='/restaurant')
def restaurant_disconnect_handler():
	print('restaurant disconnect')

@socketio.on('connect',namespace='/consumer')
def consumer_connect_handler():
	print('consumer connect')
	user=User.objects(token=request.args.get('token')).first()
	if user==None  or user.identity!='0':
		disconnect()
		return
	order_dicts=list(Order.objects(consumer_id=user.id, delivery_state__in=['pending','accepted','delivering']).as_pymongo())
	if order_dicts==None:
		return
	for order_dict in order_dicts:
		Order.dict_to_string(order_dict)
		order_store=Store.objects(id=order_dict['store_id']).first()
		order_dict['store_name']=order_store.name
		for food in order_dict['foods']:
			for food_info in order_store.foods:
				if food_info['id'] == food['food_id'] :
					food['name']=food_info['name']
	emit('order_data',json.dumps(order_dicts))
	join_room(str(user.id))


@socketio.on('disconnect',namespace='/consumer')
def consumer_disconnect_handler():
	print('consumer disconnect')
