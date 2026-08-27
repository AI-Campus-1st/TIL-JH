### 문항1. 아실 아파트 목록, 매물 크롤링
> 요구사항 1. 아실 사이트에서 수집을 두 단계로 분리해 작성하시오.

- 대상: `https://asil.kr/asil/index.jsp`
- 1단계 `collect_apt.py` — 행정동 별로 아파트 목록을 모아 `apts.csv`로 저장
- 2단계 `collect_forsale.py` — `apts.csv`를 읽어 매물 페이지를 수집해 `forsales.csv`로 저장 (status를 최신화, `done`, `failed`)
- `apts.csv`는 다음 컬럼을 가질 것: `seq`, `status`, `collected_at` +a (상세칼럼들)
- `status`의 초기값은 `pending`
- 요청 간 0.5초 이상 지연

> 요구사항 2. 재시도 & 로깅 & 실패 큐 처리 로직 적용

- 재시도 — 지수 백오프. 재시도 대상은 Timeout·ConnectionError·429·5xx로 한정하고, 404·400은 즉시 포기할 것
- 로깅 — `print` 대신 `logging`. 파일과 화면에 동시 출력, INFO/WARNING/ERROR 구분
- 실패 큐 — 실패한 seq을 오류 유형과 함께 `failed_apt.csv, failed_forsale.csv` 각각 분리하여 저장
- 통계 — 종료 시 성공 / 실패 / 건너뜀 건수를 한 줄로 출력
- 검증 — 큐의 URL 중 일부를 존재하지 않는 주소로 바꿔 넣고, 크롤러가 죽지 않고 끝까지 도는지 확인할 것

```py
# 답안
# 1단계 collect_apy.py

import requests
import pandas as pd
from datetime import datetime
import time

URL = 'https://asil.kr/app/data/data_apt_list.jsp'

def get_apartments(dong):

    params = {
    'building': '',
    'household': '50',
    'order': '0',
    'order_type': '0',
    'dong': dong,
    }

    headers = {
        'user-agent': 'Mozilla/5.0',
        'referer': 'http://asil.kr/app/apt_list.jsp'
    }

    res = requests.get(URL, params=params, headers=headers)

    # print(res.status_code)
    # print(repr(res.text))

    data = res.json()

    return data

# dong = '1168010300'

DONG_CODES = [
    '1174010600',
    '1174010900',
    '1174011000'
]

results = []

for dong in DONG_CODES:
    
    data = get_apartments(dong)

    for apt in data:
        result = {
            'seq': apt['seq'],
            'status': 'pending',
            'collected_at': datetime.now(),
            'building': apt['building'],
            'name': apt['name'],
            'dong': apt['dong'],
            'dongname': apt['dongname'],
            'bungi': apt['bungi'],
            'movein': apt['movein'],
            'household': apt['household'],
            'total_dong': apt['total_dong'],
            'type': apt['type'],
            'etc': apt['etc'],
            'offer': apt['offer'],
            'lat': apt['lat'],
            'lng': apt['lng']
        }

        results.append(result)

    time.sleep(0.5)

len(results) # 53

df = pd.DataFrame(results)
'df.to_csv('apts.csv', index=False, encoding='utf-8-sig')


# 2단계 collect_forsale.py

import requests
import pandas as pd

URL = 'https://realty.asil.kr/api_asil/data_sale_of_apt_nomal.aspx'

df = pd.read_csv('apts.csv', dtype=str)

seq = df.loc[0, 'seq']

params = {
    'asil_bldcode': seq,
    'focus_bldcode': seq,
    'oidx': '2',
    'oby': 'down',
    'total': '20',
    'last_mm_num': '0',
}

headers = {
    'user-agent': 'Mozilla/5.0',
    'referer': 'https://asil.kr/app/apt_list.jsp'
}

res = requests.post(URL, data=params, headers=headers)

print(res.status_code)

data = res.json()

data
```
