# Pandas数据加载与存储

## 文本读取
pandas提供了一些用于将表格型数据读取为DataFrame对象的函数，其中read_csv和read_table是最常用的。

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

先来看一个典型CSV文件，如下 `ex1.csv`:
```csv
"date","close","volume","open","high","low"
2018/10/23,23.230,17943360.0000,22.610,23.5900,22.3300
2018/10/22,23.540,13934080.0000,23.860,24.1100,23.3000
2018/10/19,23.010,12953670.0000,23.940,23.9499,22.9500
2018/10/18,23.330,15580080.0000,23.500,24.1321,23.2200
2018/10/17,23.680,15368750.0000,24.520,24.6100,23.4600
```

使用 `read_csv` 函数读取
```python
import pandas as pd

pd.read_csv('ex1.csv')
#          date  close      volume   open     high    low
# 0  2018/10/23  23.23  17943360.0  22.61  23.5900  22.33
# 1  2018/10/22  23.54  13934080.0  23.86  24.1100  23.30
# 2  2018/10/19  23.01  12953670.0  23.94  23.9499  22.95
# 3  2018/10/18  23.33  15580080.0  23.50  24.1321  23.22
# 4  2018/10/17  23.68  15368750.0  24.52  24.6100  23.46
```

也可以使用read_table，并指定分隔符
```python
pd.read_table('ex1.csv', sep=',')
```

但有时候并不是所有文件都有标题行,如下 `ex2.csv`:  
```csv
Alice,25,Beijing
Bob,30,Shanghai
Charlie,35,Hangzhou
```

```python
# 采用默认分配列名
pd.read_csv('ex2.csv', header=None)
#          0   1         2
# 0    Alice  25   Beijing
# 1      Bob  30  Shanghai
# 2  Charlie  35  Hangzhou

# 自定义指定列名
pd.read_csv('ex2.csv', names=['Name','Age','City'])
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35  Hangzhou
```

指定对应列作为索引
```python
pd.read_csv('ex2.csv',names=['Name','Age','City'], index_col="Name")
#          Age      City
# Name
# Alice     25   Beijing
# Bob       30  Shanghai
# Charlie   35  Hangzhou
```

指定多列作为索引
```python
pd.read_csv('ex2.csv', names=['Name','Age','City'], index_col=['City','Age'])
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
pd.read_csv('ex3.csv', sep='\s+')
#             A         B         C
# aaa -0.264438 -1.026059 -0.619500
# bbb  0.927272  0.302904 -0.032399
# ccc -0.264273 -0.386314 -0.217601
# ddd -0.871858 -0.348382  1.100491
```

`skiprows` 参数用于跳过文件指定行
```python
# 跳过前2行
pd.read_csv('ex2.csv', skiprows=2, header=None)
#          0   1         2
# 0  Charlie  35  Hangzhou

# 跳过指定行号
pd.read_csv('ex2.csv', skiprows=[0,2], header=None)
#      0   1         2
# 0  Bob  30  Shanghai
```

缺失值处理是文件解析任务中的一个重要组成部分,如下 `ex4.csv`
```csv
Name,Age,City
Alice,25,Beijing
Bob,30,Shanghai
Charlie,35,unknown
Tom,0,NULL
```

在 pandas 中，`NaN`（Not a Number）用于表示缺失或不可用的数据
```python
pd.read_csv('ex4.csv')
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35   unknown
# 3      Tom    0       NaN
```

`na_values` 参数用于指定在读取数据时应被识别为缺失值（NaN）的特定值  
```python
pd.read_csv('ex4.csv', na_values=['NULL', 'unknown'])
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35       NaN
# 3      Tom    0       NaN
```

各列也可以自定义各自的NAN标记值
```python
pd.read_csv('ex4.csv', na_values={"City":['NULL','unknown'], "Age":['0']})
#       Name   Age      City
# 0    Alice  25.0   Beijing
# 1      Bob  30.0  Shanghai
# 2  Charlie  35.0       NaN
# 3      Tom   NaN       NaN
```

## 分批读取
处理大型数据集时，分批读取是解决内存限制的有效方法

这里先生成模拟数据
```python
import pandas as pd

data = {
    'order_id': [f'ORD_{i:05d}' for i in range(1, 10001)],
    'product': [f'Product_{i%100}' for i in range(10000)],
    'quantity': [i%10 + 1 for i in range(10000)],
    'price': [round((i%100 + 1) * 1.5, 2) for i in range(10000)]
}

df = pd.DataFrame(data)
df.to_csv('ex5.csv', index=False)
```

读取指定行数  
```python
pd.read_csv('ex5.csv', nrows=5)
#     order_id    product  quantity  price
# 0  ORD_00001  Product_0         1    1.5
# 1  ORD_00002  Product_1         2    3.0
# 2  ORD_00003  Product_2         3    4.5
# 3  ORD_00004  Product_3         4    6.0
# 4  ORD_00005  Product_4         5    7.5
```

逐块读取
```python
chunker = pd.read_csv('ex5.csv',chunksize=1000)
chunker
# <pandas.io.parsers.readers.TextFileReader at 0x21f511b8a30>
```

逐块迭代,统计商品总价
```python
chunker = pd.read_csv('ex5.csv', chunksize=1000)

tot = pd.Series([])
for piece in chunker:
    tot = tot.add(piece.groupby('product')['price'].sum(), fill_value=0)

tot = tot.sort_values(ascending=False)
```

## 输出文本格式

```python
df = pd.read_csv('ex5.csv')
# 使用逗号分隔
df.to_csv('ex6.csv')

# 指定分隔符
df.to_csv('ex6.csv', sep='|')

# 不写入行索引与列索引
df.to_csv('ex6.csv', index=False, header=False)

# 缺失值填充字符
df.to_csv('ex6.csv', na_rep='NULL')

# 指定输出的列
df.to_csv('ex6.csv', columns=['product','quantity','price'])
```

## JSON 数据
JSON已经成为通过HTTP请求在Web浏览器和其他应用程序之间发送数据的标准格式之一。

让我们回忆下之前通过字典创建DataFrame的方式
```python
import json
import pandas as pd

jsonstr = """
{
  "Name": ["Alice", "Bob", "Charlie"],
  "Age": [25, 30, 35],
  "City": ["Beijing", "Shanghai", "Hangzhou"]
}
"""
data = json.loads(jsonstr)
pd.DataFrame(data)
#       Name  Age      City
# 0    Alice   25   Beijing
# 1      Bob   30  Shanghai
# 2  Charlie   35  Hangzhou
```


`read_json` 函数可以自动将特别格式的JSON数据集转换为Series或DataFrame
```python
# 读取记录式(最常用)
# [{"col1":1,"col2":"a"}, {"col1":2,"col2":"b"}]
pd.read_json('ex7.json', orient='records')
#    col1 col2
# 0     1    a
# 1     2    b

# 读取列索引格式
# {"col1":{"row1":1,"row2":2}, "col2":{"row1":"a","row2":"b"}}
pd.read_json('ex7.json')
#       col1 col2
# row1     1    a
# row2     2    b

# 读取行索引格式
# {"row1":{"col1":1,"col2":"a"}, "row2":{"col1":2,"col2":"b"}}
pd.read_json('ex7.json', orient='index')
#       col1 col2
# row1     1    a
# row2     2    b

# 读取值式
# [["a","b"], [1,2]]
pd.read_json('ex7.json', orient='values')
#    0  1
# 0  a  b
# 1  1  2
```

## XML 与 HTML
Python有许多可以读写常见的HTML和XML格式数据的库，包括lxml、Beautiful Soup和html5lib。
lxml的速度比较快，但其它的库处理有误的HTML或XML文件更好。

```shell
pip install lxml beautifulsoup4 html5lib
```

`read_html` 函数适用于小型数据集、且符合表格数据格式。否则还是更推荐scrapy或requests实现数据爬取
```html
<table class="..." id="..." ...>
     <tbody>
        <tr>
            <td>...</td>
        </tr>
        <tr>...</tr>
    </tbody>
</table>
```

## Microsoft Excel

`read_excel` 函数支持读取存储在Excel中的表格型数据。
这两个工具分别使用扩展包xlrd和openpyxl读取XLS和XLSX文件

```shell
pip install xlrd openpyxl
```

```python
df = pd.read_excel('ex8.xlsx', 'Sheet1')

df.to_excel('ex9.xlsx', sheet_name="Sheet1", index=False)
```


## 数据库交互

在商业场景下，大多数数据可能不是存储在文本或Excel文件中。
基于SQL的关系型数据库（如SQL Server、PostgreSQL和MySQL等）使用更为常见。

```python
import pandas as pd
from sqlalchemy import create_engine

# 创建连接引擎，这里以MySQL为例
engine = create_engine('mysql+pymysql://user:password@localhost:3306/db_name')

# 读取数据
df = pd.read_sql('select * from article', engine)
```

连接字符串示例

| 数据库类型      | 链接字符串格式                                    |
|------------|--------------------------------------------|
| MySQL      | mysql+pymysql://user:pass@host:port/db     |
| PostgreSQL | postgresql+psycopg2://user:pass@host/db    |
| SQLite     | sqlite:///path/to/database.db              |
| Oracle     | oracle+cx_oracle://user:pass@host:port/sid |
