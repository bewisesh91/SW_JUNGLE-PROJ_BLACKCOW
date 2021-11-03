import requests
import json 

MAX_ITEM = 300
LOWER_CONSTANT = 0.5
UPPER_CONSTANT = 1.5

def _filter_items(items, lower, upper, result_str, result_dict):
    '''API를 통해 얻어온 상품 리스트들에서 outlier를 제거하고, 제거된 아이템들의 평균 가격을 구하여 result_dict에 넣어주는 함수.
    
    Args:
        items (list): 상품 정보가 담긴 리스트 
        lower (float): outlier를 제거하기 위해 median으로 부터 lowerbound를 만들기 위한 상수 
        upper (float): outlier를 제거하기 위해 median으로 부터 upperbound를 만들기 위한 상수 
        result_str (str): result_dict의 키값으로 쓰일 중고 플랫폼 스트링
        result_dict (dict): 검색한 결과가 저장되는 dictionary
    
    Returns:
        None
    '''
    items = sorted(items)
    if len(items) == 0:
        median = 0
        result_dict[result_str] = ([], 0)
        return 
    
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


def gather_bunjang(query, result_dict):
    '''번개장터로 부터 query에 대한 검색 결과를 얻어 오는 함수 
    
    Args:
        - query (str): 유저가 검색한 쿼리 스트링
        - result_dict (dict): 검색한 결과가 저장되는 dictionary
    
    Returns:
        None
    '''
    items = []
    max_idx = MAX_ITEM // 30
    for i in range(max_idx):
        bunjang_url = f'https://api.bunjang.co.kr/api/1/find_v2.json?q={query}&order=date&page={i}&stat_device=w&stat_category_required=1&req_ref=search&version=4'
        res = requests.get(bunjang_url.encode('utf-8'))
        raw_items = res.json()['list']
        for item in raw_items:
            price = int(item['price'])
            if price != 0:
                items.append(    
                    (
                        int(item['price']), 
                        item['name'],
                        item['product_image'],
                        item['pid'] # 상세 페이지 
                    )
                )
    _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, 'bunjang', result_dict)
    
        
def gather_joongna(query, result_dict):
    '''중고나라로부터 query에 대한 검색 결과를 얻어 오는 함수 
    
    Args:
        - query (str): 유저가 검색한 쿼리 스트링
        - result_dict (dict): 검색한 결과가 저장되는 dictionary
    
    Returns:
        None
    '''
    
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "searchWord": query,
        "sort": "RECENT_SORT", 
        "searchQuantity": MAX_ITEM
    }

    res = requests.post(url = 'https://search-api.joongna.com/v25/search/product', headers = headers,  data = json.dumps(data))
    raw_items = res.json()['data']['items']
    items = []
    for item in raw_items:
        price = int(item['price'])
        if price != 0:
            items.append(
                (
                    price, 
                    item['title'],
                    item['detailImgUrl'],
                    item['seq'] # 상세 페이지 : https://m.joongna.com/product-detail/28300332
                )
            )
    _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, 'joongna', result_dict)
    

def gather_hellomarket(query, result_dict):
    '''헬로마켓으로부터 query에 대한 검색 결과를 얻어 오는 함수 
    
    Args:
        - query (str): 유저가 검색한 쿼리 스트링
        - result_dict (dict): 검색한 결과가 저장되는 dictionary
    
    Returns:
        None
    '''
    
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.hellomarket.com/api/search/items?q={query}&limit={MAX_ITEM}"
    response = requests.get(url, headers=headers)
    
    raw_items = response.json()['list']
    items = []
    for item in raw_items:
        if not 'item' in item:
            continue
        item = item['item']
        price = int(item['property']['price']['amount'])
        if price != 0:
            items.append(
                (
                    price, 
                    item['title'],
                    item['media']['imageUrl'],
                    item['itemIdx'] # 상세 페이지 : https://www.hellomarket.com/item/172319904
                )
            )    

    _filter_items(items, LOWER_CONSTANT, UPPER_CONSTANT, 'hellomarket', result_dict)
        
if __name__ == '__main__':   
    import threading 
    threads = []
    result_dict = {}
    search_functions = [gather_bunjang, gather_joongna, gather_hellomarket]
    args = ('아이폰', result_dict)
    for fn in search_functions:
        th = threading.Thread(target = fn, args = args)
        threads.append(th)

    for th in threads:
        th.start()
    for th in threads:
        th.join()
    gather_joongna('아이폰', result_dict)
    print(result_dict)
    