import json
import threading
from gather_items import gather_hellomarket, gather_bunjang, gather_joongna
from utils import process_product_info, token_to_id, generate_crawling_response
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt, hashlib, datetime

app = Flask(__name__)
SECRET_KEY = 'black_cow'

client = MongoClient('localhost', 27017)

db = client.dbjungle_black_cow

cache = {}

def error_handler(func):
    def decorated():
        try:
            return func()
        except:
            return render_template('404.html')
    decorated.__name__ = func.__name__
    return decorated


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
@error_handler
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
@error_handler
def check_up():
    email_receive = request.form['email_give']
    duplicate = bool(db.users.find_one({'email': email_receive}))
    return jsonify({'result': 'success', 'duplicate':duplicate})


### 로그인 기능 구현 ###
@app.route('/sign_in', methods=['GET'])
def sign_in():
    return render_template('signin.html', title = '로그인')


@app.route('/sign_in', methods=['POST'])
@error_handler
def sign_in_user():
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    
    result = db.users.find_one({'email': email_receive, 'password': password_hash})
    
    if result is not None :
        payload = {
            'ID': email_receive,
            'NAME': result['username'],
            'EXP': str(datetime.datetime.utcnow() + datetime.timedelta(seconds = 60 * 60 * 24))
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'result': 'success', 'token': str(token)})
    else :
        return jsonify({'result': 'fail', 'message': 'E-mail/Password가 정확하지 않습니다.'})


# 상품 정보 가져오기 기능 구현 
@app.route('/products', methods=['GET'])
@error_handler
def get_products():
    parameter_dict = request.args.to_dict()
    query = parameter_dict['q']
    token_receive = request.cookies.get('mytoken')
    
    threads = []
    result_dict = {}
    search_functions = [gather_bunjang, gather_joongna, gather_hellomarket]
    args = (query, result_dict)
    for fn in search_functions:
        th = threading.Thread(target = fn, args = args)
        threads.append(th)
    
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    user_favorites_pid = set()
    if token_receive is not None :
        user_id = token_to_id(token_receive, SECRET_KEY)
        user_favorites = list(db.favorites.find({"user_id": user_id}))    
        for user_favorite in user_favorites:
            user_favorites_pid.add(user_favorite['pid'])
    
        processed = process_product_info(result_dict, user_favorites_pid)
        products_res, details_res = generate_crawling_response(processed)
        cache[user_id] = details_res
    else:
        processed = process_product_info(result_dict, user_favorites_pid)
        products_res, details_res = generate_crawling_response(processed)
        
    return jsonify(products_res)


@app.route('/details', methods=['GET'])
@error_handler
def get_details():
    parameter_dict = request.args.to_dict()
    company = parameter_dict['c']
    token_receive = request.cookies.get('mytoken')
    
    if token_receive is not None :
        user_id = token_to_id(token_receive, SECRET_KEY)
        if user_id in cache:
            details_res = cache[user_id][company]
        else:
            details_res = {'result':'fail'}
    else:        
        details_res = {'result':'fail'}
    
    return jsonify(details_res)


@app.route('/favorite', methods=['POST'])
@error_handler
def add_favorite():
    title = request.form['title']
    image_url = request.form['image_url']
    price = request.form['price']
    company = request.form['company']
    pid = request.form['detail_url'].split('/')[-1]
    token_receive = request.cookies.get('mytoken')
    user_id = token_to_id(token_receive, SECRET_KEY)
    
    document = {
        'title': title,
        'pid': pid,
        'image_url': image_url,
        'price': price,
        'user_id': user_id,
        'company': company,
    }

    count = db.favorites.count_documents({
        'pid': pid, 
        'user_id': user_id
    })
    response = {'result':'fail'}
    
    if not count:    
        result = db.favorites.insert_one(document)
        if result.acknowledged:
            response = {'result':'success'}
    return jsonify(response)


@app.route('/favorite', methods=['DELETE'])
@error_handler
def remove_favorite():
    pid = request.form['detail_url'].split('/')[-1]
    token_receive = request.cookies.get('mytoken')
    user_id = token_to_id(token_receive, SECRET_KEY)
    
    result = db.favorites.delete_one({
            'pid': pid, 
            'user_id': user_id
        })
    if result.deleted_count:
        return {'result': 'success'}
    return {'result': 'fail'}


@app.route('/my_page', methods=['GET'])
def my_page():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None :
        user_id = token_to_id(token_receive, SECRET_KEY)
        user_favorites = list(db.favorites.find({"user_id": user_id}))
        return render_template('mypage.html', user_favorites = user_favorites)
    else :
        return render_template('signin.html')
    

if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)


