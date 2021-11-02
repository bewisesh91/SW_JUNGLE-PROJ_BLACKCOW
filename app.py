from flask import Flask, json, render_template, jsonify, request
import requests
import json
import datetime
from bson.json_util import dumps
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('index.j2')






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)