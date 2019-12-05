from mongoengine import *
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from . import app

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

	# 密碼加密
	def hash_password(self, password):
		self.password = custom_app_context.encrypt(password)

    # 密碼解析
	def verify_password(self, password):
		return custom_app_context.verify(password, self.password) 

    # 獲取token，有效時間10min
	def generate_auth_token(self, expiration=600):
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		print(str(self.id))
		return s.dumps({'id': str(self.id)})

    # 解析token，確認登錄的用戶身份
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			print('valid token, but expired')
			return None  # valid   token, but expired
		except BadSignature:
			print('invalid token')
			return None  # invalid token
		user = User.objects(id = str(data['id'])).get()
		return user

	