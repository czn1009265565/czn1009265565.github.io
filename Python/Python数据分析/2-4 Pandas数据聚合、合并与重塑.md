# Pandas 数据聚合、合并与重塑
层次化索引是pandas的一项重要功能，它使你能在一个轴上拥有多个（两个以上）索引级别。

## 多层索引
```python
import numpy as np
import pandas as pd

s1 = pd.Series(data=np.random.randn(9), index=[
    ['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'],
    [1, 2, 3, 1, 3, 1, 2, 2, 3]
])
s1
# a  1   -0.609708
#    2    0.359835
#    3    0.734779
# b  1   -0.189056
#    3    0.619737
# c  1   -0.409865
#    2    0.208735
# d  2   -1.064397
#    3    0.158406
# dtype: float64
```

查看索引
```python
s1.index
# MultiIndex([('a', 1),
#             ('a', 2),
#             ('a', 3),
#             ('b', 1),
#             ('b', 3),
#             ('c', 1),
#             ('c', 2),
#             ('d', 2),
#             ('d', 3)],
#            )
```

对于一个层次化索引的对象，可以使用所谓的部分索引，使用它选取数据子集  
```python
s1.loc['b']
# 1   -0.189056
# 3    0.619737
# dtype: float64

s1.loc['a':'b']
# a  1   -0.609708
#    2    0.359835
#    3    0.734779
# b  1   -0.189056
#    3    0.619737

# 内层选取
s1.loc['a':'b', 1:2]
# a  1   -0.609708
#    2    0.359835
# b  1   -0.189056
# dtype: float64
```

对于一个具有 多层索引（MultiIndex） 的 `Series` 或 `DataFrame`， `unstack()` 将行索引中的一层转换成列索引  
```python
s1.unstack()
#           1         2         3
# a -0.609708  0.359835  0.734779
# b -0.189056       NaN  0.619737
# c -0.409865  0.208735       NaN
# d       NaN -1.064397  0.158406
```

`unstack()` 的逆运算是 `stack()`  
```python
s1.unstack().stack()
# a  1   -0.609708
#    2    0.359835
#    3    0.734779
# b  1   -0.189056
#    3    0.619737
# c  1   -0.409865
#    2    0.208735
# d  2   -1.064397
#    3    0.158406
# dtype: float64
```

对于一个DataFrame，每条轴都可以有分层索引  
```python
df = pd.DataFrame(np.arange(12).reshape((4, 3)),
                index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                columns=[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
df
#      Ohio     Colorado
#     Green Red    Green
# a 1     0   1        2
#   2     3   4        5
# b 1     6   7        8
#   2     9  10       11
```

基于索引选取列分组  
```python
df.loc[:, ['Ohio']]
#      Ohio
#     Green Red
# a 1     0   1
#   2     3   4
# b 1     6   7
```

## 排序
按第二层索引排序  
```python
df.sort_index(level=1)
#      Ohio     Colorado
#     Green Red    Green
# a 1     0   1        2
# b 1     6   7        8
# a 2     3   4        5
# b 2     9  10       11
```

基于列索引排序
```python
df.sort_index(axis=1)
#     Colorado  Ohio
#        Green Green Red
# a 1        2     0   1
#   2        5     3   4
# b 1        8     6   7
#   2       11     9  10
```

## 使用DataFrame的列作为索引

DataFrame的 `set_index` 函数会将其一个或多个列转换为行索引，并创建一个新的DataFrame
```python
df = pd.DataFrame(data = np.random.rand(9).reshape(3,3), columns=['A','B','C'])
df
#           A         B         C
# 0  0.609641  0.582972  0.653154
# 1  0.892500  0.633966  0.122544
# 2  0.136063  0.115897  0.637093

df.set_index(['A','C'])
#                           B
# A        C
# 0.609641 0.653154  0.582972
# 0.892500 0.122544  0.633966
# 0.136063 0.637093  0.115897
```
默认情况下，这些列会从DataFrame中移除，但也可以保留

```python
df.set_index(['A','C'], drop=False)
#                           A         B         C
# A        C
# 0.609641 0.653154  0.609641  0.582972  0.653154
# 0.892500 0.122544  0.892500  0.633966  0.122544
# 0.136063 0.637093  0.136063  0.115897  0.637093
```

`reset_index` 的功能跟 `set_index` 刚好相反，层次化索引的级别会被转移到列里面
```python
df.reset_index()
#    index         A         B         C
# 0      0  0.609641  0.582972  0.653154
# 1      1  0.892500  0.633966  0.122544
# 2      2  0.136063  0.115897  0.637093
```

## 合并数据集

1. `pd.merge` 或 `pd.join` 按一列或多列，类似与SQL的join操作
2. `pd.concat` 以沿着一条轴将多个对象堆叠到一起
3. `combine_first` 用调用对象（self）中的非空值填充目标对象（参数传入的对象）中的空值

大数据集推荐使用 `merge()`，相较于`concat()`，性能更优

### 数据库风格合并

基于指定列名合并
```python
df1 = pd.DataFrame(data={"A":['a','b','c'],"B":[1,2,3]})
df2 = pd.DataFrame(data={"A":['a','b','c'],"C":[1,4,9]})
pd.merge(df1, df2, on=['A'])
#    A  B  C
# 0  a  1  1
# 1  b  2  4
# 2  c  3  9
```

如果两个对象的列名不同，也可以分别进行指定  
```python
df1 = pd.DataFrame(data={"A1":['a','b','c'],"B":[1,2,3]})
df2 = pd.DataFrame(data={"A2":['a','b','c'],"C":[1,4,9]})
pd.merge(df1, df2, left_on='A1', right_on='A2')
#   A1  B A2  C
# 0  a  1  a  1
# 1  b  2  b  4
# 2  c  3  c  9
```

默认情况下，`merge` 做的是“内连接”，结果中的数据是交集。其他方式还有`left`,`right`,`outer`

```python
df1 = pd.DataFrame(data={"A":['a','b','c','d'],"B":[1,2,3,4]})
df2 = pd.DataFrame(data={"A":['a','b','c'],"C":[1,4,9]})

pd.merge(df1, df2, on='A', how='outer')
#    A  B    C
# 0  a  1  1.0
# 1  b  2  4.0
# 2  c  3  9.0
# 3  d  4  NaN
```

多对多连接产生的是行的笛卡尔积  
```python
df1 = pd.DataFrame(data={"A":['a','b','a'],"B":[1,2,3]})
df2 = pd.DataFrame(data={"A":['a','b','a'],"C":[1,4,9]})

pd.merge(df1, df2, on='A', how='left')
#    A  B  C
# 0  a  1  1
# 1  a  1  9
# 2  b  2  4
# 3  a  3  1
# 4  a  3  9
```

对于合并运算需要考虑的最后一个问题是对重复列名的处理。虽然可以手动处理列名重叠的问题，
但merge有一个更实用的suffixes选项，用于指定附加到左右两个DataFrame对象的重叠列名上的字符串

```python
df1 = pd.DataFrame(data={"A":['a','b','c'],"C":[1,2,3]})
df2 = pd.DataFrame(data={"A":['a','b','c'],"C":[1,4,9]})

pd.merge(df1, df2, on='A', suffixes=('_left','_right'))
#    A  C_left  C_right
# 0  a       1        1
# 1  b       2        4
# 2  c       3        9
```

有时候，DataFrame中的连接键位于其索引中，这种情况下，可以传入left_index=True或right_index=True（或两个都传）以说明索引应该被用作连接键
```python
df1 = pd.DataFrame(data={"B":[1,2,3]}, index=['a','b','c'])
df2 = pd.DataFrame(data={"A":['a','b','c'],"C":[1,4,9]})

pd.merge(df1, df2, left_index=True, right_on='A')
#    B  A  C
# 0  1  a  1
# 1  2  b  4
# 2  3  c  9
```

DataFrame还有一个便捷的join实例方法，它能更为方便地实现按索引合并，方法默认使用的是左连接

```python
df1 = pd.DataFrame(data={"B":[1,2,3,4]}, index=['a','b','c','d'])
df2 = pd.DataFrame(data={"C":[1,4,9]}, index=['a','b','c'])

df1.join(df2)
#    B    C
# a  1  1.0
# b  2  4.0
# c  3  9.0
# d  4  NaN
```

## 轴向连接
concat纵向拼接Series值和索引
```python
s1 = pd.Series([0, 1], index=['a', 'b'])
s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])

pd.concat([s1, s2])
# a    0
# b    1
# c    2
# d    3
# e    4
```

concat横向拼接Series，通过传入 `axis=1`
```python
pd.concat([s1, s2], axis=1)
#      0    1
# a  0.0  NaN
# b  1.0  NaN
# c  NaN  2.0
# d  NaN  3.0
# e  NaN  4.0
```

DataFrame纵向合并
```python
df1 = pd.DataFrame(data={"A":[1,2],"B":[3,4]})
df2 = pd.DataFrame(data={"A":[5,6],"B":[7,8]})

pd.concat([df1, df2])
#    A  B
# 0  1  3
# 1  2  4
# 0  5  7
# 1  6  8
```
这里可以看到行索引重复了，可以使用 `ignore_index=True` 重置索引  
```python
pd.concat([df1, df2], ignore_index=True)
#    A  B
# 0  1  3
# 1  2  4
# 2  5  7
# 3  6  8
```

DataFrame横向拼接  
```python
pd.concat([df1, df2], axis=1)
#    A  B  A  B
# 0  1  3  5  7
# 1  2  4  6  8
```

不同列名的情况
```python
df1 = pd.DataFrame(data={"A":[1,2],"B":[3,4]})
df2 = pd.DataFrame(data={"A":[5,6],"C":[7,8]})

pd.concat([df1, df2], ignore_index=True)
#    A    B    C
# 0  1  3.0  NaN
# 1  2  4.0  NaN
# 2  5  NaN  7.0
# 3  6  NaN  8.0
```

交集与并集
```python
pd.concat([df1, df2], ignore_index=True, join='inner')
#    A
# 0  1
# 1  2
# 2  5
# 3  6

pd.concat([df1, df2], ignore_index=True, join='outer')
#    A    B    C
# 0  1  3.0  NaN
# 1  2  4.0  NaN
# 2  5  NaN  7.0
# 3  6  NaN  8.0
```

## 重塑层次化索引

1. stack()  
   - 作用: 将列索引的某一层级“压缩”到行索引中（从宽格式变长格式）。
   - 结果: 生成一个多层索引（MultiIndex）的 Series 或 DataFrame。
   - 适用场景: 将多列数据聚合成单列（如变量名和值分离）。
2. unstack()  
   - 作用: 将行索引的某一层级“展开”到列索引中（从长格式变宽格式）。
   - 结果: 减少行索引层级，增加列索引层级。
   - 适用场景: 将聚合后的数据展开为交叉表形式。

```python
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}
df = pd.DataFrame(data, index=['row1', 'row2', 'row3'])
df
#       A  B
# row1  1  4
# row2  2  5
# row3  3  6
```

压缩最内层列索引到行索引
```python
df.stack()
# row1  A    1
#       B    4
# row2  A    2
#       B    5
# row3  A    3
#       B    6
# dtype: int64
```

展开最内层行索引到列索引  
```python
df.stack().unstack()
#       A  B
# row1  1  4
# row2  2  5
# row3  3  6
```

### 经典应用场景
将宽表转换为长表  
```python
wide_df = pd.DataFrame({
    'Date': ['2023-01-01', '2023-01-02'],
    'AAPL': [150, 152],
    'GOOG': [2800, 2850]
}).set_index('Date')
wide_df
#             AAPL  GOOG
# Date
# 2023-01-01   150  2800
# 2023-01-02   152  2850

long_df = wide_df.stack().reset_index(name='Price')
long_df.columns = ['Date', 'Stock', 'Price']
long_df
#          Date Stock  Price
# 0  2023-01-01  AAPL    150
# 1  2023-01-01  GOOG   2800
# 2  2023-01-02  AAPL    152
# 3  2023-01-02  GOOG   2850
```

将长表转换回宽表
```python
df = long_df.set_index(['Date','Stock']).unstack()
df.columns = df.columns.map('_'.join)
#             Price_AAPL  Price_GOOG
# Date
# 2023-01-01         150        2800
# 2023-01-02         152        2850
```