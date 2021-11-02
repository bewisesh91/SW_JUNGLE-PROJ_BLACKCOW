from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt, hashlib, datetime


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'black_cow'

client = MongoClient('localhost', 27017)
db = client.dbjungle_black_cow


@app.route('/')
def home():
    return render_template('index.html')


### 회원 가입 기능 구현 ###
@app.route('/sign_up', methods=['GET'])
def sing_up():
    return render_template('singup.html')


@app.route('/sign_up', methods=['POST'])
def sign_up():
    # 회원 가입 시 받을 정보 3가지 
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    email_receive = request.form['email_give']

    # password의 경우 보안을 위해 hash 처리
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    user_data = {
        'username': username_receive,
        'password': password_hash,
        'email': email_receive
    }

    db.users.insert_one(user_data)
    return jsonify({'result': 'success'})


@app.route('/check_up', methods=['POST'])
def check_up():
    email_receive = request.form['email_give']
    duplicate = bool(db.users.find_one({'email': email_receive}))
    return jsonify({'result': 'success', 'duplicate':duplicate})


### 로그인 기능 구현 ###
@app.route('/sign_in', methods=['GET'])
def sing_in():
    return render_template('signin.html')





if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)