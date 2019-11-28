from mongoengine import *
class Store(me.Document):
	owner_id = me.StringField()
	name = me.StringField(required=True)
	district = me.StringField()
	address = me.StringField()
	tel = me.StringField()
	info = me.StringField()	
	foods = ListField()
	meta  = { 'collection' : 'Store' }