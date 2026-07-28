### 문항1. 정중앙 문자
> 문자열을 전달 받아 해당 문자열의 정중앙 문자를 반환하는 get_middle_char 함수를 작성하시오.  
> 단, 문자열의 길이가 짝수일 경우에는 정중앙 문자 2개를 반환한다.

```py
# 답안

def get_middle_char(text):
    if len(text) % 2 == 1:
        result1 = text[len(text)//2]
        return result1
    else:
        result2 = text[len(text)//2-1:len(text)//2+1]
        return result2

get_middle_char('study') # => u
get_middle_char('python') # => th

```

### 문항2. 가변 인자 리스트
> 가변 인자 리스트를 사용하여, 개수가 정해지지 않은 여러 정수들을 전달 받아 해당 정수들의 평균 값을 반환하는 my_avg 함수를 작성하시오

```py
# 답안

def my_avg(*nums):
    total = 0
    for num in nums:
        total += num
    return total / len(nums)

my_avg(77, 83, 95, 80, 70) # => 81.0

```