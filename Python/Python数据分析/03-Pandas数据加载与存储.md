# Pandas数据加载与存储

## 文本读写

- read_csv: 从文件、URL、文件型对象加载带分隔符的数据。默认分隔符为 `,`
- read_table: 从文件、URL、文件型对象加载带分隔符的数据。默认分隔符为制表符 `\t`
- read_fwf: 读取定宽格式数据
- read_clipboard: 读取剪切板中的数据，网页转换为表格是很有用
- read_excel: 读取Execl表格数据
- read_hdf: 读取HDF5文件
- read_html: 读取HTML中的所有表格
- read_json: 读取json字符串中的数据
- read_msgpack: 读取二进制格式编码的pandas数据
- read_pickle: 读取Python pickle格式中存储的任意对象
- read_sas: 读取SAS系统中存储的自定义SAS数据集
- read_sql: 读取SQL查询结果
- read_stata: 读取Stata格式数据集
- read_feature: 读取Feature二进制格式

典型CSV文件，如下 `ex1.csv`:
```csv
"date","close","volume","open","high","low"
2018/10/23,23.230,17943360.0000,22.610,23.5900,22.3300
2018/10/22,23.540,13934080.0000,23.860,24.1100,23.3000
2018/10/19,23.010,12953670.0000,23.940,23.9499,22.9500
2018/10/18,23.330,15580080.0000,23.500,24.1321,23.2200
2018/10/17,23.680,15368750.0000,24.520,24.6100,23.4600
```

使用read_csv读取
```python
import pandas as pd

df = pd.read_csv('ex1.csv')
df.head()
#          date  close      volume   open     high    low
# 0  2018/10/23  23.23  17943360.0  22.61  23.5900  22.33
# 1  2018/10/22  23.54  13934080.0  23.86  24.1100  23.30
# 2  2018/10/19  23.01  12953670.0  23.94  23.9499  22.95
# 3  2018/10/18  23.33  15580080.0  23.50  24.1321  23.22
# 4  2018/10/17  23.68  15368750.0  24.52  24.6100  23.46
```

也可以使用read_table，并指定分隔符
```python
df = pd.read_table('ex1.csv', sep=',')
```

并不是所有文件都有标题行,如下 `ex2.csv`:  
```csv
Alice,25,Beijing
Bob,30,Shanghai
Charlie,35,Hangzhou
```

```python
# Pandas默认分配列名
df2 = pd.read_csv('ex2.csv', header=None)
df2.head()
#          0   1         2
# 0    Alice  25   Beijing
# 1      Bob  30  Shanghai
# 2  Charlie  35  Hangzhou

# Pandas指定列名
df3 = pd.read_csv('ex2.csv', names=['Name','Age','City'])
df3.head()
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35  Hangzhou
```

指定对应列作为索引
```python
df4 = pd.read_csv('ex1.csv', index_col="date")
df4.head()
#             close      volume   open     high    low
# date
# 2018/10/23  23.23  17943360.0  22.61  23.5900  22.33
# 2018/10/22  23.54  13934080.0  23.86  24.1100  23.30
# 2018/10/19  23.01  12953670.0  23.94  23.9499  22.95
# 2018/10/18  23.33  15580080.0  23.50  24.1321  23.22
# 2018/10/17  23.68  15368750.0  24.52  24.6100  23.46
```

指定多列作为索引
```python
df5 = pd.read_csv('ex2.csv', names=['Name','Age','City'], index_col=['City','Age'])
df5.head()
#                  Name
# City     Age
# Beijing  25     Alice
# Shanghai 30       Bob
# Hangzhou 35   Charlie
```

有些情况下，有些表格并不是以固定的分隔符分隔的
```csv
            A         B         C
aaa -0.264438 -1.026059 -0.619500
bbb  0.927272  0.302904 -0.032399
ccc -0.264273 -0.386314 -0.217601
ddd -0.871858 -0.348382  1.100491
```

传递正则表达式作为read_csv的分隔符
```python
df6 = pd.read_csv('ex3.csv', sep='\s+')
df6.head()
#             A         B         C
# aaa -0.264438 -1.026059 -0.619500
# bbb  0.927272  0.302904 -0.032399
# ccc -0.264273 -0.386314 -0.217601
# ddd -0.871858 -0.348382  1.100491
```

`skiprows` 参数用于跳过文件开头的指定行
```python
# 跳过前2行
df7 = pd.read_csv('ex2.csv', skiprows=2, header=None)
df7.head()
#          0   1         2
# 0  Charlie  35  Hangzhou

# 跳过指定行号
df8 = pd.read_csv('ex2.csv', skiprows=[0,2], header=None)
df8.head()
#      0   1         2
# 0  Bob  30  Shanghai
```