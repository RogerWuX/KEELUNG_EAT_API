from mongoengine import *
class Order(Document):
	delivery_state_choice=['pending','accepted','delivering','finished']
	store_state_choice=['rejected','unconfirmed','confirmed']
	receive_time=DateTimeField()
	delivery_time=DateTimeField()
	district=StringField()
	address=StringField()
	consumer_id=ObjectIdField()
	store_id=ObjectIdField()
	delivery_id=ObjectIdField()
	foods=ListField()
	total_price=DecimalField()
	delivery_state=StringField(choice=delivery_state_choice)	
	store_state=StringField()
	meta = {
        'collection': 'Order'
    }
	@staticmethod
	def delivery_state_key(state):
		for i in range(0,len(Order.delivery_state_choice)):
			if state == Order.delivery_state_choice[i]:
				return i;
	@staticmethod
	def dict_to_string(dict):
		for field in ['_id','receive_time','delivery_time','store_id','consumer_id','delivery_id']:
			if field in dict:
				dict[field]=str(dict[field])
