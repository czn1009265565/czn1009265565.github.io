# Tensors张量
类似于NumPy的多维数组，Tensor(张量)只是给矩阵起的一个花哨的名字，优势是可以在GPU上进行加速计算。

## 初始化

```python
import torch

# 初始化5x3的空矩阵
empty = torch.empty(5, 3)
print(empty)

# 初始化随机矩阵
rand = torch.rand(5, 3)
print(rand)

# 创建一个0填充的矩阵，指定数据类型为long
a = torch.zeros(5, 3, dtype=torch.long)
print(a)
# 创建一个1填充的矩阵，指定数据类型为int32
b = torch.ones(5, 3, dtype=torch.int32)
print(b)

# 基于现有数据创建矩阵
c = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
print(c)
```

## 获取元素

```python
import torch

a = torch.arange(0, 9)

a[1]
# >>> tensor(1)
a[:]
# >>> tensor([0, 1, 2, 3, 4, 5, 6, 7, 8])
a[5:]
# >>> tensor([5, 6, 7, 8])
a[:3]
# >>> tensor([0, 1, 2])
a[3:5]
# >>> tensor([3, 4])
```

## Tensor与NumPy Array
```python
import torch
import numpy as np

f = torch.tensor([[1, 2], [3, 4]])
# Tensor转Array
f_numpy = f.numpy()
# >>> array([[1, 2],[3, 4]], dtype=int64)

# Array转Tensor
h = np.array([[8, 7, 6, 5], [4, 3, 2, 1]])
h_tensor = torch.from_numpy(h)
# >>> tensor([[8, 7, 6, 5],[4, 3, 2, 1]], dtype=torch.int32)
```

## 基本运算

```python
import torch

# 原始数据
data = torch.randint(1, 20, [2, 3])
print(data)

# 加法，不改变原数据
add = data.add(1)
print(add)

# 加法，改变原数据
data.add_(2)
print(data)

# 减法
sub = data.sub(5)
# 乘法
mul = data.mul(5)
# 除法
div = data.div(5)

# 转换维度为2,3
matrix_1 = torch.arange(1, 7).reshape(2, 3)
print(matrix_1)
# 转换维度为3,2
matrix_2 = torch.arange(1, 7).reshape(3, 2)
print(matrix_2)

# 对应元素相乘
a = matrix_1 * matrix_1
print(a)
# 矩阵点乘
b = torch.tensordot(matrix_1, matrix_2, dims=1)
print(b)
```
