import requests
# from flask import Flask, render_template, jsonify, request
# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
MAX_ITEM = 300
MAX_IDX = MAX_ITEM // 60 
LOWER_CONSTANT = 0.3
UPPER_CONSTANT = 2
result_dict = {}
def _filter_items(items, lower, upper, result_str):
    items = sorted(items)
    mid = len(items) // 2
    median = items[mid][0]

    filtered_item = []
    sum = 0
    for item in items:
        lower_bound = median * lower
        upper_bound = median * upper
        if lower_bound < item[0] < upper_bound:
            filtered_item.append(item)
            sum += item[0]
    result_dict[result_str] = (filtered_item, sum / len(filtered_item))

def gather_bunjang(query):
    items = []
    for i in range(MAX_IDX):
        bunjang_url = f'https://api.bunjang.co.kr/api/1/find_v2.json?q={query}&order=date&page={i}&stat_device=w&stat_category_required=1&req_ref=search&version=4'
        res = requests.get(bunjang_url)
        raw_items = res.json()['list']
        for item in raw_items:
            items.append(
                (
                    int(item['price']), 
                    item['name'],
                    item['product_image'],
                    item['pid'] # 상세 페이지 
                )
            )
    _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, 'bunjang')
    # return _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, result_str)

        
def gather_joongna(query):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = '{"searchWord": "%s","sort": "RECENT_SORT", "searchQuantity":%d}'%(query, MAX_ITEM)
    res = requests.post(url = 'https://search-api.joongna.com/v25/search/product', headers = headers,  data = data.encode("utf-8"))
    raw_items = res.json()['data']['items']
    items = []
    for item in raw_items:
        items.append(
                (
                    int(item['price']), 
                    item['title'],
                    item['detailImgUrl'],
                    item['seq'] # 상세 페이지 : https://m.joongna.com/product-detail/28300332
                )
            )
    _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, 'joongna')
    # return _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, result_str)

if __name__ == '__main__':    
    import time
    import threading
    threads = []
    search_functions = [gather_bunjang, gather_joongna, gather_bunjang, gather_joongna]
    args = ('맥북',)
    for fn in search_functions:
        th = threading.Thread(target = fn, args = args)
        threads.append(th)
    start_time = time.time()
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    # print('threading', time.time() - start_time)
    # start_time = time.time()
    # gather_bunjang('맥북')
    # gather_joongna('맥북')
    # gather_bunjang('맥북')
    # gather_joongna('맥북')
    # print('sequential', time.time() - start_time)
    
