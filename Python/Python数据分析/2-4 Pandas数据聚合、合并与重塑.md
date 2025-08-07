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

```python

```