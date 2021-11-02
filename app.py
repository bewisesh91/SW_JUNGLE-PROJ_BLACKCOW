from flask import Flask, request, jsonify
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.db_blackcow

app = Flask(__name__)

@app.route('/favorite', methods=['POST'])
def add_favorite():
    title = request.form['title']
    image_url = request.form['image_url']
    price = request.form['price']
    pid = request.form['detail_url'].split('/')[-1]
    user_id = request.form['user_id']
    
    document = {
        'title': title,
        'pid': pid,
        'image_url': image_url,
        'price': price,
        'user_id': user_id
    }
    count = db.favorite.count_documents({
        'pid': pid, 
        'user_id': user_id
    })
    response = {'result':'fail'}
    
    if not count:    
        result = db.favorite.insert_one(document)
        if result.acknowledged:
            response = {'result':'success'}
    return jsonify(response)


@app.route('/favorite', methods=['DELETE'])
def remove_favorite():
    pid = request.form['detail_url'].split('/')[-1]
    user_id = request.form['user_id']
    print(pid, user_id)
    result = db.favorite.delete_one({
            'pid': pid, 
            'user_id': user_id
        })
    if result.deleted_count:
        return {'result': 'success'}
    return {'result': 'fail'}

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)