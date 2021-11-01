import requests
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
MAX_ITEM = 300
MAX_IDX = MAX_ITEM // 60 
LOWER_CONSTANT = 0.3
UPPER_CONSTANT = 2

def gather_bunjang(query):
    items = []
    for i in range(MAX_IDX):
        bunjang_url = f'https://api.bunjang.co.kr/api/1/find_v2.json?q={query}&order=date&page={i}&stat_device=w&stat_category_required=1&req_ref=search&version=4'
        res = requests.get(bunjang_url)
        for item in res.json()['list']:
            items.append(
                (
                    int(item['price']), 
                    item['name'],
                    item['product_image'],
                    item['pid'] # 상세 페이지 
                )
            )
    items = sorted(items)
    mid = len(items) // 2
    median = items[mid][0]
    filtered_item = []
    sum = 0
    for item in items:
        lower_bound = median * LOWER_CONSTANT
        upper_bound = median * UPPER_CONSTANT
        if lower_bound < item[0] < upper_bound:
            filtered_item.append(item)
            sum += item[0]
    return filtered_item, sum / len(filtered_item)
filtered_item, avg = gather_bunjang('맥북')
print(filtered_item)
print(avg)

        