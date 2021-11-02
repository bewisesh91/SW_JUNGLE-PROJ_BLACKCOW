from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient, message
import jwt, hashlib, datetime



app = Flask(__name__)
SECRET_KEY = 'black_cow'

client = MongoClient('localhost', 27017)
db = client.dbjungle_black_cow


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None :
        token_receive = bytes(token_receive[2:-1].encode('ascii'))

        try:
            payload= jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({'email': payload['ID']})
            return render_template('index.html', user_info=user_info)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('/sign_in', message = "로그인 시간이 만료되었습니다."))
    else :
        return render_template('index.html')


### 회원 가입 기능 구현 ###
@app.route('/sign_up', methods=['GET'])
def sing_up():
    return render_template('signup.html', title = '회원가입')


@app.route('/sign_up', methods=['POST'])
def sign_up_save():
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
def sign_in():
    return render_template('signin.html')

@app.route('/sign_in', methods=['POST'])
def sign_in_user():
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'email': email_receive, 'password': password_hash})

    print(result)

    if result is not None :
        payload = {
            'ID': email_receive,
            'EXP': str(datetime.datetime.utcnow() + datetime.timedelta(seconds = 60 * 60 * 24))
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'result': 'success', 'token': str(token)})
    else :
        return jsonify({'result': 'fail', 'message': 'E-mail/Password가 정확하지 않습니다.'})


if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)
