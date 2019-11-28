from mongoengine import *
class User(Document):
	name = StringField(required=True)
	email =  StringField()
	password = StringField()
	district = StringField()
	address = StringField()
	identity = StringField()
	status = StringField()
	tel = StringField()
	meta = {'collection': 'User'}

	