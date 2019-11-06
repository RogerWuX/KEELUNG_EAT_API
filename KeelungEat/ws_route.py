
from KeelungEat.models import Order

from flask import request

from flask_socketio import send,emit,join_room,leave_room

from . import socketio

@socketio.on('connect',namespace='admin')
def all_order_connect_handler():
	print('admin_connect')	
	socketio.emit('order_data',Order.objects().to_json(),namespace='admin',broadcast=True)


@socketio.on('disconnect',namespace='admin')
def all_order_disconnect_handler():
	print('disconnect')
	
@socketio.on('get_order')
def all_order_disconnect_handler():
	print('getorder')
	

	
	