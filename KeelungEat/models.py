from mongoengine import *
connect(host='mongodb+srv://WuRoger:RogerWuIsMe@cluster0-upq73.gcp.mongodb.net/KEELUNG_EAT?retryWrites=true&w=majority')

class Order(Document):
	recieve_time=DateTimeField()
	district=StringField()
	address=StringField()
	store=ListField()
	meta = {
        'collection': 'Order'
    }
	