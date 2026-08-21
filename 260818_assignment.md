### 문항1. 할리스커피 매장 정보 10페이지 수집
> 할리스커피 매장 찾기 페이지에서 매장 정보를 수집해 리스트-딕셔너리 형태로 정리하시오.

- 대상: https://www.hollys.co.kr/store/korea/korStore2.do
- 총 10페이지를 순회할 것 (페이지를 넘기며 URL이 바뀌는 것을 확인)
- 추출 필드: 지역 / 매장명 / 현황 / 주소 / 매장 서비스 / 전화번호
- 매장 서비스는 리스트로 담을 것 (아이콘이 여러 개인 매장이 있음)
- 결과를 hollys.csv로 저장할 것
```
# 결과 예시
[{'지역': '서울 동대문구',
  '매장명': '경희대 경영대점',
  '현황': '영업중',
  '주소': '서울특별시 동대문구 경희대로 26 (회기동) 경영대학 3층',
  '매장 서비스': ['주차'],
  '전화번호': '.'},
 ...]
```

```py
# 답안
import requests
from bs4 import BeautifulSoup

URL = 'https://www.hollys.co.kr/store/korea/korStore2.do'

result = []

for page in range(1, 11):

    params = {
        'sido': '',
        'gugun': '',
        'store': '',
        'pageNo': page
    }


    res = requests.get(URL, params=params)
    res.status_code

    # print(res.text)

    soup = BeautifulSoup(res.text, 'html.parser')

    # soup.title

    trs = soup.select('table tr')

    # len(trs)

    tds = trs[6].select('td')
    services = tds[4].select('img')

    for tr in trs[1:]:
        tds = tr.select('td')
        services = tds[4].select('img')
        service_list = []

        for service in services:
            service_list.append(service.attrs['alt'])

        data = {
        '지역': tds[0].text.strip(),
        '매장명': tds[1].text.strip(),
        '현황': tds[2].text.strip(),
        '주소': tds[3].text.strip(),
        '매장 서비스': service_list,
        '전화번호': tds[5].text.strip(),
        }
        result.append(data)

result

# len(result) # 100

import pandas as pd

df = pd.DataFrame(result)

# df.head()

df.to_csv('hollys.csv', index=False)
```

### 문항2. 알라딘 베스트셀러 수집
> 알라딘 베스트셀러 페이지에서 도서 정보를 수집해 CSV로 저장하시오.

- 대상: 알라딘 베스트셀러 목록 페이지(https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1)
- 추출 필드: 카테고리 / 제목 / 저자 / 할인가격 / 이미지 URL
- 이미지 URL은 <img> 태그의 속성에서 가져올 것
- 결과를 aladin_bestseller.csv로 저장할 것
- 추가학습: 총 500위까지 수집해주세요.

```
# 결과예시
[{'카테고리': '[국내도서]',
  '제목': '오뒷세이아',
  '저자': '호메로스',
  '정가': '25,000원',
  '할인가격': '22,500원',
  '이미지': '<https://image.aladin.co.kr/product/39940/12/cover200/8932476462_2.jpg>'},
 ...]
```

```py
# 답안


```