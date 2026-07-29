### 문항1. 재귀 함수
> 재귀 함수를 사용했을 때 얻을 수 있는 장점과 단점을 반복문과 비교하여 작성하시오. 

```
# 답안

<장점>
- 변수 사용을 줄일 수 있기 때문에, 코드를 반복문보다 간단하게 작성할 수 있다.
- 코드가 직관적이고, 이해하기 쉽다.
<단점>
- 반복문보다 연산 속도가 느리다.(연산 비효율 발생)
- 최대 재귀 깊이가 1,000으로 정해져 있다.(RecursionError발생)

```

### 문항2. Circle 클래스 생성, 활용
> 다음의 요구사항을 만족하는 Circle 클래스를 정의하고, 넓이와 둘레, 중심 좌표를 구하는 메서드를 정의하시오.

```
# 반지름: 3, x좌표: 2, y좌표: 4
c1 = Circle(3, 2, 4)

c1.area() #=> 28.26
c1.circumference() #=> 18.84
c1.center() #=> (2, 4)
```

```py
# 답안
class Circle():
    def __init__(self, r, x ,y):
        self.r = r
        self.x = x
        self.y = y
    def area(self):
        result = 3.14 * self.r ** 2
        print(result)
    def circumference(self):
        result = 2 * 3.14 * self.r
        print(result)
    def center(self):
        result = (self.x, self.y)
        print(result)


```