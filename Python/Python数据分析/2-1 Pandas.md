# Pandas

## 背景
Pandas 是一个基于 NumPy 的 Python 数据分析库，
提供了高效的数据结构和工具（如 DataFrame 和 Series），专门用于处理结构化数据（如表格、时间序列等）。

## Series
Series是一种类似于一维数组的对象，它由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成。

Series的字符串表现形式为：索引在左边，值在右边。

### 创建
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

基于字典创建
```python
import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['Beijing', 'Shanghai', 'Hangzhou']
}
df1 = pd.DataFrame(data)
df1
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35  Hangzhou

# 指定顺序
df2 = pd.DataFrame(data, columns=['City', 'Name', 'Age'])
df2
#        City     Name  Age
# 0   Beijing    Alice   25
# 1  Shanghai      Bob   30
# 2  Hangzhou  Charlie   35

# 如果传入的列名在字典中不存在，则会产生缺失值
df3 = pd.DataFrame(data, columns=['City', 'Name', 'Age','Sex'])
df3
#        City     Name  Age  Sex
# 0   Beijing    Alice   25  NaN
# 1  Shanghai      Bob   30  NaN
# 2  Hangzhou  Charlie   35  NaN
```

基于列表创建
```python
data = [
    ['Alice', 25, 'Beijing'],
    ['Bob', 30, 'Shanghai'],
    ['Charlie', 35, 'Hangzhou']
]
df4 = pd.DataFrame(data, columns=['Name', 'Age', 'City'])
df4
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35  Hangzhou

# 指定索引
df5 = pd.DataFrame(data, columns=['Name', 'Age', 'City'], index=['a','b','c'])
df5
#       Name  Age      City
# a    Alice   25   Beijing
# b      Bob   30  Shanghai
# c  Charlie   35  Hangzhou
```

### 基本功能

```python
import pandas as pd

# 初始化DataFrame
data = [
    ['Alice', 25, 'Beijing'],
    ['Bob', 30, 'Shanghai'],
    ['Charlie', 35, 'Hangzhou']
]
df = pd.DataFrame(data, columns=['Name', 'Age', 'City'], index=['a','b','c'])

# 查看样例数据，默认前五条
df.head()
#       Name  Age      City
# a    Alice   25   Beijing
# b      Bob   30  Shanghai
# c  Charlie   35  Hangzhou

# 基于列名访问,返回整列
df.Name
df['Name']
# a      Alice
# b        Bob
# c    Charlie
# Name: Name, dtype: object
```

列可以通过赋值的方式进行修改或新增
```python
df['Age'] = 30
df
#       Name  Age      City
# a    Alice   30   Beijing
# b      Bob   30  Shanghai
# c  Charlie   30  Hangzhou

df['Sex'] = 'male'
df
#       Name  Age      City   Sex
# a    Alice   30   Beijing  male
# b      Bob   30  Shanghai  male
# c  Charlie   30  Hangzhou  male
```

将列表或数组赋值给某个列时，其长度必须跟DataFrame的长度相匹配。如果赋值的是一个Series，就会精确匹配DataFrame的索引，所有的空位都将被填上缺失值

```python
sex = pd.Series(['male','female','female'], index=['b','a','c'])
df['Sex'] = sex
df
#       Name  Age      City     Sex
# a    Alice   30   Beijing  female
# b      Bob   30  Shanghai    male
# c  Charlie   30  Hangzhou  female
```

del方法可以用来删除列(更推荐drop方法)

```python
del df['Sex']
df
#       Name  Age      City
# a    Alice   30   Beijing
# b      Bob   30  Shanghai
# c  Charlie   30  Hangzhou
```

使用类似NumPy数组的方法，对DataFrame进行转置（交换行和列）

```python
df.T
#             a         b         c
# Name    Alice       Bob   Charlie
# Age        30        30        30
# City  Beijing  Shanghai  Hangzhou
```

跟Series相同，values属性也会以二维ndarray的形式返回DataFrame中的数据

```python
df.values
# array([['Alice', 30, 'Beijing'],
#        ['Bob', 30, 'Shanghai'],
#        ['Charlie', 30, 'Hangzhou']], dtype=object)
```

### 索引与切片
DataFrame引入了特殊的标签运算符标签索引loc和下标位置索引iloc。

| 特性	     | loc                         | 	iloc                |
|---------|-----------------------------|----------------------|
| 索引类型	   | 标签（index/column names）      | 	下标位置                |
| 区间包含性	  | 闭区间（包含端点）	                  | 左闭右开（不包含右端点）         |
| 支持条件筛选	 | 直接支持（如 df.loc[df['A'] > 1]） | 	需转换为位置（如 nonzero()） |
| 性能      | 	稍慢（需查找标签）                  | 	更快（直接访问位置）          |

>注意点:通过索引方式返回的列只是相应数据的视图而已，并不是副本。因此，对返回的Series所做的任何就地修改全都会反映到源DataFrame上。

```python
# 基于标签的索引(行标签和列标签)，包含区间端点
df.loc['a', :]
# Name      Alice
# Age          25
# City    Beijing
# Name: a, dtype: object
df.loc['a', ['Name','Age']]
# Name    Alice
# Age        30
# Name: a, dtype: object

# 基于下标位置索引访问，左闭右开，不包含右端点
df.iloc[0, :]
# Name      Alice
# Age          25
# City    Beijing
# Name: a, dtype: object
df.iloc[0, [0,1]]
# Name    Alice
# Age        30
# Name: a, dtype: object
```

### 重置索引
```python
# 重置行索引,默认为行索引
df.reindex(index=['c','b','a'])
#       Name  Age      City
# c  Charlie   30  Hangzhou
# b      Bob   30  Shanghai
# a    Alice   30   Beijing

# 重置列索引
df.reindex(columns=['City', 'Name', 'Age'])
df
#        City     Name  Age
# a   Beijing    Alice   30
# b  Shanghai      Bob   30
# c  Hangzhou  Charlie   30
```

### 删除索引
```python
# 删除行索引
df.drop(index=['a'])
#       Name  Age      City
# b      Bob   30  Shanghai
# c  Charlie   30  Hangzhou

# 删除列索引
df.drop(columns=['Name'])
#    Age      City
# a   30   Beijing
# b   30  Shanghai
# c   30  Hangzhou
```

### 算数运算和数据对齐
pandas最重要的一个功能是，它可以对不同索引的对象进行算术运算。
在将对象相加时，如果存在不同的索引对，则结果的索引就是该索引对的并集。

```python
data1 = [
    [1,2,3],
    [4,5,6]
]
df1 = pd.DataFrame(data1, columns=['c1','c2','c3'], index=['a','b'])

data2 = [
    [7,8,9],
    [10,11,12]
]
df2 = pd.DataFrame(data2, columns=['c1','c2','c3'], index=['b','c'])

# 如果DataFrame对象相加，没有共用的列或行标签，结果都会是空
df1+df2
#      c1    c2    c3
# a   NaN   NaN   NaN
# b  11.0  13.0  15.0
# c   NaN   NaN   NaN
```

### 算数运算与填充值
在对不同索引的对象进行算术运算时，你可能希望当一个对象中某个轴标签在另一个对象中找不到时填充一个特殊值（比如0）

```python
df1.add(df2, fill_value=0)
#      c1    c2    c3
# a   1.0   2.0   3.0
# b  11.0  13.0  15.0
# c  10.0  11.0  12.0
```

以字母r开头，它会翻转参数  
- add, radd 加法
- sub, rsub 减法
- div, rdiv 除法
- floordiv, rfloordiv 地板除
- mul, rmul 乘法
- pow, rpow 指数

### 函数与映射
NumPy的ufuncs（元素级数组方法）也可用于操作pandas对象
```python
df = pd.DataFrame(np.random.randn(4, 3))
df
#           0         1         2
# 0 -0.623919  0.657959  0.460313
# 1  0.215846 -0.130751  0.012251
# 2  0.241636 -0.849421 -0.700828
# 3  2.880184  2.273270 -0.472849

np.abs(df)
#           0         1         2
# 0  0.623919  0.657959  0.460313
# 1  0.215846  0.130751  0.012251
# 2  0.241636  0.849421  0.700828
# 3  2.880184  2.273270  0.472849
```
另一个常见的操作是，将函数应用到由各列或行所形成的一维数组上。DataFrame的apply方法即可实现此功能。
```python
f = lambda x: x.mean()

df.apply(f)
# 0    0.678437
# 1    0.487764
# 2   -0.175278
# dtype: float64
```
基本语法  
```python
DataFrame.apply(func, axis=0, raw=False, result_type=None, args=(), **kwargs)
```
- func: 应用的函数
- axis:  
  - axis=0 或 'index'（默认）: 对每一列应用函数
  - axis=1 或 'columns': 对每一行应用函数
- args: 传递给函数的位置参数
- kwargs: 传递给函数的关键字参数

类似的applymap方法可以实现对DataFrame中的每个元素进行转换
```python
f = lambda x: '%.2f' % x
df.applymap(f)
#        0      1      2
# 0  -0.62   0.66   0.46
# 1   0.22  -0.13   0.01
# 2   0.24  -0.85  -0.70
# 3   2.88   2.27  -0.47
```

map方法口适用于 `Series` 中的每个元素进行映射或转换
```python
# 格式化
df.iloc[0, :].map(lambda x: '%.2f' % x)
# 0    -0.62
# 1     0.66
# 2     0.46
# Name: 0, dtype: object

# 修改列名
df.columns = df.columns.map(lambda x: 'column_' + x)
df
#    column_0  column_1  column_2
# 0 -0.623919  0.657959  0.460313
# 1  0.215846 -0.130751  0.012251
# 2  0.241636 -0.849421 -0.700828
# 3  2.880184  2.273270 -0.472849
```

### 排序与排名

```python
df = pd.DataFrame(np.random.randn(3, 3), columns=['c','b','a'], index=['three','two','one'])
df
#               c         b         a
# three -0.083204  1.543056 -0.232281
# two    1.659153 -0.691435  0.266102
# one    0.527569 -0.883109  1.313007

# 根据行索引排序
df.sort_index()
#               c         b         a
# one    0.527569 -0.883109  1.313007
# three -0.083204  1.543056 -0.232281
# two    1.659153 -0.691435  0.266102

# 根据列索引排序
df.sort_index(axis=1)
#               a         b         c
# three -0.232281  1.543056 -0.083204
# two    0.266102 -0.691435  1.659153
# one    1.313007 -0.883109  0.527569

# 根据行索引倒序
df.sort_index(ascending=False)
#               c         b         a
# two    1.659153 -0.691435  0.266102
# three -0.083204  1.543056 -0.232281
# one    0.527569 -0.883109  1.31300

# 根据列值排序
df.sort_values(by='a')
#               c         b         a
# three -0.083204  1.543056 -0.232281
# two    1.659153 -0.691435  0.266102
# one    0.527569 -0.883109  1.313007

# 根据多列排序
df.sort_values(by=['a','b'])
#               c         b         a
# three -0.083204  1.543056 -0.232281
# two    1.659153 -0.691435  0.266102
# one    0.527569 -0.883109  1.313007
```

接下来介绍Series和DataFrame的rank方法
```python
DataFrame.rank(
    axis=0,                  # 排名方向：0按列排名，1按行排名
    method='average',        # 排名方法（见下文）
    numeric_only=None,       # 是否仅对数值列排名
    na_option='keep',        # 缺失值处理方式
    ascending=True,          # 是否升序排名
    pct=False                # 是否返回百分比排名
)
```
1. method（排名方法）  
   - 'average'	默认值，相同值取平均排名（如1, 2, 2 → 1, 2.5, 2.5）
   - 'min'	相同值取最小排名（如1, 2, 2 → 1, 2, 2）
   - 'max'	相同值取最大排名（如1, 2, 2 → 1, 3, 3）
   - 'first'	按数据出现顺序分配排名（如1, 2, 2 → 1, 2, 3）
   - 'dense'	相同值排名相同，但后续排名不跳跃（如1, 2, 2 → 1, 2, 2；下一个是3）
2. na_option（缺失值处理）  
   - 'keep'：保留缺失值，不参与排名（默认）
   - 'top'：缺失值排在最前
   - 'bottom'：缺失值排在最后
3. pct（百分比排名）  
   - True：返回值的百分位排名（范围[0, 1]）

```python
scores = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85, 92, 85, 78]
})
scores['Rank'] = scores['Score'].rank(ascending=False, method='min')
#       Name  Score  Rank
# 0    Alice     85   2.0
# 1      Bob     92   1.0
# 2  Charlie     85   2.0
# 3    David     78   4.0

scores.sort_values(by='Rank')
#       Name  Score  Rank
# 1      Bob     92   1.0
# 0    Alice     85   2.0
# 2  Charlie     85   2.0
# 3    David     78   4.0
```

### 汇总统计
DataFrame对象拥有一组常用的数学和统计方法，如均值、标准差、分位数等。

```python
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': ['X', 'Y', 'X', 'Y', 'X']  # 非数值列自动忽略
})

# 针对Series或DataFrame列计算汇总统计
df.describe()
#               A          B
# count  5.000000   5.000000
# mean   3.000000  30.000000
# std    1.581139  15.811388
# min    1.000000  10.000000
# 25%    2.000000  20.000000
# 50%    3.000000  30.000000
# 75%    4.000000  40.000000
# max    5.000000  50.000000
```

| 方法            | 说明                        |
|---------------|---------------------------|
| count         | 非NA值的数量                   |
| describe      | 针对Series或DataFrame列计算汇总统计 |
| min/max       | 计算最小值和最大值                 |
| argmin/argmax | 计算获取到的最小值和最大值的索引位置        |
| idxmin/idxmax | 计算获取到的最小值和最大值的索引值         |
| quantile      | 计算样本的分位数(0-1)             |
| sum           | 值的总和                      |
| mean          | 值的平均值                     |
| median        | 值的算数中位数                   |
| mad           | 根据平均值计算平均绝对离差             |
| var           | 样本值的方差                    |
| std           | 样本值的标准差                   |
| skew          | 样本值的偏度(三阶矩)               |
| kurt          | 样本值的峰度(四阶矩)               |
| cumsum        | 样本值的累计和                   |
| cummin/cummax | 样本值的累计最小值和累计最大值           |
| cumprod       | 样本值的累计积                   |
| diff          | 计算一阶差分                    |
| pct_change    | 计算百分数变化                   |


### 相关系数与协方差

Series的corr和cov方法用于计算两个Series中重叠的、非NA的、按索引对齐的值的相关系数或协方差
```python
df = pd.DataFrame(data=np.random.rand(10,2),columns=['A','B'])
df.head()
#           A         B
# 0  0.145299  0.589530
# 1  0.348180  0.407578
# 2  0.961118  0.358217
# 3  0.080754  0.724280
# 4  0.456072  0.269244

df['A'].corr(df['B'])
# -0.38845939898319237

df['A'].cov(df['B'])
# -0.0348801705940428
```

DataFrame的corr和cov方法将分别计算列与列之间的相关系数或协方差矩阵
```python
df.corr()
#           A         B
# A  1.000000 -0.388459
# B -0.388459  1.000000

df.cov()
#           A         B
# A  0.099861 -0.034880
# B -0.034880  0.080736
```

DataFrame的corrwith方法可以计算其列或行跟另一个Series或DataFrame之间的相关系数
```python
df.corrwith(df['A'])
# A    1.000000
# B   -0.388459

df.corrwith(df)
# A    1.0
# B    1.0

df.corrwith(df, axis=1)
# 0    1.0
# 1    1.0
# 2    1.0
# 3    1.0
# 4    1.0
# 5    1.0
# 6    1.0
# 7    1.0
# 8    1.0
# 9    1.0
```

### 唯一值与值计数

unique函数可以返回Series中的唯一值数组
```python
s1 = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
uniques = s1.unique()
uniques
# array(['c', 'a', 'd', 'b'], dtype=object)
```

value_counts()函数，用于统计DataFrame/Series中每个唯一值出现的次数
```python
s1 = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
d1 = pd.DataFrame(data=np.random.rand(2,2),columns=['A','B'])

s1.value_counts()
# c    3
# a    3
# b    2
# d    1
# Name: count, dtype: int64

d1.value_counts()
# A         B
# 0.176576  0.597745    1
# 0.941797  0.854708    1
# Name: count, dtype: int64
```