## API
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
    - user_token: 유저 토큰
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
    - user_token: 유저 토큰
- response: 
    - result: success 또는 fail

### 마이페이지 요청 
- 마이페이지를 그리기 위한 정보 요청 
- url: /mypage
- method: GET
- response:
    - result: success 또는 fail
    - counts: 전체 상품 개수 
    - items: 유저가 좋아요 누른 아이템 목록 
        - 상품 각각의 정보 
        ```javascript
            {
                "title": "", // 상품명
                "price": 0, // 가격
                "imageUrl": "", // 이미지 url
                "company": "", // 플랫폼 정보 스트링
                "productPageUrl": "", // 상품 상세 페이지 url 
            } 
        ```
        
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
