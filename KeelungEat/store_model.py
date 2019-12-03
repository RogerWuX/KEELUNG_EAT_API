from mongoengine import *
class Store(Document):
	owner_id = StringField()
	name = StringField(required=True)
	district = StringField()
	address = StringField()
	tel = StringField()
	info = StringField()	
	foods = ListField()
	meta  = { 'collection' : 'Store' }