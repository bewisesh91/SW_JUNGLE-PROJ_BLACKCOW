import threading
from gather_items import gather_hellomarket, gather_bunjang, gather_joongna
from utils import _generate_product_response
from pymongo import MongoClient
from flask import Flask, request, jsonify

client = MongoClient('localhost', 27017)
db = client.db_blackcow

app = Flask(__name__)

@app.route('/products', methods=['POST'])
def get_products():
    query = request.form['user_query']
    user_id = str(request.form['user_id'])
    user_favorites = db.favorites.find({"user_id": user_id})
    user_favorites_pid = set()
    for user_favorite in user_favorites:
        user_favorites_pid.add(user_favorite['pid'])

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

    response = _generate_product_response(result_dict, user_favorites_pid)
    return jsonify(response)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)