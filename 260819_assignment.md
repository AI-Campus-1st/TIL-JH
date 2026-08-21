### 문항1. 뒤죽박죽인 날짜 표기를 하나로 통일하기
> 여러 사이트에서 긁어온 날짜 문자열이 제각각이다. 이를 YYYY-MM-DD 하나로 통일하는 함수를 작성하시오.
```
samples = [
    "2024.12.24",          "2024-12-24",        "2024/12/24",
    "24.12.24",            "2024년 12월 24일",   "2024년 3월 5일",
    "12/24/2024",          "2024.12.24 14:30",  "등록일 : 2024.12.24",
    "2024-13-45",          "작성일 없음",         "",
]
```
조건
1. `normalize_date(s) -> str | None` 함수를 작성할 것
2. 위 12가지를 모두 처리할 것 — 변환 불가능하면 `None`
3. 두 자리 연도(`24.12.24`)는 `2024`로 해석할 것
4. 월·일이 한 자리인 경우(`3월 5일`)도 `03, 05`로 채울 것
5. 존재하지 않는 날짜(`2024-13-45`)는 `None`으로 처리할 것 — 정규표현식만으론 거를 수 없음. 후처리할 것
6. `12/24/2024`(미국식)와 `2024/12/24`를 구분할 것
7. 각 입력에 대해 어떤 패턴으로 매치됐는지 함께 출력할 것 (기대결과 부분 확인)

※ 매칭된 것을 변수로써 꺼내는 방법 (명명 그룹)  
(`?P<변수명>정규표현식`)
```
pattern = re.compile(r"(?P<loc>\d{3,4})\-(?P<mid>\d{3,4})\-(?P<last>\d{4})")
m = pattern.search('031-555-3331')
print(m['loc'])
# 031
```

```
# 결과 예시
2024.12.24            → 2024-12-24   [ymd_dot]
24.12.24              → 2024-12-24   [ymd_short]
2024년 3월 5일         → 2024-03-05   [ymd_kor]
12/24/2024            → 2024-12-24   [mdy_slash]
2024-13-45            → None         [ymd_dash · 유효하지 않은 날짜]
작성일 없음            → None         [매치 없음]
""                   → None         [빈 값]
```

```py
# 답안
import re
import datetime

def normalize_date(s):

    if not s or not str(s).strip():
        return (None, '빈 값')

    pattern = re.compile(
        r"(?P<year>\d{4})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})"
    )

    m = pattern.search(s)

    if m:
        pattern_name = 'ymd_dot'

    if not m:
        pattern = re.compile(
            r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
        )
        m = pattern.search(s)

        if m:
            pattern_name = 'ymd_dash'

        if not m:
            pattern = re.compile(
                r"(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})"
            )
            m = pattern.search(s)

            if m:
                pattern_name = 'ymd_slash'

            if not m:
                pattern = re.compile(
                    r"(?P<year>\d{2})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})"
                )
                m = pattern.search(s)

                if m:
                    pattern_name = 'ymd_short'

                if not m:
                    pattern = re.compile(
                        r"(?P<year>\d{4})년\s*(?P<month>\d{1,2})월\s*(?P<day>\d{1,2})일"
                    )
                    m = pattern.search(s)

                    if m:
                        pattern_name = 'ymd_kor'

                    if not m:
                        pattern = re.compile(
                            r"(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4})"
                        )
                        m = pattern.search(s)

                        if m:
                            pattern_name = 'mdy_slash'

                        if not m:
                            return (None, '매치 없음')

    if len(m['year']) == 2:
        year = '20' + m['year']
    else:
        year = m['year']

    date = f"{year}-{int(m['month']):02d}-{int(m['day']):02d}"

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return (date, pattern_name)
    except ValueError:
        return (None, f'{pattern_name} · 유효하지 않은 날짜')

for s in samples:
    value, pattern_name = normalize_date(s)
    print(f'{s} → {str(value)} [{pattern_name}]')
```

### 문항2. 서버 액세스 로그 파싱과 집계
> 웹 서버의 액세스 로그를 정규표현식으로 파싱해 분석하시오.

- 아래 내용을 담은 로그 파일 access.log 를 생성하시오.
```
203.0.113.42 - - [06/Aug/2026:14:22:31 +0900] "GET /list?page=3 HTTP/1.1" 200 5321 "<https://example.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
198.51.100.7 - - [06/Aug/2026:14:22:33 +0900] "POST /api/search HTTP/1.1" 429 118 "-" "python-requests/2.31.0"
203.0.113.42 - - [06/Aug/2026:14:22:35 +0900] "GET /detail/9981 HTTP/1.1" 404 209 "<https://example.com/list>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

조건
1. 하나의 정규표현식으로 한 줄에서 다음 7개를 추출할 것 
    - ip / timestamp / method / path / status / bytes / user_agent
2. 명명 그룹 (?P<name>...) 을 사용할 것
3. 형식이 깨진 줄은 건너뛰고, 몇 줄을 건너뛰었는지 출력할 것
4. 다음 세 가지를 집계해 출력할 것
    - 상태코드별 요청 수
    - 4xx·5xx가 발생한 경로 상위 5개
    - 봇으로 의심되는 User-Agent 목록과 그 요청 수 (bot / crawler / spider / python-requests 포함 여부로 판정, 대소문자 무시)
5. 결과를 access_report.csv로 저장할 것

```
# 결과예시
파싱 3줄 · 건너뜀 0줄

── 상태코드별 요청 수 ──
status
200    1
404    1
429    1

── 4xx·5xx 발생 경로 상위 5 ──
path
/api/search     1
/detail/9981    1

── 봇 의심 User-Agent ──
user_agent
python-requests/2.31.0    1
  봇 요청 비율 33.3%
```

```py
# 답안


```