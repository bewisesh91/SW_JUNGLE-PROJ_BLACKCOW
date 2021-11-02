## API
### 상품 관련 정보 얻어오기 
- url: /products
- method: POST
- data: 
    - user_query: 유저 검색어 정보 
    - user_id: 유저 아이디
- response:
```Javascript
response = {
    'status': 200, // 상태 코드
    'total_average': 0, // 전체 평균
    'averages': { // 평균 정보 
        'bunjang':{ // 번개장터 평균 & 전체 평균 대비 퍼센트
            'average':0,
            'percentage':0
        },
        'joongna':{ // 중고나라 평균 & 전체 평균 대비 퍼센트
            'average':0,
            'percentage':0
        },
        'hellomarket':{ // 헬로마켓 평균 & 전체 평균 대비 퍼센트
            'average':0,
            'percentage':0
        }
    },
    'items': { // 상품 정보 
        'bunjang':{ // 번개 장터 상품 정보 
            'counts': 0, // 전체 개수 
            'items':[ // 상품 정보 
                {
                    'title': '', // 상품명
                    'price': 0, // 가격
                    'imageUrl': '', // 이미지 url
                    'productPageUrl': '', // 상품 상세 페이지 url 
                    'percentage': 0, // 평균 가격 대비 
                    "isFavorite": true // 즐겨찾기 여부 
                }, 
                ...
            ]
        },
        'joongna':{ // 중고나라 상품 정보 
            'counts': 0, 
            'items':[ 
                {
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0,
                    "isFavorite": true,
                }, 
                ...
            ]
        },
        'hellomarket':{ // 헬로마켓 상품 정보 
            'counts': 0,
            'items':[
                {
                    'title': '',
                    'price': 0,
                    'imageUrl': '',
                    'productPageUrl': '',
                    'percentage': 0,
                    "isFavorite": true
                }, 
                 ...
            ]
        },
    }
}
``` 
