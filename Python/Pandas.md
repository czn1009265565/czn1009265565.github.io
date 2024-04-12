# Pandas

## Series
Series是一种类似于一维数组的对象，它由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成。

```python
i = ["a","b","c","d"]
v = [1,2,3,4]
t = pd.Series(v, index=i, name = "col_name")
t
>>> 
a    1
b    2
c    3
d    4
Name: col_name, dtype: int64
```

## DataFrame
DataFrame是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔值等）。
DataFrame既有行索引也有列索引，它可以被看做由Series组成的字典（共用同一个索引）。
DataFrame中的数据是以一个或多个二维块存放的（而不是列表、字典或别的一维数据结构）。

### 创建

#### 字典创建
```python
# 创建一个字典，其中包含不同的列和数据
data = {
    'Column1': [1, 2, 3, 4],
    'Column2': ['A', 'B', 'C', 'D'],
    'Column3': [5.0, 6.5, 7.2, 8.8]
}
 
# 使用字典创建DataFrame
df = pd.DataFrame(data)
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