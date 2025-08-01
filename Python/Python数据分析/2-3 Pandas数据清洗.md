# Pandas 数据清洗
在数据分析和建模的过程中，相当多的时间要用在数据准备上，也就是所谓的特征工程，往往占用分析师80%或者更多。

## 缺失值处理
在 pandas 中，`NaN`（Not a Number）用于表示缺失或不可用的数据

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({'A': [1, 2, np.nan], 'B': [np.nan, None, 5]})
df.head()
#      A    B
# 0  1.0  NaN
# 1  2.0  NaN
# 2  NaN  5.0
```

检测缺失值
```python
# isnull() 与 isna() 等价
df.isnull()
#        A      B
# 0  False   True
# 1  False   True
# 2   True  False

# notnull() 与 notna() 等价
df.notnull()
#        A      B
# 0   True  False
# 1   True  False
# 2  False   True
```

删除缺失值
```python
# 删除包含缺失值的行
df.dropna(axis=0) 

# 删除包含缺失值的列
df.dropna(axis=1)

# 删除全为缺失值的行
df.dropna(how='all', axis=0)

# 删除全为缺失值的列
df.dropna(how='all', axis=1)
```

填充缺失值
```python
# 用固定值填充
df.fillna(0)

# 前向填充（用前一行的值）
df.fillna(method='ffill') 

# 后向填充（用后一行的值）
df.fillna(method='bfill')

# 用统计值填充
df.fillna(df.mean())    # 均值填充
df.fillna(df.median())  # 中位数填充
df.fillna(df.mode())    # 众数填充
```

## 删除重复数据

DataFrame的 `duplicated` 方法返回一个布尔型Series，表示各行是否是重复行

```python
import pandas as pd

df = pd.DataFrame({'A':[1,2,1], 'B':[1,2,1]})
df.duplicated()
# 0    False
# 1    False
# 2     True
dtype: bool
```

DataFrame的 `drop_duplicates`方法会返回一个去重后的DataFrame

```python
df.drop_duplicates()
#    A  B
# 0  1  1
# 1  2  2
```

`duplicated` 与 `drop_duplicates` 默认会判断全部列，你也可以指定部分列进行重复项判断
```python
df.drop_duplicates(['A'])
#    A  B
# 0  1  1
# 1  2  2
```

`duplicated` 与 `drop_duplicates` 默认保留的是第一个出现的值组合。传入keep='last'则保留最后一个
```python
df.drop_duplicates(keep='last')
#    A  B
# 1  2  2
# 2  1  1
```

## 利用函数或映射进行转换

Series的 `map` 方法可以接受一个函数或含有映射关系的字典型对象
```python
english = {"Tom": 70, "Bob": 80, "Kim": 80}
df = pd.DataFrame({'Name':['Tom','Bob','Kim'], 'Math':[80,90,100]})

df['English'] = df['Name'].map(english)
#   Name  Math  English
# 0  Tom    80       70
# 1  Bob    90       80
# 2  Kim   100       80
```

也可以传入一个能够完成全部这些工作的函数

```python
df['English'] = df['Name'].map(lambda x: english[x])
```

当然这里也可以使用 `apply` 函数
```python
df['English'] = df['Name'].apply(lambda x:english[x])
```

## 值替换

利用fillna方法填充缺失数据可以看做值替换的一种特殊情况。map可用于修改对象的数据子集，而replace则提供了一种实现该功能的更简单、更灵活的方式

```python
# 替换单个值
df.replace(100, 'A')
#   Name Math  English
# 0  Tom   80       70
# 1  Bob   90       80
# 2  Kim    A       80

# 替换多个值
df.replace([90,100], 'A')
#   Name Math  English
# 0  Tom   80       70
# 1  Bob    A       80
# 2  Kim    A       80

# 每个值对应不同的替换值
df.replace([70,80,90,100], ['C','B','A','A'])
#   Name Math English
# 0  Tom    B       C
# 1  Bob    A       B
# 2  Kim    A       B
```

## 重命名行索引
这里由于没有指定行索引，因此是默认生成的
```python
df.index
# RangeIndex(start=0, stop=3, step=1)

df.index = df.index.map(lambda a: a*a)
df
#   Name  Math  English
# 0  Tom    80       70
# 1  Bob    90       80
# 4  Kim   100       80
```

## 离散化和面元划分
为了便于分析，连续数据常常被离散化或拆分为“面元”（bin）。假设有一组人员数据，而你希望将它们划分为不同的年龄组

```python
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
```
接下来将这些数据划分为“18到25”、“26到35”、“35到60”以及“60以上”几个面元。要实现该功能，你需要使用pandas的cut函数

```python
bins = [18, 25, 35, 60, 100]
cats = pd.cut(ages, bins)
cats
# [(18, 25], (18, 25], (18, 25], (25, 35], (18, 25], ..., (25, 35], (60, 100], (35, 60], (35, 60], (25, 35]]
# Length: 12
# Categories (4, interval[int64, right]): [(18, 25] < (25, 35] < (35, 60] < (60, 100]]
```
pandas返回的是一个特殊的Categorical对象
```python
cats.codes
# array([0, 0, 0, 1, 0, 0, 2, 1, 3, 2, 2, 1], dtype=int8)
cats.categories
# IntervalIndex([(18, 25], (25, 35], (35, 60], (60, 100]], dtype='interval[int64, right]')
```

如果向cut传入的是面元的数量而不是确切的面元边界，则它会根据数据的最小值和最大值计算等长面元，这里我们将年龄划分为3组
```python
pd.cut(ages, bins=3)
# Categories (3, interval[float64, right]): [(19.959, 33.667] < (33.667, 47.333] < (47.333, 61.0]]
```

qcut是一个非常类似于cut的函数，它可以根据样本百分比对数据进行面元划分
```python
pd.qcut(ages, q=3)
# Categories (3, interval[float64, right]): [(19.999, 24.333] < (24.333, 33.667] < (33.667, 61.0]]
```

与cut类似，你也可以传递自定义的百分比（0到1之间的数值，包含端点）

```python
pd.qcut(ages, q=[0.5,0.9])
```

## 检测和过滤异常值
过滤或变换异常值（outlier）在很大程度上就是运用数组运算

```python
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(1000, 4))
#             0         1         2         3
# 0    1.579059  0.731801  0.479594 -0.013417
# 1    1.857063  1.447599  0.565390 -0.271619
# 2   -0.889404  0.406947 -1.459394 -1.891637
# 3   -1.026456  0.961349 -0.161376 -0.588752
# 4   -1.132299 -0.802765 -1.487836 -0.737502
# ..        ...       ...       ...       ...
```

假设这里需要筛选出第一列中绝对值大于3的数据
```python
col1 = df.iloc[:, 0]
col1[np.abs(col1) > 3]
# 47     3.363335
# 128    3.742106
# Name: 0, dtype: float64
```

筛选出含有绝对值大于3的行
```python
df[(np.abs(df) > 3).any(axis=1)]
#             0         1         2         3
# 47   3.363335  0.791264  0.357049 -1.400207
# 128  3.742106  0.193598  0.020480 -0.412122
```

- any() 函数是一个用于检查DataFrame或Series中是否存在至少一个True/非零/非空字符串
- all() 函数检查 DataFrame 或 Series 中是否所有值都为 True/非零/非空字符串

参数说明
- axis: 检查方向
  - axis=0 或 'index': 按列检查(默认)
  - axis=1 或 'columns': 按行检查
- bool_only: 仅检查布尔列(默认False)
- skipna: 是否跳过NA值(默认True)

## 排列和随机采样

利用numpy.random.permutation函数可以轻松实现对Series或DataFrame的列的随机排序  
- 输入为整数 n: 返回 0 到 n-1 的随机排列数组。
- 输入为数组/序列: 返回其元素的随机排列（不修改原数组）。
- 随机性: 每次调用结果不同（基于伪随机数生成器）。

```python
df = pd.DataFrame(np.arange(5 * 4).reshape((5, 4)))
df
#     0   1   2   3
# 0   0   1   2   3
# 1   4   5   6   7
# 2   8   9  10  11
# 3  12  13  14  15
# 4  16  17  18  19

sampler = np.random.permutation(5)
sampler
# array([1, 0, 4, 3, 2])
df.iloc[sampler, :]
#     0   1   2   3
# 1   4   5   6   7
# 0   0   1   2   3
# 4  16  17  18  19
# 3  12  13  14  15
# 2   8   9  10  11
```