### 문항1. 무신사 상품 10페이지
> 무신사 상품 페이지에서 상의 카테고리 제품을 10페이지 크롤링해주세요.

- 대상: `https://www.musinsa.com/category/001/goods?gf=A`
- 추출 필드: 브랜드명 / 제품명 / 원래가격 / 할인가격 / 리뷰 수 / 리뷰 점수
- `Selenium` 혹은 `requests`로 수집
- Selenium으로 수집 시
    - `time.sleep()`으로 요소를 기다리지 말 것. `WebDriverWait` + `expected_conditions`를 사용할 것
    - headless 모드로 실행하고 창 크기를 명시할 것
    - `try / finally`로 드라이버가 반드시 종료되게 할 것
- 결과를 `musinsa.csv`로 저장할 것

```
# 기대 결과
[{'브랜드명': '생로랑', '제품명': '클래식 반소매 티셔츠 - 블랙 / 801474YB2FT1000',
  '원래가격': 838000, '할인가격': 105990, '리뷰수': 1, '리뷰점수': 100},
 {'브랜드명': '108파운드', '제품명': 'Days Comfort Fit Shirt_White',
  '원래가격': 89000, '할인가격': 76100, '리뷰수': 0, '리뷰점수': 0}, ...]
```

```py
# 답안
import requests
from bs4 import BeautifulSoup

URL = 'https://api.musinsa.com/api2/dp/v2/plp/goods'

params = {
    'gf': 'A',
    'sortCode': 'POPULAR',
    'category': '001',
    'size': '60',
    'caller': 'CATEGORY',
    'seen': '121'
}

res = requests.get(URL, params={**params, 'page': 1})
data = res.json()

results = []

# 1페이지
for item in data['data']['list']:
    results.append({
        '브랜드명': item['brandName'],
        '제품명': item['goodsName'],
        '원래가격': item['normalPrice'],
        '할인가격': item['finalPrice'],
        '리뷰 수': item['reviewCount'],
        '리뷰 점수': item['reviewScore'],
    })

# # 2페이지
# next_url = data['data']['pagination']['nextPageUrl']
# res2 = requests.get(next_url)
# data2 = res2.json()

# len(data2['data']['list']) # 60

# # 3페이지
# next_url = data2['data']['pagination']['nextPageUrl']
# res3 = requests.get(next_url)
# data3 = res3.json()

# len(data3['data']['list']) # 60

# 2~10페이지 반복
next_url = data['data']['pagination']['nextPageUrl']

for page in range(2, 11):
    res = requests.get(next_url)
    data = res.json()
    
    for item in data['data']['list']:
        results.append({
            '브랜드명': item['brandName'],
            '제품명': item['goodsName'],
            '원래가격': item['normalPrice'],
            '할인가격': item['finalPrice'],
            '리뷰 수': item['reviewCount'],
            '리뷰 점수': item['reviewScore'],
        })

    next_url = data['data']['pagination']['nextPageUrl']

len(results)

import pandas as pd

df = pd.DataFrame(results)
df.to_csv('musinsa.csv', index=False, encoding='utf-8-sig')
```
