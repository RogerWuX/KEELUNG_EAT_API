from flask import Flask , jsonify , request, abort, g, make_response, Response
from mongoengine import *
import json
from bson import ObjectId
#from flask_cors import cross_origin
from .models import *
#from flask_httpauth import HTTPBasicAuth
import os
from .auth import *
#----------------------------------------------------------
#auth = HTTPBasicAuth()

@app.route('/register', methods=['POST'])
def new_user():
    json_data = request.get_json()
    name = json_data['name']
    email = json_data['email']
    password = json_data['password']
    district = json_data['district']
    address = json_data['address']
    identity = json_data['identity']
    status = json_data['status']
    tel = json_data['tel']

    if email is None or password is None:
        abort(400)  # missing arguments
    if User.objects(email=email).first() is not None:
        abort(400)  # existing user
    user = User(name=name, email=email, district=district, address=address, identity='0', status=status, tel=tel)
    user.hash_password(password)
    user.save()
    return jsonify({'name': user.name, 'password': user.password, 'district': user.district, 'address': user.address, 'identity': user.identity, 'status': user.status, 'tel': user.tel})

@auth.verify_password
def verify_password(email_or_token, password):
    if request.path == "/login":
        email_and_password_post = request.get_json()
        if email_and_password_post.get('email') is not None:
            email_or_token = email_and_password_post['email']
        if email_and_password_post.get('password') is not None:
            password = email_and_password_post['password']

        user = User.objects(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        """data = request.get_json()
        token = data['token']"""
        token=request.cookies.get('token')
        user = User.verify_auth_token(token)
        if not user:
            return False
    g.user = user
    return True
    
@app.route('/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    token = str(token, encoding='utf8')
    User.objects(id = str(g.user.id)).update(
      token = token
    )
    print(str(g.user['id']))
    response=make_response(token)  
    response.set_cookie('token',token, max_age=600) 
    return response

#-----------------------------------------------------------
@app.route('/check',methods=['get'])
def check():
    token=request.cookies.get('token')
    if token is None:
        return jsonify(False)
    else:
        return jsonify(True)

@app.route("/auth", methods=['GET'])
@auth.login_required
def auth():
    output = []
    output.append( {'id': str(g.user.id) , 'name' : g.user.name , 'email' : g.user.email , 'password' : g.user.password , 'district' : g.user.district , 'address' : g.user.address , 'identity' : g.user.identity , 'status' : g.user.status , 'tel' : g.user.tel, 'token': g.user.token} )
    return jsonify(output)

@app.route('/User/View_Delivery' , methods = ['GET']) 
#@cross_origin()
#@auth.login_required
def view_all_delievery_man ():
 Users =  User.objects().all()
 output = []
 for user in Users:
      if user['identity'] is '1' :
       output.append( {'id': str(user['id']) , 'name' : user['name'] , 'email' : user['email'] , 'password' : user['password'] , 'district' : user['district'] , 'address' : user['address'] , 'identity' : user['identity'] , 'status' : user['status'] , 'tel' : user['tel'] } )
    
 return jsonify(output)


@app.route('/User/View_User' , methods = ['GET']) 
#@cross_origin()
def view_all_user ():
 Users =  User.objects().all()
 output = []
 for user in Users:
      if user['identity'] is '0' :
       output.append( {'id': str(user['id']) , 'name' : user['name'] , 'email' : user['email'] , 'password' : user['password'] , 'district' : user['district'] , 'address' : user['address'] , 'identity' : user['identity'] , 'status' : user['status'] , 'tel' : user['tel'] } )
    
 return jsonify(output)
 
 
@app.route('/User/View_User_and_Delivery' , methods = ['GET']) 
#@cross_origin()
def view_all_user_delievery ():
 Users =  User.objects().all()
 output = []
 for user in Users:
       output.append( {'id': str(user['id']) , 'name' : user['name'] , 'email' : user['email'] , 'password' : user['password'] , 'district' : user['district'] , 'address' : user['address'] , 'identity' : user['identity'] , 'status' : user['status'] , 'tel' : user['tel'] } )
    
 return jsonify(output)
 


@app.route('/User/insert' , methods=['POST'] )
#@cross_origin()
def create_delievery():

  data = request.json
  user = User(name = str(data['name']) , email = str(data['email']) , password = str(data['password']) , district = str(data['district']) , address = str(data['address']) , identity = '0' , status = '0' , tel = str(data['tel'])  )
  user.save()
  return jsonify(True)


@app.route('/User/delete' , methods=['POST'])
#@cross_origin()
def delete_delievery():
  
  data = request.json
 # print(request.get_json()) 
  User.objects(id = str(data['id']) ).delete()
  return jsonify(True)



@app.route('/User/modify' , methods = ['POST'])
#@cross_origin()
def modify_delievery():

  data = request.json
  
  User.objects(id = str(data['id'])).update( name = str(data['name'])) 
  if 'password' in data :
   User.objects(id = str(data['id'])).update( password = str( data['password'] ) ) 
  User.objects(id = str(data['id'])).update( district = str( data['district'] ) )
  User.objects(id = str(data['id'])).update( address = str (data['address'] ) )
  if 'identity' in data :
   User.objects(id = str(data['id'])).update( identity = str ( data['identity'] ) )
  User.objects(id = str(data['id'])).update( tel =  str(data['tel'] ) )  

  

  return jsonify(True)
