### 문항1. Dog과 Bird는 Animal이다
> 다음과 같이 Animal 클래스가 주어질 때, 해당 클래스를 상속 받아 아래의 보기와 같이 동작하는 Dog 클래스와 Bird 클래스를 작성하시오. 
```
class Animal:
	def __init__(self, name):
		self.name = name
	
	def walk(self):
		print(f'{self.name}! 걷는다!')
	
	def eat(self):
		print(f'{self.name}! 먹는다!')
```

```
dog = Dog('멍멍이')
dog.walk() # 멍멍이! 달린다!
dog.bark() # 멍멍이! 짖는다!

bird = Bird('구구')
bird.walk() # 구구! 걷는다!
bird.eat() # 구구! 먹는다!
bird.fly() # 구구! 푸드덕!
```

```py
# 답안
class Animal:
	def __init__(self, name):
		self.name = name
	
	def walk(self):
		print(f'{self.name}! 걷는다!')
	
	def eat(self):
		print(f'{self.name}! 먹는다!')

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def walk(self):
        print(f'{self.name}! 달린다!')

    def bark(self):
        print(f'{self.name}! 짖는다!')

class Bird(Animal):
    def __init__(self, name):
        super().__init__(name)
    
    def fly(self):
        print(f'{self.name}! 푸드덕!')

dog = Dog('멍멍이')

dog.walk() # 멍멍이! 달린다!
dog.bark() # 멍멍이! 짖는다!

bird = Bird('구구')

bird.walk() # 구구! 걷는다!
bird.eat() # 구구! 먹는다!
bird.fly() # 구구! 푸드덕!

```

### 문항2. 결제 시스템 구현
> 온라인 쇼핑몰의 결제 시스템을 상속 구조로 설계하세요.

```
1. Payment 클래스

    1) 생성자에서 소유자 owner와 잔액 balance를 받아 저장한다.

    2) 수수료 메서드 (fee)를 정의하여 결제금액에 대한 수수료를 반환하는 추상메서드를 만든다. (Payment 클래스에서는 구현하지 않음)

    3)결제 메서드 (pay)를 정의, 아래 규칙대로 구현하라

        - 총 차감액 = amount + self.fee(amount)

        - 잔액이 총 차감액보다 적으면 ValueError("잔액 부족")를 발생시킨다. (raise 활용)

        - 충분하면 잔액에서 총 차감액을 빼고, {"amount": amount, "fee": 수수료, "balance": 결제후잔액} 딕셔너리를 반환한다.

2. 결제수단 클래스

    1) CardPayment: 수수료는 금액의 2.5% (소수점 버림, int)

    2) MobilePayment: 수수료는 무조건 100원 정액

    3) PointPayment: 수수료는 0원.
    부모의 pay 메서드를 활용하고, {"point_used": True} 값을 추가해 반환한다.
```
```
# 실행 코드
print(CardPayment("홍길동", 20000).pay(10000))    # 수수료 250  
print(MobilePayment("김철수", 20000).pay(10000))  # 수수료 100  
print(PointPayment("이영희", 20000).pay(10000))   # 수수료 0, point_used True  

print("---")  
try:  
    CardPayment("최가난", 5000).pay(10000)         # 잔액 부족  
except ValueError as e:  
    print(f"결제 실패: {e}")  
```

```py
# 답안
class Payment:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def fee(self, amount): 
        ...

# fee =>수수료
# amount => 음식값
# total => 총 지불금액

    def pay(self, amount): 
        fee = self.fee(amount)
        total = amount + fee
        if self.balance < total:
            raise ValueError('잔액 부족')
        else:
            self.balance -= total
        return {
            'amount':amount,
            'fee':fee,
            'balance':self.balance
        }

class CardPayment(Payment):
    def fee(self, amount):
        return int(amount * 0.025)

class MobilePayment(Payment):
    def fee(self, amount):
        return 100

class PointPayment(Payment):
    def fee(self, amount):
        return 0

    def pay(self,amount):
        result = super().pay(amount)
        result['point_used'] = True
        return result


print(CardPayment("홍길동", 20000).pay(10000))    # {'amount': 10000, 'fee': 250, 'balance': 9750}  
print(MobilePayment("김철수", 20000).pay(10000))  # {'amount': 10000, 'fee': 100, 'balance': 9900}
print(PointPayment("이영희", 20000).pay(10000))   # {'amount': 10000, 'fee': 0, 'balance': 10000, 'point_used': True}

print("---")  
try:  
    CardPayment("최가난", 5000).pay(10000)         # 결제 실패: 잔액 부족 
except ValueError as e:  
    print(f"결제 실패: {e}")  
```