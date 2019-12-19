import KeelungEat.models
from flask import Flask, jsonify, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from mongoengine import *
import mongoengine as me
import json
from bson import ObjectId
from . import app
from .models import *
#from flask_httpauth import HTTPBasicAuth
from .auth import *
import requests
import time
import os
import base64


#auth = HTTPBasicAuth()

@app.route('/search', methods=['POST'])
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

#@auth.login_required
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

@app.route('/distance', methods=['POST'])
def distance():
	api_key ='AIzaSyB2qSt6SBvkcbnaKYLSlpuTI9RNYtR9NSg'
	url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
	json_data = request.get_json()
	source = '202基隆市'+str(json_data['source'])
	dest = '202基隆市'+str(json_data['dest'])

	r = requests.get(url + 'origins=' + source +
					'&destinations=' + dest +
					'&key=' + api_key) 
	output = r.json() 

	rows = output['rows']
	elements = rows[0]
	ele = elements['elements']
	info = ele[0]
	distance_info = info['distance']
	duration_info = info['duration']
	distance = distance_info['text']
	duration = duration_info['text']
	if distance_info['value'] < 5000:
		fee = 30
	else:
		fee = 50

	arr = []
	arr.append({'distance' : distance, 'duration' : duration, 'fee' : fee})

	return jsonify(arr)

@app.route('/geo', methods=['POST'])
def geo():
	api_key ='AIzaSyB2qSt6SBvkcbnaKYLSlpuTI9RNYtR9NSg'
	url ='https://maps.googleapis.com/maps/api/geocode/json?'
	json_data = request.get_json()
	address = '202基隆市'+str(json_data['address'])

	r = requests.get(url + 'address=' + address +
					'&key=' + api_key) 
	output = r.json() 
	results = output['results']
	geo = results[0]
	geometry = geo['geometry']
	location = geometry['location']

	return jsonify(location)


basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/image/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  
    if f and allowed_file(f.filename):  
        fname = secure_filename(f.filename)
        #print fname
        ext = fname.rsplit('.', 1)[1] 
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  
        f.save(os.path.join(file_dir, new_filename)) 
       
        store = Store.objects(name = request.form['store_name']).get()
        for food in store.foods:
        	if food['name'] == request.form['food_name']:
        		food['image_url'] = app.config['UPLOAD_FOLDER'] + new_filename
        		break;
        store.save()
		
        return jsonify({"errmsg": "success", "fileName": new_filename})
    else:
        return jsonify({"errmsg": "fail"})
