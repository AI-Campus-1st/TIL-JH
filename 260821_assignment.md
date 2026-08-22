### 문항1. 네이버 VIBE Top 100 수집
> 네이버 VIBE 차트에서 오늘의 Top 100 순위를 수집하시오.

- 대상: https://vibe.naver.com/chart
- 추출 필드: 순위 / 곡명 / 아티스트
- 아티스트는 리스트로 담을 것 (협업곡은 여러 명)
- Selenium 사용 금지
- 100건이 모두 수집되었는지 건수로 확인할 것
- 결과를 vibe_top100.csv로 저장할 것

```
# 결과 예시
[{'순위': 1, '곡명': 'All I Want for Christmas Is You', '아티스트': ['Mariah Carey']},
 {'순위': 2, '곡명': 'APT.', '아티스트': ['로제 (ROSÉ)', 'Bruno Mars']},
 ...]
```

```py
# 답안
import requests
import pandas as pd

URL = 'https://apis.naver.com/vibeWeb/musicapiweb/vibe/v6/chart/home'

headers = {
    'Accept': 'application/json'
}

res = requests.get(URL, headers=headers)

# res.status_code
# res.text

data = res.json()

# data  # res안에 json데이터를 파이썬 자료형으로 변환해서 가져옴

tracks = data['response']['result']['charthome']['charts'][0]['items']['tracks']

len(tracks) # 100

results = []

for track in tracks:
    # 순위
    rank = track['rank']['currentRank']
    # 곡명
    title = track['trackTitle']
    # 아티스트
    artists = []
    for artist in track['artists']:
        artists.append(artist['artistName'])

    result = {
        '순위': rank,
        '곡명': title,
        '아티스트': artists,
    }

    results.append(result)

print(len(results))
print(results[0])

df = pd.DataFrame(results)
df.to_csv('vibe_top100.csv', index=False, encoding='utf-8-sig')
```
