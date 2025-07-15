# Pandas

## 背景
Pandas 是一个基于 NumPy 的 Python 数据分析库，
提供了高效的数据结构和工具（如 DataFrame 和 Series），专门用于处理结构化数据（如表格、时间序列等）。

## Series
Series是一种类似于一维数组的对象，它由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成。

Series的字符串表现形式为：索引在左边，值在右边。

### Series创建
```python
import pandas as pd

# 基础创建(默认索引)
s1 = pd.Series([1,2,3,4])
s1
# 0    1
# 1    2
# 2    3
# 3    4
# dtype: int64

# 自定义索引和列名
index = ["a","b","c","d"]
data = [1,2,3,4]
s2 = pd.Series(data=data, index=index, name="col_name")
s2
# a    1
# b    2
# c    3
# d    4
# Name: col_name, dtype: int64

# 字典创建(字典的 key 会自动成为 Series 的索引，value 为数据值)
data = {'Alice': 25, 'Bob': 30, 'Charlie': 35}
s3 = pd.Series(data)
s3
# Alice      25
# Bob        30
# Charlie    35
# dtype: int64
```

### 索引与切片
与普通NumPy数组相比，你可以通过索引的方式选取Series中的单个或一组值，更具有灵活性

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

# 单值访问
s['a']
# 10

# 多值访问
s[['a','b']]
# a    10
# b    20
# dtype: int64

# 位置访问
s.iloc[0]
# 10
s.iloc[-1]
# 30

# 位置切片(不包含结束位置)
s.iloc[0:2]
# a    10
# b    20
# dtype: int64

# 索引切片(包含结束标签)
s.loc["a":"b"]
# a    10
# b    20
# dtype: int64
```

使用NumPy函数或类似NumPy的运算（如根据布尔型数组进行过滤、标量乘法、应用数学函数等）都会保留索引值的链接

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

s[s>10]
# b    20
# c    30
# dtype: int64

np.sqrt(s)
# a    3.162278
# b    4.472136
# c    5.477226
# dtype: float64
```

Series 运算操作（如加减乘除）会按索引自动对齐，未匹配的索引对应值为 NaN

```python
a = pd.Series([1, 2], index=['x', 'y'])
b = pd.Series([3, 4], index=['y', 'z'])
a + b
# x    NaN
# y    5.0
# z    NaN
# dtype: float64
```

Series的索引可以通过赋值的方式就地修改

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
s.index =['d','e','f']
s
# d    10
# e    20
# f    30
# dtype: int64
```


### 缺失值判断

```python
s = pd.Series([1,2,3,np.nan])
pd.isnull(s)
# 0    False
# 1    False
# 2    False
# 3     True
# dtype: bool

pd.notnull(s)
# 0     True
# 1     True
# 2     True
# 3    False
# dtype: bool
```

## DataFrame
DataFrame是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔值等）。
DataFrame既有行索引也有列索引，它可以被看做由Series组成的字典（共用同一个索引）。
DataFrame中的数据是以一个或多个二维块存放的（而不是列表、字典或别的一维数据结构）。

### 创建

```python
# 创建一个字典，其中包含不同的列和数据
data = {
    'Column1': [1, 2, 3, 4],
    'Column2': ['A', 'B', 'C', 'D'],
    'Column3': [5.0, 6.5, 7.2, 8.8]
}
 
# 使用字典创建DataFrame
df = pd.DataFrame(data)

data = [
    [1,2,3],
    [4,5,6]
]
headers = ["c1", "c2", "c3"]
df = pd.DataFrame(data, columns=headers)
```

### 拼接

```python
import pandas as pd

columns = ["column1", "column2", "column3"]
# 使用字典创建DataFrame
df = pd.DataFrame(columns=columns)
# 拼接新行
series = pd.Series([1,2,3], index=columns)
result = pd.concat([df, series.to_frame().T], ignore_index=True)
# 垂直拼接
df = pd.concat([df1, df2], ignore_index=True)
```

#### Numpy数据创建
```python
df = pd.DataFrame(np.random.randn(10,3), columns = ["Column1", "Column2", "Column3"], index = list("abcdefghij"))
```

#### 读取CSV

CSV文件示例:  
```csv
"date","close","volume","open","high","low"
2018/10/23,23.230,17943360.0000,22.610,23.5900,22.3300
2018/10/22,23.540,13934080.0000,23.860,24.1100,23.3000
2018/10/19,23.010,12953670.0000,23.940,23.9499,22.9500
2018/10/18,23.330,15580080.0000,23.500,24.1321,23.2200
2018/10/17,23.680,15368750.0000,24.520,24.6100,23.4600
2018/10/16,24.630,11679180.0000,24.500,24.7000,24.0800
2018/10/15,24.140,11132030.0000,24.110,24.6400,23.8000
2018/10/12,24.450,20191050.0000,24.540,24.9000,23.7400
```

```python
df = pd.read_csv("jd.csv")

# 指定逗号分隔符
df = pd.read_csv("jd.csv", sep=",")
# 指定第一行作为表头
df = pd.read_csv("jd.csv", header=0)
# 自定义表头
df = pd.read_csv("jd.csv", header=0, names=["日期","收盘价","数量","开盘价","最高价","最低价"])
# 指定date列做为index
df = pd.read_csv("jd.csv", index_col=['date'])
```

**公共参数介绍:**  
- sep: 指定分隔符。如果不指定参数，则会尝试使用逗号分隔
- header: 指定作为列名的行，默认0，即取第一行，数据为列名行以下的数据；若数据不含列名，则设定 header = None
- names: 指定结果的列名列表，如果数据文件中没有列标题行，就需要执行header=None
- index_col: 用作行索引的列编号或者列名，如果给定一个序列则有多个行索引

**转存CSV**  
```python
df.to_csv("jd2.csv", index=False)
```

#### 读取Excel
```python
df = pd.read_excel('../data/bikes.xlsx', sheet_name="Sheet1")
```

**转存Excel**  
```python
df.to_excel("jd2.xlsx",sheet_name="Sheet1", index=False)
```

### 属性

#### columns
columns属性可以获得DataFrame有那些列，即DataFrame的表头
```python
df.columns
>>>
Index(['date', 'close', 'volume', 'open', 'high', 'low'], dtype='object')
```

#### shape
shape属性是描述DataFrame的形状的。
```python
df.shape
>>>
# 行,列
(8,6)
```

#### size
size属性返回的是DataFrame的value的个数
```python
df.size
>>>
48
```

#### values
当前DataFrame的数据,是numpy.ndarray类型

```python
df.values
```

### 时间序列

时间序列是指多个时间点上形成的数值序列，它既可以是定期的，也可以是不定期出现的。

#### 创建时间序列
Pandas 支持解析时间格式字符串、`np.datetime64`、`datetime.datetime` 等多种时间序列数据,
生成 `DatetimeIndex`、`TimedeltaIndex` 、`PeriodIndex` 等定频日期与时间段序列。

```python
import datetime
import numpy as np
import pandas as pd

dti = pd.to_datetime(['2024-04-24',np.datetime64('2024-04-25'), datetime.datetime(2024,4,26)])
```

#### 生成定频时间戳
- date_range 默认的频率是日历日
- bdate_range 的默认频率是工作日

```python
# 根据起始和结束日期
start = datetime.datetime(2011, 1, 1)
end = datetime.datetime(2012, 1, 1)
index1 = pd.date_range(start, end)
index2 = pd.bdate_range(start, end)

# 根据频率和周期
pd.date_range(start, periods=10, freq='D')
```

#### 切片索引

```python
# 字符串索引
df['2021-01-01':'2021-02-01']

# 精确索引
df[datetime.datetime(2021, 1, 1):datetime.datetime(2021, 2, 1)]
```
