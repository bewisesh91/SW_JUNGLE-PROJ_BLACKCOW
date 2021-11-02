from flask import Flask, json, render_template, jsonify, request
import requests
import json
import datetime
from bson.json_util import dumps
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('index.html', hello = '안녕')


@app.route('/signin')
def signin():

    return render_template('pages/signin/index.j2', pageName = '로그인')

@app.route('/signup')
def signup():

    return render_template('pages/signup/index.j2', pageName = '회원가입')

@app.route('/mypage')
def mypage():
    # 로그인 안되어있을 경우, 접근 제한 기능,
    return render_template('pages/mypage/index.j2', pageName = '마이페이지')

# @app.route('/mypage')
# def mypage():
    
#     return render_template('pages/mypage/index.j2', pageName = '마이페이지')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)