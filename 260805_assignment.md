### 문항1. Numpy 배열로 5명 학생의 4과목 성적표를 만들고 축(axis) 기준 통계를 산출하시오.
> 아래 1차원 리스트는 학생 5명이 4개 과목(국어, 영어, 수학, 과학 순)에서 받은 점수를 이어 붙인 것입니다.  

> Numpy만 사용하여(반복문 사용 금지) 다음을 순서대로 수행하고 결과를 출력하세요.
```py
scores = [88, 92, 79, 95,
          75, 68, 82, 70,
          92, 99, 95, 88,
          60, 72, 65, 58,
          85, 80, 78, 90]
```

1. 위 리스트를 5행 4열 ndarray로 변환하고 shape, ndim, size, dtype을 출력하시오.
2. 학생 별 평균과 과목 별 평균을 각각 구하시오.
3. 전체에서 가장 높은 점수와 그 점수가 몇 번째 학생·몇 번째 과목인지 구하시오.
4. 전체 평균, 표준편차, 분산을 구하시오.
5. 평균이 80점 이상인 학생의 인덱스와 인원수를 구하고, 해당 학생들의 성적만 잘라내어 출력하시오.
6. 90점 이상인 점수의 개수, 100점 이상인 점수가 하나라도 있는지, 모든 점수가 60점 이상인지를 판별하시오.
7. 90점 이상은 'A', 80점 이상은 'B', 나머지는 'C'로 변환한 등급 배열을 만드시오.

```py
# 답안
import numpy as np

#1
scores = np.array(scores).reshape(5,4)
print(scores.shape)
print(scores.ndim)
print(scores.size)
print(scores.dtype)

#2
avg_students = scores.mean(axis=1)
avg_subjects = scores.mean(axis=0)

print(avg_students, avg_subjects)

# 3
print(scores.max())

student = scores.argmax() // 4
subject = scores.argmax() % 4

print(student, subject) #2, 1 => 3번째학생, 2번째과목

#4
mean_scores = scores.mean()
std_scores = scores.std()
var_scores = scores.var()

print(mean_scores)
print(std_scores)
print(var_scores)

#5
idx = np.where(avg_students >= 80)
               
print('평균 80점 이상인 학생의 인덱스:', idx[0]) # [0 2 4]
print('평균 80점 이상인 학생의 인원수:', len(idx[0])) # 3
print(avg_students[idx]) # [88.5  93.5  83.25]

#6
# 90점 이상인 점수의 개수
print(np.sum(scores >= 90)) # 6

# 100점 이상인 점수가 하나라도 있는지
print(np.any(scores >= 100)) # False

# 모든 점수가 60점 이상인지
print(np.all(scores >= 60)) # False

#7
grade = np.where(scores >= 90, 'A',
         np.where(scores >= 80, 'B', 'C'))

print(grade)

```

### 문항2. 8x8 난수 배열을 흑백 이미지로 가정하고 슬라이싱·이진화·좌우 반전을 구현하시오.
> 0~255 사이의 정수 난수로 이루어진 8행 8열 배열을 흑백 이미지 데이터라고 가정합니다. 채점 결과를 동일하게 맞추기 위해 반드시 아래 시드를 먼저 실행하세요.

```py
import numpy as np
np.random.seed(2024)
img = np.random.randint(0, 256, size=(8, 8))
```
1. 생성한 `img`를 출력하시오.
2. 이미지 정중앙의 4×4 영역만 잘라내어 출력하시오.
3. 짝수 번째 행(0, 2, 4, 6행)만 뽑아내시오.
4. 128 이상인 픽셀은 255(흰색), 미만인 픽셀은 0(검은색)으로 바꾼 이진화 배열을 만드시오.
5. 이진화 결과에서 흰색 픽셀과 검은색 픽셀의 개수를 각각 세시오.
6. 원본 이미지를 좌·우 절반으로 분할하시오.
7. 분할한 두 조각의 순서를 바꿔 다시 이어 붙여 좌우가 뒤바뀐 이미지를 만드시오.
8. 원본 이미지를 1차원으로 펼친 뒤 앞 10개 값과 shape을 출력하시오.
9. 128 이상인 픽셀만 골라내어 그 개수와 평균값을 구하시오.

```py
# 답안
#1
print(img)

#2
print(img[2:6, 2:6])

#3
print(img[::2, :])

#4
wb = np.where(img >= 128, 255, 0)
print(wb)

#5
w_count = (wb == 255)
print(w_count.sum()) # 28

b_count = (wb == 0)
print(b_count.sum()) # 36

#6
left = img[:, :4]
right = img[:, 4:]
print(left)
print(right)

#7
change = np.concatenate((right, left), axis=1)
print(change)

#8
# 행렬펼치기
flat = change.ravel(order='C')
print(flat)
# 앞 10개 값
print(flat[0:10])
# shape출력
print(flat.shape)

#9
mask = flat >= 128
idx = np.where(mask)
print(idx[0])
print(np.sum(mask)) # 개수 : 28개
print(flat[mask])

print(flat[mask].sum() / np.sum(mask)) # 평균값 193.0714...
```

### 문항3. 지점별 판매 데이터에 브로드캐스트와 행렬 연산을 적용해 매출을 분석하시오.
> 3개 지점이 4개 제품을 판매한 수량과, 제품별 단가가 다음과 같습니다.

```py
sales = np.array([[120,  80,  45,  60],     # A지점
                  [200, 150,  90,  30],     # B지점
                  [ 75,  60, 120,  95]])    # C지점
price = np.array([1500, 3000, 5000, 2000])  # 제품 1~4 단가
```
1. 브로드캐스트를 이용해 각 지점의 제품별 매출액(수량 × 단가) 행렬을 구하시오. (반복문 금지)
2. 행렬곱을 이용해 각 지점의 총매출을 한 번에 구하시오. 또한 제품별 총판매량도 구하시오.
3. 각 제품의 평균 판매량을 구한 뒤, 브로드캐스트로 평균 대비 편차 행렬을 구하시오.
4. 각 지점을 기준으로 판매량을 정규화하시오. 결과의 행별 평균이 0, 표준편차가 1이 되는지 확인하시오.
5. sales의 전치행렬을 구하고 shape을 출력하시오.
6. sales의 앞 3개 열만 잘라 3×3 정방행렬 A를 만들고, 행렬식과 역행렬을 구하시오. 이어서 A와 역행렬을 곱해 단위행렬이 나오는지 확인하시오.
7. 총매출이 가장 높은 지점의 인덱스와, 지점 순서대로의 누적 매출을 구하시오.

```py
# 답안
#1
sales_amount = sales * price
print(sales_amount)

#2
print(sales @ price) # 총매출
print(np.sum(sales, axis=0)) # 제품별 총 판매량

#3
avg = sales.mean(axis=0)
result = sales - avg
print(avg)
print(result)

#4
branch_avg = sales.mean(axis=1)
branch_avg = branch_avg.reshape(3, 1)
print(branch_avg)

branch_std = sales.std(axis=1)
branch_std = branch_std.reshape(3,1)
print(branch_std)

# # 정규화 = (원본 - 평균) / 표준편차
nomalized_sales = (sales - branch_avg) / branch_std
print(nomalized_sales)

print(nomalized_sales.mean(axis=1))
print(nomalized_sales.std(axis=1))

#5
t_sales = sales.T
print(t_sales)
print(t_sales.shape)

#6
A = sales[:, :3]
det_A = np.linalg.det(A)
inv_A = np.linalg.inv(A)
print(det_A)
print(inv_A)

print(A @ inv_A)

#7
branch_sales = sales @ price
print(branch_sales)
print(np.argmax(branch_sales))
print(np.cumsum(branch_sales))
```
