# Numpy

### 数据类型

- 布尔型（bool_）。用于表示逻辑值，可以是True或False
- 整型。包括int8、int16、int32、int64等，表示有符号整数。这些类型分别代表不同大小的整数，例如，int8的值的范围是-128到127
- 无符号整型。包括uint8、uint16、uint32、uint64等，用于表示无符号整数，例如，uint8的值的范围是0到255
- 浮点型。包括float16、float32、float64等，用于表示浮点数值，这些类型的精度和表示范围不同
- 复数型。包括complex64和complex128等，用于表示复数值
- 字符串型。包括str_和unicode_等，用于表示字符串数据
- 日期时间类型。datetime64，用于表示日期和时间
- 时间间隔类型。timedelta64，表示两个时间点之间的间隔

对于每种类型都有同名的转换函数可以将数据转为对应数据类型的数据。

### ndarray
一种多维数组对象。  
一种通用的同构数据多维容器，所有的元素都必须是相同的类型，每个数组都有一个shape（维度）和dtype（类型）。  

**创建ndarray**  
```python
import numpy as np

# Python数组
arr1 = np.array([1,2,3])
arr2 = np.array([[1,2,3], [4,5,6]])
# 函数
arr_range = np.arange(10)
arr_zeros1 = np.zeros(3)
arr_zeros2 = np.zeros(3, 3)
arr_ones1 = np.ones(3)
arr_ones2 = np.ones(3, 3)
```

**ndarray类型**  
```python
arr1 = np.array([1,2,3], dtype=np.int32)
arr2 = np.zeros(3, dtype=np.int32)
arr3 = np.ones(3, dtype=np.int32)

# 类型转换
arr1 = arr1.astype(np.float32)
```

### 数组运算
Numpy的矢量化运算是指对数组进行元素级别的操作，而无需使用循环。  
数组与标量的算数运算会将标量值传播到各个元素。  
```python
# 算术运算
arr1 = np.array([1,2,3])
arr1 + 1
>>> array([2, 3, 4])

# 布尔运算
arr1 = np.array([1,2,3])
arr1 > 1
>>> array([False,  True,  True])

# 数组间运算
arr1 = np.array([1,2,3])
arr2 = np.array([4,5,6])
arr1 * arr2
>>> array([ 4, 10, 18])
```

### 切片索引
数组切片仅是原始数组的视图，对切片的修改会传递到原始数组
```python
arr1 = np.array([1,2,3])
arr1[1:] = 4
arr1
>>> array([1, 4, 4])
```

多维数组  
```python
arr = np.arange(9)
arr = arr.reshape((3,3))
arr[:,1]
>>> array([1, 4, 7])
```

### 布尔索引

```python
arr = np.arange(9)
arr[arr > 3]
>>> array([4, 5, 6, 7, 8])
```


### 数学与统计函数
**数学函数**  

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

**统计函数**  

| 函数	                                | 说明                       |
|------------------------------------|--------------------------|
| sum(a,axis=None)	                  | 根据给定axis计算数组a相关元素之和      |
| mean(a,axis=None)	                 | 根据给定axis计算数组a的算数平均值      |
| average(a,axis=None,weights=None)	 | 根据给定axis计算数组a相关元素的加权平均值  |
| std(a,axis=None)	                  | 根据给定轴axis计算数组a相关元素的标准差   |
| var(a,axis = None)	                | 根据给定轴axis计算数组a相关元素的方差    |
| cov(a,axis = None)	                | 根据给定轴axis计算数组a相关元素的协方差   |
| min(a) max(a)	                     | 计算数组a中元素的最小值，最大值         |
| argmin(a) argmax(a)                | 	计算数组a中元素的最小值，最大值的降一维后下标 |
| ptp(a, axis=None)	                 | 计算数组a中元素最大值和最小值的差        |
| median(a, axis=None)	              | 计算数组a中元素的中位数(中值)         |

**随机数函数**  

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
