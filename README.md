## API
### 상품 관련 정보 얻어오기 
- url: /products
- method: POST
- data: user_query
- response:
```Javascript
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
            'items':[
                {
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0
                }, 
                ...
            ]
        },
        'joongna':{
            'counts': 0,
            'items':[
                {
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0
                }, 
                ...
            ]
        },
        'hellomarket':{
            'counts': 0,
            'items':[
                {
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0
                }, 
                 ...
            ]
        },
    }
}

``` 
