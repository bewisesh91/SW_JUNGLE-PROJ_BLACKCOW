# Project BlackCow
## 기획 의도 
- 커져가는 중고 시장, 다양한 중고 거래 서비스들의 등장 
- **"흑우"** 를 피하기 위한 합리적인 중고가격 제시 플랫폼

## 기술 스택 
### Client
- HTML + Jinja2 Template Engine
- CSS + Bulma
- Javascript + jQuery
### Server
- python3 + Flask
### Database
- MongoDB

## requirements
- certifi               2021.10.8
- idna                  3.3
- requests              2.26.0
- urllib3               1.26.7
- charset-normalizer    2.0.7
- autopep8              1.6.0
- click                 8.0.3
- Flask                 2.0.2
- Flask-JWT             0.3.2
- itsdangerous          2.0.1
- Jinja2                3.0.2
- MarkupSafe            2.0.1
- pycodestyle           2.8.0
- PyJWT                 1.4.2
- pymongo               3.12.1
- toml                  0.10.2
- Werkzeug              2.0.2
 
## 구현 상세 
### 와이어프레임 
- use figma
- 링크: 
    - https://www.figma.com/file/nD75qTSuVZUPFrK1Q5MCp0/00%EC%A3%BC%EC%B0%A8-1%EC%A1%B0?node-id=0%3A1
### signup
- How to keep user data secure?
    - hash function을 통한 데이터 암호화 
- How to create a strong password?
    - string pattern analysis using regular expression & guide to use strong password
- Avoid duplicated subscription
### signin & signout
- How to enable user authentication? 
    - JWT
- How to use token securely? 
    - token expiration
### search
- How to collect used item price? 
    - search API used by each services
- How to make collecting data fast?
    - threading(multi thread module)
- How to deal with invalid access through url? 
    - using error handler decorator
- How to decide reasonable price? 
    - removing outliers
### signature
- How to accumulate user specific data? 
    - efficient data management
 
## API Document
### 상품 관련 정보 얻어오기 
- url: /products
- method: GET
- params: 
    - q: 유저 검색어 정보 
- response:
```Javascript
response = {
    "result": 'success' or 'fail', // 상태값
    "total_average": 0, // 전체 평균
    "bunjang":{ // 번개 장터 상품 정보 
        "counts": 0, // 전체 개수 
        "average":0, // 평균
        "percentage":0, // 전체 평균 대비 
    },
    "joongna":{ // 중고나라 상품 정보 
        "counts": 0, 
        "average":0,
        "percentage":0,
    },
    "hellomarket":{ // 헬로마켓 상품 정보 
        "counts": 0,
        "average":0,
        "percentage":0,
    },
}
``` 

### 상품 관련 상세 정보 얻어오기 
- url: /details
- method: GET
- params: 
    - c: 유저가 선택한 상세페이지 회사 스트링 
- response: 
    ```javascript
    response = {
        "items":[
            {
                "title": "",
                "price": 0,
                "imageUrl": "",
                "productPageUrl": "",
                "percentage": 0,
                "isFavorite": true
            }, 
            ...
        ]
    }
    ```

### 즐겨찾기 추가 
- 좋아요 버튼 눌렀을때 favorites 테이블에 아이템 추가 
- url: /favorite
- method: POST
- data: 
    - title: 상품페이지 제목
    - image_url: 상품 이미지 url 
    - price: 상품 가격 
    - detail_url: 상품 상세페이지 url 
    - company: 플랫폼 정보
        - ⭐️ 'joongna', 'bunjang', 'hellomarket' 중 하나의 값
- response:
    - result: success 또는 fail

### 즐겨찾기 제거 
- 좋아요 버튼 다시 눌렀을때 favorites 테이블에서 아이템 제거 
- url: /favorite
- method: DELETE
- data: 
    - detail_url: 상품 상세페이지 url 
- response: 
    - result: success 또는 fail
        
### 회원가입 
- 초기 진입 페이지에서 회원가입 버튼 클릭시 회원가입 페이지로 이동 
- url: /sign_up
- method: POST
- data: 
    - username : 유저 이름
    - password : 유저 패스워드
    - email : 유저 이메일
- response: 
    - result: success 또는 fail
  
### 로그인 
- 초기 진입 페이지에서 로그인 버튼 클릭시 로그인 페이지로 이동 
- url: /sign_in
- method: POST
- data: 
    - email : 유저 이메일
    - password : 유저 패스워드
- response: 
    - result: success 또는 fail
    - token: 유저 토큰
