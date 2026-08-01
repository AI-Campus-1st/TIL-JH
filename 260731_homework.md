### 문항1. CSV 다루기
> 아래와 같은 scores.csv가 주어집니다 (일부 행에 빈 값 또는 숫자가 아닌 값이 섞여 있습니다).
```py
name,kor,eng,math
홍길동,90,85,80
김철수,,70,60
이영희,88,abc,95
박민수,100,100,100
```
각 학생의 평균 점수를 계산해 `result.csv(name,average)`로 저장하는 프로그램을 작성하세요.
- 점수 칸이 비어 있거나 숫자로 변환할 수 없으면 그 과목은 0점으로 처리한다.
- 변환에 실패한 칸이 있으면 "[처리] 이영희 - math 값 오류(abc) → 0점 처리" 형태로 로그를 출력한다.
- 평균은 소수 첫째 자리까지 반올림한다.

```py
# 실행결과
[처리] 김철수 - kor 값 오류() → 0점 처리
[처리] 이영희 - eng 값 오류(abc) → 0점 처리
완료: result.csv 생성

```

```py
# 답안
with open('scores.csv', 'r') as f:

    columns = f.readline()
    lines = f.readlines()

    columns = columns.rstrip().split(',')

    subjects = ['kor', 'eng', 'math']
    results = []
    for line in lines:
        data = line.rstrip().split(',')

        for i in range(1, 4):
            try:
                data[i] = int(data[i])
            except:
                print(f'[처리] {data[0]} - {subjects[i-1]} 값 오류({data[i]}) → 0점 처리')
                data[i] = 0

        avg = ((data[1] + data[2] + data[3]) / 3)
        avg = round(avg, 1)

        results.append([data[0], avg])

with open('result.csv', 'w') as f:
    f.write('name,average\n')
    for result in results:
        str_values = map(str, result)
        f.write( ','.join(str_values) + '\n' )

print('완료: result.csv 생성')

```

### 문항2. CSV를 JSON으로 변환
> CSV를 읽어 JSON으로 변환하되, 실패한 행은 건너뛰고 오류 리포트를 남긴다.
> members.csv를 읽어 members.json(리스트 형태)으로 변환하는 프로그램을 작성하세요.

```py
id,name,age
1,홍길동,30
2,김철수,스물다섯
3,이영희,28
4,,40
```

#### 규칙
- 각 행을 {"id": 정수, "name": 문자열, "age": 정수} 형태의 딕셔너리로 변환한다.
- age가 숫자가 아니거나 name이 비어 있는 행은 JSON에 넣지 않고 건너뛴다.
- 건너뛴 행은 errors.log 파일에 행번호와 사유를 기록한다(예: 3행: name 비어있음).
- 최종적으로 "성공 N건 / 실패 M건"을 화면에 출력한다.
- 정상 변환된 데이터만 members.json에 한글이 깨지지 않게 저장한다.

```py
# 실행 결과
성공 2건 / 실패 2건

# members.json
[
  {
    "id": 1,
    "name": "홍길동",
    "age": 30
  },
  {
    "id": 3,
    "name": "이영희",
    "age": 28
  }
]

# errors.log
3행: invalid literal for int() with base 10: '스물다섯'
5행: name 비어있음
```


```py
# 답안



```