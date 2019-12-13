from . import socketio
from .models import *
import datetime 

EXPIRED_ORDER_CLEAN_INTERVAL_SEC=10

def expired_order_cleaner():
	while True:
		socketio.sleep(EXPIRED_ORDER_CLEAN_INTERVAL_SEC)
		print("clean expired order")
		#Order.objects(receive_time__le=datetime.datetime.now()).delete()


socketio.start_background_task(target=expired_order_cleaner)