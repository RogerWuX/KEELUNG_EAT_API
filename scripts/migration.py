import sys
from datetime import datetime
sys.path.append("..")
from KeelungEat.models import Order


if sys.argv[1] == 'seed':
	order_ids=Order.objects.insert(
	[
		Order(
			recieve_time=datetime(2019,8,9,0,0),
			delivery_time=None,
			district='中正區',address='北寧路2號',
			consumer_id='5dc3c34ff1733b1e786c8389',
			store_id='5dc3c34ff1733b1e786c8389',
			delivery_id='5dc3c34ff1733b1e786c8389',
			foods=[{'food_id':'5dc3c34ff1733b1e786c8389','number':5}],
			delivery_state='finished',
			store_state='confirmed')
		
		
		

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
