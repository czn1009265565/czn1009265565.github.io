# Python 装饰器详解

## 一、装饰器基础概念
装饰器（Decorator）是Python中一种特殊的语法，用于修改或增强函数/类的功能，而不需要修改其源代码。

### 基本特点：
- 本质是高阶函数（接受函数作为参数或返回函数）
- 使用 `@` 符号语法糖
- 遵循"开放-封闭"原则（对扩展开放，对修改封闭）

## 二、基本装饰器示例

### 1. 最简单的装饰器
```python
def simple_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before function call
# Hello!
# After function call
```

### 2. 带参数的函数装饰

```python
def greet_decorator(func):
    def wrapper(name):
        print("Greeting starts")
        func(name)
        print("Greeting ends")
    return wrapper

@greet_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Greeting starts
# Hello, Alice!
# Greeting ends
```

## 三、进阶装饰器特性

### 1. 装饰器带参数

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

say_hi()
```

### 2. 保留原函数元信息

```python
from functools import wraps

def preserve_metadata(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@preserve_metadata
def example():
    """Original docstring"""
    pass

print(example.__name__)
# "example"
print(example.__doc__)
# "Original docstring"
```

## 四、类装饰器

### 1. 装饰类

```python
def add_method(cls):
    def greeting(self):
        return f"Hello from {self.__class__.__name__}"
    cls.greet = greeting
    return cls

@add_method
class Person:
    pass

p = Person()
print(p.greet())  
# "Hello from Person"
```

### 2. 类实现装饰器

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0
    
    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"Call {self.calls} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()
# Call 1 of say_hello
# Hello!
say_hello()
# Call 2 of say_hello
# Hello!
```

## 五、内置装饰器

### 1. property
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
print(c.radius)
# 5
c.radius = 10    
# 调用setter
```

### 2. @classmethod 和 @staticmethod

```python
class MyClass:
    @classmethod
    def class_method(cls):
        print(f"Called from {cls.__name__}")
    
    @staticmethod
    def static_method():
        print("Called as static")

MyClass.class_method()
# Called from MyClass
MyClass.static_method()
# Called as static
```

## 六、实际应用场景

### 1. 计时装饰器
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end-start:.4f} seconds")
        return result
    return wrapper

@timer
def long_running_func():
    time.sleep(1)

long_running_func()
# 输出执行时间
```

### 2. 权限检查

```python
from functools import wraps

def admin_required(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if user.get('role') != 'admin':
            raise PermissionError("Admin access required")
        return func(user, *args, **kwargs)
    return wrapper

@admin_required
def delete_user(user, username):
    print(f"Deleting user {username}")

admin = {'name': 'Alice', 'role': 'admin'}
delete_user(admin, 'bob')
# 正常执行
```

## 七、装饰器链
多个装饰器可以叠加使用，执行顺序从下往上：

```python
@decorator1
@decorator2
@decorator3
def func():
    pass

# 等价于
func = decorator1(decorator2(decorator3(func)))
```

## 八、最佳实践

1. 使用 functools.wraps 保留元信息
2. 避免过度嵌套装饰器（一般不超过3层）
3. 复杂的装饰器参数处理可以考虑使用类装饰器
4. 装饰器应尽量保持单一职责