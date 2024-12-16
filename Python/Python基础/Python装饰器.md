# Python装饰器

## 简介
装饰器（decorators）是 Python 中的一种高级功能，它允许你动态地修改函数或类的行为。

装饰器是一种函数，它接受一个函数作为参数，并返回一个新的函数或修改原来的函数。

装饰器的语法使用 `@decorator_name` 来应用在函数或方法上。

Python 还提供了一些内置的装饰器，比如 `@staticmethod` 和 `@classmethod`，用于定义静态方法和类方法。

装饰器的应用场景:

- 日志记录: 装饰器可用于记录函数的调用信息、参数和返回值
- 性能分析: 可以使用装饰器来测量函数的执行时间
- 权限控制: 装饰器可用于限制对某些函数的访问权限
- 缓存: 装饰器可用于实现函数结果的缓存，以提高性能

## 基本语法

```python
def decorator_function(original_function):
    def wrapper(*args, **kwargs):
        # 这里是在调用原始函数前添加的新功能
        print("before call")

        result = original_function(*args, **kwargs)

        # 这里是在调用原始函数后添加的新功能
        print("after call")

        return result

    return wrapper


# 使用装饰器
@decorator_function
def target_function(*args, **kwargs):
    pass  # 原始函数的实现


if __name__ == "__main__":
    target_function()
```