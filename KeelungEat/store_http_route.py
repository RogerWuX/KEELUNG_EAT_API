from flask import Flask, jsonify, request
from mongoengine import *
import mongoengine as me
import json
from bson import ObjectId

from . import app
import KeelungEat.models

@app.route('/search', methods=['GET'])
#@cross_origin()
def search():
  """http://localhost:5000/search"""
  data = request.json
  stores = Store.objects(district = str(data['district'])).all()
  output = []
  for store in stores:
    output.append({'owner_id' : str(store['owner_id']), 'id' : str(store['id']), 'name' : store['name'], 'district' : store['district'], 'address' : store['address'], 'tel' : store['tel'], 'info' : store['info'], 'foods' : store['foods']})
  return jsonify(output)

@app.route('/user', methods=['GET'])
#@cross_origin()
def get_all_users():
  """http://localhost:5000/user"""
  users = User.objects().all()
  output = []
  for user in users:
    output.append({'id' : str(user['id']), 'email' : user['email'], 'name' : user['name'], 'district' : user['district'], 'address' : user['address'], 'tel' : user['tel'], 'identity' : user['identity'], 'status' : user['status']})
  return jsonify(output)
  
@app.route('/store', methods=['GET'])
#@cross_origin()
def get_all_stores():
  """http://localhost:5000/store"""
  stores = Store.objects().all()
  output = []
  for store in stores:
    output.append({'owner_id' : str(store['owner_id']), 'id' : str(store['id']), 'name' : store['name'], 'district' : store['district'], 'address' : store['address'], 'tel' : store['tel'], 'info' : store['info'], 'foods' : store['foods']})
  return jsonify(output)

@app.route('/store/search', methods=['POST'])
#@cross_origin()
def get_one_stores():
  data = request.json
  store = Store.objects(id = str(data['id'])).get()
  output = []
  output.append({'owner_id' : str(store['owner_id']), 'id' : str(store['id']), 'name' : store['name'], 'district' : store['district'], 'address' : store['address'], 'tel' : store['tel'], 'info' : store['info'], 'foods' : store['foods']})
  return jsonify(output)

@app.route('/store/insert', methods=['POST']) 
#@cross_origin()
def insert_store():
	"""http://localhost:5000/store/insert?email=email&name=ntou&district=中正區&address=北寧路&tel=12345678&info=學校"""
	data = request.json
	user = User.objects(email = str(data['email'])).get()
	user.identity = '2'
	user.save()
	store = Store(owner_id = str(user.id), name = str(data['name']), district = str(data['district']), address = str(data['address']), tel = str(data['tel']), info = str(data['info']))
	store.foods = data['foods']
	store.save()

	for food in store.foods:
		id = str(ObjectId())
		food['id'] = id
		store.save()
	
	return jsonify(True)

@app.route('/store/delete', methods=['POST'])
#@cross_origin()
def delete_store():
	"""http://localhost:5000/store/delete?id=id"""
	data = request.json
	Store.objects(id = str(data['id'])).delete()
	return jsonify(True)

@app.route('/store/update', methods=['PUT'])
#@cross_origin()
def update_store():
	"""http://localhost:5000/store/update?store_id=id&name=ntou&district=中正區&address=北寧路&tel=12345678&info=學校"""
	data = request.json
	Store.objects(id = str(data['store_id'])).update(
		name = str(data['name']),
	    district = str(data['district']),
	    address = str(data['address']),
	    tel = str(data['tel']),
	    info = str(data['info'])
		)

	"""foods"""

	food = []
	id = str(ObjectId())
	data = request.json
	store = Store.objects(id = str(data['store_id'])).get()

	ele = 0
	for food in store.foods:
		del store.foods[ele]
		ele += 1

	store.save()

	store.foods = data['foods']
	store.save()

	for food in store.foods:
		id = str(ObjectId())
		food['id'] = id
		store.save()

	return jsonify(True)
