from flask import Flask, render_template, request, jsonify, url_for, session, redirect
from pymongo import MongoClient
import hashlib, datetime, jwt

client = MongoClient('localhost', 27017)
db = client.db_dotori


app = Flask(__name__)

SECRET_KEY = 'DOTORI'

# index 페이지
@app.route('/')
def index():
   return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_member():
    username = request.form['username']
    nickname = request.form['nickname']
    userid = request.form['userid']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    member = {'username':username, 'nickname':nickname, 'userid':userid, 'password':password_hash}
    db.users.insert_one(member)
    
    return jsonify({'result': 'success'})


@app.route('/login', methods=['POST'])
def login_api():
    userid = request.form['userid']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    result = db.users.find_one({'userid': userid})
    
    if result is not None:
        
        result_pw = db.users.find_one({'password': password_hash})
        
        if result_pw is not None:
            payload = {
            'id': userid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        
            return jsonify({'result': 'success', 'token': token})
        
        
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디가 없습니다.'})



if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)