def _generate_product_response(result_dict, user_favorites_pid):
    detail_base_url = {
        'bunjang': 'https://m.bunjang.co.kr/products/{{PID}}',
        'joongna': 'https://m.joongna.com/product-detail/{{PID}}',
        'hellomarket': 'https://www.hellomarket.com/item/{{PID}}'
    }
    response = {
        'status': 200, 
        'total_average': 0,
        'averages': {
            'bunjang':{
                'average':0,
                'percentage':0
            },
            'joongna':{
                'average':0,
                'percentage':0
            },
            'hellomarket':{
                'average':0,
                'percentage':0
            }
        },
        'items': {
            'bunjang':{
                'counts': 0,
                'items':[{
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0
                }],
            },
            'joongna':{
                'counts': 0,
                'items':[{
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0
                }]
            },
            'hellomarket':{
                'counts': 0,
                'items':[{
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0
                }]
            },
        }
    }
    total_average = 0 
    total_count = 0
    for company in result_dict:
        items_list, company_avg = result_dict[company]
        company_count = len(items_list)
        total_average += company_count * company_avg
        total_count += company_count
        response['averages'][company]['average'] = company_avg
        response['items'][company]['counts'] = company_count
        company_items = []
        for item in items_list:
            an_item = {}
            an_item['title'] = item[1]
            an_item['imageUrl'] = item[2]
            an_item['price'] = item[0]
            an_item['productPageUrl'] = detail_base_url[company].replace('{{PID}}', str(item[3]))
            an_item['percentage'] = (item[0] - company_avg) / company_avg * 100 
            an_item['isFavorite'] = True if str(item[3]) in user_favorites_pid else False
            company_items.append(an_item)
        response['items'][company]['items'] = company_items 

    response['total_average'] = total_average / total_count
    for company in result_dict:
        if response['items'][company]['counts'] != 0:
            response['averages'][company]['percentage'] = (response['averages'][company]['average'] - response['total_average']) / response['total_average'] * 100 
        else:
            response['averages'][company]['percentage'] = 0
    return response
