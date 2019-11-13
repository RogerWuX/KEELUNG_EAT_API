import sys
from models import Order
from datetime import datetime

if sys.argv[1] == 'seed':
	order_ids=Order.objects.insert(
	[
		Order(recieve_time=datetime(2019,8,9,0,0),delivery_time=(2019,8,9,1,0),
			district='中正區',address='北寧路2號',

			delivery_state='pending',store_state='confirmed')
		
		

	]
	,load_bulk=False)
	with open('ids.txt','a') as f:
		for id in order_ids:
			f.write(str(id))
elif sys.argv[1] == 'rollback':
	with open('ids.txt','r') as f:
		contents_read_by_line=f.readlines()
		Order.objects(id__in=contents_read_by_line).delete()
elif sys.argv[1] == 'delete_all':
	Order.objects.delete()
	with open('ids.txt','w') as f:
		pass;
