### 문항1. 금융위 주식시세정보 API 호출과 오류 처리
> 공공데이터포털에서 발급받은 서비스키로 금융위원회 주식시세정보 API를 호출하시오.

- 대상: `https://www.data.go.kr/data/15094808/openapi.do`
- 서비스키는 `.env`로 분리하고, `.gitignore`에 `.env`를 추가할 것
- 코드에 키를 하드코딩하지 않고 불러와 사용할 것
- 삼성전자(`005930`) 최근 5영업일 시세를 조회해 JSON을 dict로 파싱할 것
- 다음 세 가지 오류 상황을 각각 구분해 처리할 것
    - 인증키 오류 (`SERVICE_KEY_IS_NOT_REGISTERED_ERROR`)
    - 일일 쿼터 초과 (`LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR`)
    - 필수 파라미터 누락 (`INVALID_REQUEST_PARAMETER_ERROR`)
- `.env.example` 파일을 함께 제출할 것 (키 값은 비울 것)

```py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

BASE_URL = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo'


class OpenAPIKeyError(Exception): ...
class OpenAPIQuotaError(Exception): ...
class OpenAPIParameterError(Exception): ...
class OpenAPIError(Exception): ...

def fetch_stock(stock_code='005930', page=1, size=5):

    params = {
        'serviceKey': OPEN_API_KEY,
        'resultType': 'json',
        'numOfRows': size,
        'pageNo': page,
        'likeSrtnCd': stock_code
    }

    res = requests.get(BASE_URL, params=params)
    res.raise_for_status()
    
    data = res.json()

    # print(data.keys()) # dict_keys(['response'])
    # print(data['response'].keys()) # dict_keys(['header', 'body'])
    # print(data['response']['body'].keys()) # dict_keys(['numOfRows', 'pageNo', 'totalCount', 'items'])

    # 1. API 에러 처리
    if data.get('OpenAPI_ServiceResponse'):
        msg = data.get('OpenAPI_ServiceResponse')['cmmMsgHeader']['errMsg']

        if msg == 'SERVICE_KEY_IS_NOT_REGISTERED_ERROR':
            raise OpenAPIKeyError(msg)
        elif msg == 'LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR':
            raise OpenAPIQuotaError(msg)
        elif msg == 'INVALID_REQUEST_PARAMETER_ERROR':
            raise OpenAPIParameterError(msg)

    # 2. 그 외의 에러 처리
    if data['response']['header']['resultCode'] != '00':
        msg = data['response']['header']['resultMsg']
        raise OpenAPIError(msg)

    return data

data = fetch_stock()

# items = data['response']['body']['items']

# print(items)

stock_data = data['response']['body']['items']['item']

# print(stock_data)

print(stock_data[0]['itmsNm'])
print(stock_data[0]['basDt'])
print(stock_data[0]['clpr'])
```

### 문항2. DB 스키마 설계와 적재 검증
> 수집한 원본을 보관할 테이블을 만들고, 가공 없이 적재하시오. (과제1의 코드를 활용하여 진행)

1. MariaDB에 `fsc_db` 데이터베이스를 만들고 전용 계정으로 접속할 것
2. 테이블 `raw_item`을 다음 컬럼으로 생성할 것 `raw_id` / `source` / `url` / `collected_at` / `payload` / `content_hash`
    - `content_hash`에 UNIQUE 제약
    - `(source, collected_at)` 복합 인덱스 설정
3. 다음 10개 종목의 최근 2025년 주식 시세를 수집하여 `source='fsc_api'` 로, 원문 JSON 그대로 `payload`에 적재할 것
```
CODES = ["005930", "000660", "035420", "051910", "005380",
         "006400", "035720", "068270", "105560", "055550"]
```
4. `executemany` 배치 삽입 + `ON DUPLICATE KEY UPDATE` 를 쓸 것
5. 같은 스크립트를 두 번 실행하고, 행 수가 변하지 않음을 SQL로 확인할 것
6. DB 비밀번호도 `.env`로 관리할 것
```
# 참고용 해싱 코드

import hashlib

key_src = '해싱하여 중복되는 값이 들어올 경우 UNIQUE 제약조건을 발생시킬 문자열'
# 예시) fsc_api|20250101|005930
# 수집소스|날짜|주식코드를 해싱하여 같은 값이 또 들어올 경우 Duplicate 처리
hashlib.sha256(key_src.encode()).hexdigest()
```

```py
import json
import os
import hashlib
from datetime import datetime

import pymysql
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

conn = pymysql.connect(
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

CODES = ["005930", "000660", "035420", "051910", "005380", "006400", "035720", "068270", "105560", "055550"]

results = []

for code in CODES:
    data = fetch_stock(
        stock_code=code, 
        page=1, 
        size=300
    )

    results.append((code, data))

insert_data = []

for code, data in results:
    source = 'fsc_api'
    url = BASE_URL
    collected_at = datetime.now()

    payload = json.dumps(data, ensure_ascii=False)

    key_src = f'fsc_api|2025|{code}'
    content_hash = hashlib.sha256(
        key_src.encode()
    ).hexdigest()

    insert_data.append((
        source,
        url,
        collected_at,
        payload,
        content_hash
    ))

sql = """
INSERT INTO raw_item
    (source, url, collected_at, payload, content_hash)
VALUES
    (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    collected_at = VALUES(collected_at),
    payload = VALUES(payload)
"""

cursor = conn.cursor()

cursor.executemany(sql, insert_data)

conn.commit()

cursor.close()
conn.close()
```