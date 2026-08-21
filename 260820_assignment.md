### 문항1. 네이버 연관검색어 수집 함수 만들기
> 키워드를 입력받아 그 키워드의 연관검색어 리스트를 돌려주는 함수를 작성하시오.

- 함수명: `get_related_keywords(keyword)`
- 반환: 문자열 리스트
- Selenium 사용 금지. Network 탭에서 요청을 찾아 `requests`로 재현할 것
- 결과가 없으면 빈 리스트를 돌려줄 것 (예외를 던지지 말 것)
- `힌트.md`에 문서 찾기 힌트, 결과 파싱 힌트 있음

```
# 실행 예시
>>>get_related_keywords('부트캠프')
['부트캠프 뜻', '부트캠프', '부트캠프 추천', '카카오 부트캠프', '맥북 부트캠프',
 '카카오테크 부트캠프', '직무부트캠프', '네이버 부트캠프', '마케팅 부트캠프', '코멘토 직무부트캠프']
```

```py
# 답안
import requests

def get_related_keywords(keyword):

    URL = 'https://ac.search.naver.com/nx/ac'

    params = {
        'q': keyword,
        'con': '1',
        'frm': 'nv',
        'ans': '2',
        'r_format': 'json',
        'r_enc': 'UTF-8',
        'r_unicode': '0',
        't_koreng': '1',
        'run': '2',
        'rev': '4',
        'q_enc': 'UTF-8',
        'st': '100',
        'ackey': 'qb0mja81',
        '_callback': '_jsonp_4'
    }

    res = requests.get(URL, params=params)

    # print(res.text)
    # '_jsonp_4({\n"query" : ["부트캠프"],\n"answer" : [],\n"intend" : [],\n"items" : [\n ... 트캠프", "0"]]\n]\n})

    text = res.text
    text = text[9:-1]

    # print(text)

    import json

    data = json.loads(text)

    # type(data) -> dict

    items = data['items'][0]
    # items[0] # ['부트캠프', '0']
    # items[0][0] # '부트캠프'

    if not items:
        return []

    result = []
    for item in items:
        result.append(item[0])

    return result

print(get_related_keywords('부트캠프'))
```

### 문항2. 네이버 웹툰 전체 목록 수집
> 네이버 웹툰의 요일별 전체 웹툰을 수집하시오.

- 대상: https://comic.naver.com/webtoon
- 추출 필드: 제목 / 링크 / 요일
- 모든 요일의 웹툰을 수집할 것
- 링크는 상세 페이지로 바로 이동할 수 있는 절대 주소로 만들 것 (힌트 1)
- 결과를 naver_webtoon.csv로 저장할 것

```
# 결과예시
[{'제목': '광마회귀', '링크': 'https://comic.naver.com/webtoon/list?titleId=776601', '요일': '금'},
 {'제목': '외모지상주의', '링크': 'https://comic.naver.com/webtoon/list?titleId=641253', '요일': '금'},
 ...]
```

```py
# 답안
import requests

URL = 'https://comic.naver.com/api/webtoon/titlelist/weekday'

params = {
    'order': 'user'
}

res = requests.get(URL, params=params)

# res.status_code
# res.text
data = res.json()
data.keys() # dict_keys(['titleListMap', 'dayOfWeek'])

# data['titleListMap']['MONDAY'][0]
# data['dayOfWeek'] # 'FRIDAY'
data['titleListMap'].keys()

result = []

day_map = {
    'MONDAY': '월',
    'TUESDAY': '화',
    'WEDNESDAY': '수',
    'THURSDAY': '목',
    'FRIDAY': '금',
    'SATURDAY': '토',
    'SUNDAY': '일',
}

for day in data['titleListMap']:
    # print(day)
    for title in data['titleListMap'][day]:
    #     print(title['titleName'])
    #     print(title['titleId'])
    #     print(day)
    #     break
    # break

        item = {
            '제목': title['titleName'],
            '링크': f'https://comic.naver.com/webtoon/list?titleId={title['titleId']}',
            '요일': day_map[day]
        }

        result.append(item)

len(result)

import pandas as pd

df = pd.DataFrame(result)
df.to_csv('naver_webtoon.csv', index=False, encoding='utf-8-sig')
```

### 문항3. 사람인 채용공고 10페이지 수집
> 사람인의 공개 채용공고 목록을 10페이지 수집하시오.

- 대상: https://www.saramin.co.kr/zf_user/jobs/public/list
- 추출 필드: 기업명 / 그룹사 / 기업종류 / 공고명 / 직무키워드 / 학력 / 경력구분 / 근무지
- 직무키워드는 리스트로 담을 것
- 값이 없는 항목은 빈 문자열 또는 빈 리스트로 둘 것 (오류로 멈추지 말 것)
- 요청 간 0.5초 이상 지연을 둘 것
- 결과를 saramin.csv로 저장할 것

```
# 결과예시
[{'기업명': '(주)유니드',
  '그룹사': '오씨아이그룹',
  '기업종류': '대기업',
  '공고명': '2025년 유니드 상반기 신입사원 수시채용',
  '직무키워드': ['외환관리', '자금관리', '자산운용', '재무제표', '재무회계'],
  '학력': '대학교(4년)↑',
  '경력구분': '신입 · 정규직',
  '근무지': '서울 중구 외'},
 ...]
```

```py
# 답안
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

URL = 'https://www.saramin.co.kr/zf_user/jobs/public/list'

headers = {
    'user-agent': 'Mozilla/5.0'
}

results = []

for page in range(1, 11):

    params = {
        'page': page,
        'isAjaxRequest': 'y',
    }

    res = requests.get(URL, params=params, headers=headers)

    # print(res.status_code) #200
    # res.text[:1000]

    soup = BeautifulSoup(res.text, 'html.parser')

    # soup.find_all('a')[:10]
    # soup.get_text()[:2000]

    items = soup.select('.list_item')

    # len(items) # 20개의 공고

    for item in items:

        # 기업명
        name_tag = item.select_one('.company_nm .str_tit')
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = ''

        # 그룹사
        group_tag = item.select_one('.company_nm .main_corp')
        if group_tag:
            group = group_tag.text.strip()
        else:
            group = ''

        # 기업종류
        stock_tag = item.select_one('.company_nm .info_stock')
        if stock_tag:
            stock = stock_tag.text.strip()
        else:
            stock = ''

        # 공고명
        job_tag = item.select_one('.job_tit .str_tit')
        if job_tag:
            job = job_tag.text.strip()
        else:
            job = ''

        # 직무키워드
        keywords = []

        for keyword in item.select('.job_sector span'):
            keywords.append(keyword.text.strip())

        # keywords

        # 학력
        education_tag = item.select_one('.education')
        if education_tag:
            education = education_tag.text.strip()
        else:
            education = ''
        # 경력구분
        career_tag = item.select_one('.career')
        if career_tag:
            career = career_tag.text.strip()
        else:
            career = ''
        # 근무지
        place_tag = item.select_one('.work_place')
        if place_tag:
            place = place_tag.text.strip()
        else:
            place = ''

        result = {
            '기업명': name,
            '그룹사': group,
            '기업종류': stock,
            '공고명': job,
            '직무키워드': keywords,
            '학력': education,
            '경력구분': career,
            '근무지': place,
        }

        results.append(result)

    time.sleep(0.5)

len(results) # 200

df = pd.DataFrame(results)
df.to_csv('saramin.csv', index=False, encoding='utf-8-sig')
```