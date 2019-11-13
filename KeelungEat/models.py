from mongoengine import *
connect(host='mongodb+srv://WuRoger:RogerWuIsMe@cluster0-upq73.gcp.mongodb.net/KEELUNG_EAT?retryWrites=true&w=majority')

class Order(Document):
	delivery_state_choice=['pending','accepted','delivering','finished']
	store_state_choice=['unconfirmed','confirmed']
	recieve_time=DateTimeField()
	delivery_time=DateTimeField()
	district=StringField()
	address=StringField()
	consumer_id=ObjectIdField()
	store_id=ObjectIdField()
	delivery_id=ObjectIdField()
	foods=ListField()
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
	def to_string_dict(dict):
		dict['_id']=str(dict['_id'])
		dict['consumer_id']=str(dict['consumer_id'])
		dict['delivery_id']=str(dict['delivery_id'])		
		dict['store_id']=str(dict['store_id'])
		dict['recieve_time']=str(dict['recieve_time'])
		dict['delivery_time']=str(dict['recieve_time'])
		
	