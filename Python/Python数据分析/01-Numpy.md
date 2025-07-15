# Numpy

## 背景
NumPy（Numerical Python的简称）是Python科学计算的基础包。
功能包括多维数组处理、数学函数、线性代数、随机数生成等，且具备高性能的特点。

### 关键优势
- 性能：底层用C实现，避免Python循环开销
- 简洁语法：用矢量操作代替显式循环
- 丰富功能：提供大量数学函数和线性代数运算
- 内存效率：连续存储，支持大数组处理

```python
import numpy as np

my_arr = np.arange(1000000)
my_list = list(range(1000000))

%time for _ in range(10): my_arr2 = my_arr * 2

%time for _ in range(10): my_list2 = [x * 2 for x in my_list]
```

## 多维数组
NumPy的核心是ndarray对象，它是一个多维数组。存储相同类型的元素，支持矢量化运算和广播功能。

### 基础类型

- 布尔型（bool_）。用于表示逻辑值，可以是True或False
- 整型。包括int8、int16、int32、int64等，表示有符号整数。这些类型分别代表不同大小的整数，例如，int8的值的范围是-128到127
- 无符号整型。包括uint8、uint16、uint32、uint64等，用于表示无符号整数，例如，uint8的值的范围是0到255
- 浮点型。包括float16、float32、float64等，用于表示浮点数值，这些类型的精度和表示范围不同
- 复数型。包括complex64和complex128等，用于表示复数值
- 字符串型。包括str_和unicode_等，用于表示字符串数据
- 日期时间类型。datetime64，用于表示日期和时间
- 时间间隔类型。timedelta64，表示两个时间点之间的间隔

### 基础属性
- `ndarray.ndim`: 数组的轴（维度）的个数。在Python世界中，维度的数量被称为rank。
- `ndarray.shape`: 数组的维度。这是一个整数的元组，表示每个维度中数组的大小。对于有 *n* 行和 *m* 列的矩阵，`shape` 将是 `(n,m)`。因此，`shape` 元组的长度就是rank或维度的个数 `ndim`。
- `ndarray.size`: 数组元素的总数。这等于 `shape` 的元素的乘积。
- `ndarray.dtype`: 一个描述数组中元素类型的对象。可以使用标准的Python类型创建或指定dtype。另外NumPy提供它自己的类型。例如numpy.int32、numpy.int16和numpy.float64。
- `ndarray.itemsize`: 数组中每个元素的字节大小。例如，元素为 `float64` 类型的数组的 `itemsize` 为8（=64/8），而 `complex32` 类型的数组的 `itemsize` 为4（=32/8）。它等于 `ndarray.dtype.itemsize` 。
- `ndarray.data`: 该缓冲区包含数组的实际元素。通常，我们不需要使用此属性，因为我们将使用索引访问数组中的元素。

### 数组创建

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1, 2], [3, 4]])

# 显式指定数组类型
c = np.array([[1, 2], [3, 4]], dtype=np.int32)
c = c.astype(np.float32)

# 初始占位符
d = np.zeros((3, 4))
e = np.ones((3, 4))

# 生成等间距序列
# 指定步长 np.arange(start, stop, step)
f = np.arange(0, 5, 0.5)
# [0. 0.5 1. 1.5 2. 2.5 3. 3.5 4. 4.5]

# 指定数组个数 np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0)
g = np.linspace(0, 5, 10)
# array([0.        , 0.55555556, 1.11111111, 1.66666667, 2.22222222,
# 2.77777778, 3.33333333, 3.88888889, 4.44444444, 5.        ])
```

### 数组运算
Numpy的矢量化运算是指对数组进行元素级别的操作，而无需使用循环。  
数组与标量的算数运算会将标量值传播到各个元素。

```python
import numpy as np

A = np.array([[1, 1],[0, 1]])
B = np.array([[2, 0],[3, 4]])

A + 1
# array([[2,2],[1,2]])

A * 2
# [[4,4],[2,4]]

# 对应位置元素相乘
A * B
# array([[2, 0],[0, 4]])

# 矩阵点积
E = A.dot(B)
# array([[2, 0],[0, 4]])

# 布尔运算
A > 0
# array([[ True,  True],[False,  True]])
```

### 索引、切片
数组切片仅是原始数组的视图，对切片的修改会传递到原始数组

```python
import numpy as np

arr = np.arange(9)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8])

arr[0]
# 0

arr[:5]
# array([0, 1, 2, 3, 4])

arr[7:] = 9
# array([0, 1, 2, 3, 4, 5, 6, 9, 9])
```

如果你想要得到的是ndarray切片的一份副本而非视图，就需要明确地进行复制操作

```python
import numpy as np

arr = np.arange(9)

backup = arr.copy()
backup_slice = arr[:5].copy()
```

对于高维度数组,可以传入一个以逗号隔开的索引列表来进行选取

```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 选取第二行，第一列的元素
arr2d[1,0]
# 4

# 选取第二行
arr2d[1,:]
# array([4, 5, 6])

# 选取第三列
arr2d[:,2]
# array([3, 6, 9])
```

布尔索引

```python
import numpy as np

arr = np.arange(9)

arr == 5
# array([False, False, False, False, False,  True, False, False, False])
arr > 5
# array([False, False, False, False, False, False,  True,  True,  True])
arr[arr > 5]
# array([6, 7, 8])

# 组合应用多个布尔条件，需要使用&（和）、|（或）之类的布尔算术运算符
arr[(arr > 3) & (arr < 7)]
# array([4, 5, 6])
```

### 数组转置和轴对换
转置是重塑的一种特殊形式，它返回的是源数据的视图，行转列

```python
import numpy as np

arr = np.arange(9)
arr = arr.reshape(3,3)
# array([[0, 1, 2],
#        [3, 4, 5],
#        [6, 7, 8]])

arr.T
# array([[0, 3, 6],
#        [1, 4, 7],
#        [2, 5, 8]])
```
在进行矩阵计算时，经常需要用到该操作，比如利用np.dot计算矩阵内积

```python
np.dot(arr.T, arr)
# array([[45, 54, 63],
#        [54, 66, 78],
#        [63, 78, 93]])
```

### 条件选择
numpy.where函数是三元表达式x if condition else y的矢量化版本

```python
import numpy as np

arr = np.arange(9)

# 1. 条件过滤
np.where(arr > 4)
# (array([5, 6, 7, 8], dtype=int64),)

# 2. 条件替换(将所有不大于4的元素替换为-1)
np.where(arr > 4, arr, -1)
# array([-1, -1, -1, -1, -1,  5,  6,  7,  8])

# 3. 条件选择
x = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
y = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
condition = np.array([True, False, True, True, False])
np.where(condition, x, y)
# array([1.1, 2.2, 1.3, 1.4, 2.5])
```

### 去重及排序

```python
import numpy as np

arr = np.array([4,4,3,3,2,2,1,1])
np.unique(arr)
# array([1, 2, 3, 4])

np.sort(arr)
# array([1, 1, 2, 2, 3, 3, 4, 4])
```

### 数组拼接

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# 基础拼接函数 axis 0-垂直拼接 1-水平拼接 默认为0
np.concatenate([a,b])
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

# 垂直拼接
np.vstack((a, b))
# >>> array([[1, 2],[3, 4],[5, 6],[7, 8]])

# 水平拼接
np.hstack((a, b))
# >>> array([[1, 2, 5, 6],[3, 4, 7, 8]])
```

### 统计函数

| 函数                                          | 忽略NaN函数                       	                   | 说明                       |
|---------------------------------------------|---------------------------------------------------|--------------------------|
| sum(a,axis=None)                            | nansum(a,axis=None)	                              | 计算数组a元素之和                |
| cumsum(a, axis=None)                        | nancumsum(a, axis=None)                           | 计算数组a的累积和                |
| cumprod(a, axis=None)                       | nancumprod(a, axis=None)                          | 计算数组a的累积乘积               |
| mean(a,axis=None)                           | nanmean(a,axis=None)	                             | 计算数组a的算数平均值              |
| average(a,axis=None,weights=None)           | 	                                                 | 计算数组a相关元素的加权平均值          |
| std(a,axis=None)                            | nanstd(a,axis=None)                               | 计算数组a相关元素的标准差            |
| var(a,axis = None)                          | nanvar(a,axis = None)	                            | 计算数组a相关元素的方差             |
| cov(a,axis = None)	                         |                                                   | 计算数组a相关元素的协方差            |
| min(a, axis = None)/max(a, axis = None)	    | nanmin(a, axis = None)/nanmax(a, axis = None)     | 计算数组a中元素的最小值，最大值         |
| argmin(a,axis = None)/argmax(a,axis = None) | nanargmin(a,axis = None)/nanargmax(a,axis = None) | 	计算数组a中元素的最小值，最大值的降一维后下标 |
| ptp(a, axis=None)	                          |                                                   | 计算数组a中元素最大值和最小值的差        |
| median(a, axis=None)	                       | nanmedian(a, axis=None)                           | 计算数组a中元素的中位数(中值)         |

### 数学函数


| 函数                               | 说明                          |
|----------------------------------|-----------------------------|
| np.abs(a) np.fabs(a)             | 计算数组a各元素的绝对值                |
| np.sqrt(a)	                      | 计算数组a各元素的平方根                |
| np.square(a)	                    | 计算数组a各元素的平方                 |
| np.power(a, n)                   | 计算数组a各元素的n次方                |
| np.log(a) np.log10(a) np.log2(a) | 	计算数组a各元素的自然对数、10底对数和2底对数   |
| np.ceil(a)	                      | 计算数组a各元素的ceiling值(向上取整)     |
| np.floor(a)                      | 计算数组a各元素的floor值(向下取整)       |
| np.rint(a)	                      | 计算数组a各元素的四舍五入值              |
| np.modf(a)	                      | 将数组a各元素的整数和小数部分以两个独立的数组形式返回 |
| np.cos/cosh/sin/sinh/tan/tanh    | 	计算数据各元素的普通型和双典型的三角函数       |
| np.exp(a)	                       | 计算数组各元素的指数值                 |


### 随机数函数  

| 函数	                                               | 说明                                                |
|---------------------------------------------------|---------------------------------------------------|
| random.rand(d0,d1,...dn)                          | 各元素是[0,1)的浮点数，服从均匀分布                              |
| random.randn(d0,d1,...dn)                         | 标准正态分布                                            |
| randint(low, high=None, size=None, dtype=int)     | 根据shape创建随机整数数组，范围是[low,high)                     |
| random.seed(s)                                    | 随机数种子                                             |
| random.shuffle(a)                                 | 根据数组a的第一轴进行随机排列，改变数组a                             |
| random.permutation(a)                             | 根据数组a的第一轴进行随机排列,生成新的数组，不改变数组a                     |
| random.choice(a, size=None, replace=True, p=None) | 从数组a中，以概率p抽取元素，形成size形状新数组，replace表示是否重用元素，默认True |
| random.uniform(low=0.0, high=1.0, size=None)      | 产生均匀分布的数组,起始值为low,结束值为high,size为形状                |
| random.normal(loc=0.0, scale=1.0, size=None)      | 产生正态分布的数组，loc为均值，scale为标准差，size为形状                |
| random.poisson(lam=1.0, size=None)                | 产生泊松分布的数组，lam随机事件发生的概率，size为形状                    |

