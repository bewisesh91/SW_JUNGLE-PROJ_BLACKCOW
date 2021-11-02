# API 사용법 

## 즐겨찾기 추가 
- 좋아요 버튼 눌렀을때 favorites 테이블에 아이템 추가 
- url: /favorite
- method: POST
- data: 
    - title: 상품페이지 제목
    - image_url: 상품 이미지 url 
    - price: 상품 가격 
    - detail_url: 상품 상세페이지 url 
    - user_id: User ID
- response:
    - result: success 또는 fail

## 즐겨찾기 제거 
- 좋아요 버튼 다시 눌렀을때 favorites 테이블에서 아이템 제거 
- url: /favorite
- method: DELETE
- data: 
    - detail_url: 상품 상세페이지 url 
    - user_id: User ID 
- response: 
    - result: success 또는 fail

