## 初识 Hive

Hive 是一个构建在 Hadoop 之上的数据仓库，它可以将结构化的数据文件映射成表，并提供类 SQL 查询功能

1. 简单易上手,类SQL查询语言(HQL)
2. 为超大的数据集设计的计算和存储能力,集群扩展容易
3. 统一元数据管理,可与 Presto,Impala,SparkSQL 等共享数据
4. 执行延迟高，适合海量数据离线处理

### HQL

[基础语法查看](https://www.gairuo.com/p/hive-sql-tutorial)

#### HQL执行过程

1. 语法解析：Antlr 定义 SQL 的语法规则，完成 SQL 词法，语法解析，将 SQL 转化为抽象 语法树 AST Tree；
2. 语义解析：遍历 AST Tree，抽象出查询的基本组成单元 QueryBlock；
3. 生成逻辑执行计划：遍历 QueryBlock，翻译为执行操作树 OperatorTree；
4. 优化逻辑执行计划：逻辑层优化器进行 OperatorTree 变换，合并不必要的 ReduceSinkOperator，减少 shuffle 数据量；
5. 生成物理执行计划：遍历 OperatorTree，翻译为 MapReduce 任务；
6. 优化物理执行计划：物理层优化器进行 MapReduce 任务的变换，生成最终的执行计划。

#### 基本类型

| 大类                              | 类型                                                                                     |
|---------------------------------|----------------------------------------------------------------------------------------|
| **Integers（整型）**                | TINYINT—1 字节的有符号整数 <br/>SMALLINT—2 字节的有符号整数<br/> INT—4 字节的有符号整数<br/> BIGINT—8 字节的有符号整数 |
| **Boolean（布尔型）**                | BOOLEAN—TRUE/FALSE                                                                     |
| **Floating point numbers（浮点型）** | FLOAT— 单精度浮点型 <br/>DOUBLE—双精度浮点型                                                       |
| **Fixed point numbers（定点数）**    | DECIMAL—用户自定义精度定点数，比如 DECIMAL(7,2)                                                     |
| **String types（字符串）**           | STRING—指定字符集的字符序列<br/> VARCHAR—具有最大长度限制的字符序列 <br/>CHAR—固定长度的字符序列                       |
| **Date and time types（日期时间类型）** | TIMESTAMP —  时间戳 <br/>TIMESTAMP WITH LOCAL TIME ZONE — 时间戳，纳秒精度<br/> DATE—日期类型         |
| **Binary types（二进制类型）**         | BINARY—字节序列                                                                            |

#### 复杂类型

| 类型         | 描述                                            | 示例                                     |
|------------|-----------------------------------------------|----------------------------------------|
| **STRUCT** | 类似于对象，是字段的集合，字段的类型可以不同，可以使用 ` 名称.字段名 ` 方式进行访问 | STRUCT ('xiaoming', 12 , '2018-12-12') |
| **MAP**    | 键值对的集合，可以使用 ` 名称[key]` 的方式访问对应的值              | map('a', 1, 'b', 2)                    |
| **ARRAY**  | 数组是一组具有相同类型和名称的变量的集合，可以使用 ` 名称[index]` 访问对应的值 | ARRAY('a', 'b', 'c', 'd')              |

```
CREATE TABLE students(
  name      STRING,   -- 姓名
  age       INT,      -- 年龄
  subject   ARRAY<STRING>,   --学科
  score     MAP<STRING,FLOAT>,  --各个学科考试成绩
  address   STRUCT<houseNumber:int, street:STRING, city:STRING, province:STRING>  --家庭居住地址
) 
row format delimited
fields terminated by '\t'
collection items terminated by ','
map keys terminated by ':'
lines terminated by '\n';
```

### 内部表和外部表

内部表又叫做管理表 (Managed/Internal Table)，创建表时不做任何指定，默认创建的就是内部表。想要创建外部表 (External Table)
，则需要使用 External 进行修饰。 内部表和外部表主要区别如下：

|        | 内部表                                                                                                       | 外部表                                   |
|--------|-----------------------------------------------------------------------------------------------------------|---------------------------------------|
| 数据存储位置 | 内部表数据存储的位置由 hive.metastore.warehouse.dir 参数指定，默认情况下表的数据存储在 HDFS 的 `/user/hive/warehouse/数据库名.db/表名/`  目录下 | 外部表数据的存储位置创建表时由 `Location` 参数指定；      |
| 导入数据   | 在导入数据到内部表，内部表将数据移动到自己的数据仓库目录下，数据的生命周期由 Hive 来进行管理                                                         | 外部表不会将数据移动到自己的数据仓库目录下，只是在元数据中存储了数据的位置 |
| 删除表    | 删除元数据（metadata）和文件                                                                                        | 只删除元数据（metadata）                      |

### 分区表

Hive 中的表对应为 HDFS 上的指定目录，在查询数据时候，默认会对全表进行扫描，这样时间和性能的消耗都非常大。

分区为 HDFS 上表目录的子目录，数据按照分区存储在子目录中。如果查询的 where
字句的中包含分区条件，则直接从该分区去查找，而不是扫描整个表目录，合理的分区设计可以极大提高查询速度和性能。

#### 使用场景

通常，在管理大规模数据集的时候都需要进行分区，比如将日志文件按天进行分区，从而保证数据细粒度的划分，使得查询性能得到提升

#### 创建分区表

```
CREATE TABLE students_partition(
  id        INT, -- 编号
  name      STRING,   -- 姓名
  age       INT      -- 年龄
) 
PARTITIONED BY (classno INT)   -- 按照班级编号进行分区
row format delimited
fields terminated by '\t';
```

#### 加载数据至分区表

```
LOAD DATA LOCAL INPATH "/root/students.txt" OVERWRITE INTO TABLE students_partition PARTITION (classno=2);
```

文件内容如下

```txt
1       小明    12
2       小红    13
```

查看数据

```
select * from students_partition where classno=2;
```

### 分桶表

分区提供了一个隔离数据和优化查询的可行方案，但是并非所有的数据集都可以形成合理的分区，分区的数量也不是越多越好，过多的分区条件可能会导致很多分区上没有数据。同时
Hive 会限制动态分区可以创建的最大分区数，用来避免过多分区文件对文件系统产生负担。鉴于以上原因，Hive
还提供了一种更加细粒度的数据拆分方案：分桶表 (bucket Table)。

分桶表会将指定列的值进行哈希散列，并对 bucket（桶数量）取余，然后存储到对应的 bucket（桶）中。

#### 分区表和分桶表的区别

1. 分区表是一个目录，分桶表是文件
2. 分区表使用partitioned by 子句指定，以指定字段为伪列，需要指定字段类型; 分桶表由clustered by 子句指定，指定字段为真实字段，需要指定桶的个数
3. 分区表的分区个数可以增长，分桶表一旦指定，不能再增长

#### 创建分桶表

```
CREATE TABLE students_bucket(
  id        INT, -- 编号
  name      STRING,   -- 姓名
  age       INT      -- 年龄
) 
CLUSTERED BY(id) SORTED BY(id ASC) INTO 4 BUCKETS -- 分桶时，数据默认按照分桶键升序排列
row format delimited
fields terminated by '\t';
```

#### 加载数据

```
INSERT INTO TABLE students_bucket SELECT *  FROM students; -- 这里的 students 表就是一张普通的学生表
```

### 存储格式

| 格式               | 说明                                                                                                                                                                                                                                                           |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **TextFile**     | 存储为纯文本文件。 这是 Hive 默认的文件存储格式。这种存储方式数据不做压缩，磁盘开销大，数据解析开销大。                                                                                                                                                                                                      |
| **SequenceFile** | SequenceFile 是 Hadoop API 提供的一种二进制文件，它将数据以<key,value>的形式序列化到文件中。这种二进制文件内部使用 Hadoop 的标准的 Writable 接口实现序列化和反序列化。它与 Hadoop API 中的 MapFile 是互相兼容的。Hive 中的 SequenceFile 继承自 Hadoop API 的 SequenceFile，不过它的 key 为空，使用 value 存放实际的值，这样是为了避免 MR 在运行 map 阶段进行额外的排序操作。 |
| **RCFile**       | RCFile 文件格式是 FaceBook 开源的一种 Hive 的文件存储格式，首先将表分为几个行组，对每个行组内的数据按列存储，每一列的数据都是分开存储。                                                                                                                                                                              |
| **ORC Files**    | ORC 是在一定程度上扩展了 RCFile，是对 RCFile 的优化。                                                                                                                                                                                                                         |
| **Avro Files**   | Avro 是一个数据序列化系统，设计用于支持大批量数据交换的应用。它的主要特点有：支持二进制序列化方式，可以便捷，快速地处理大量数据；动态语言友好，Avro 提供的机制使动态语言可以方便地处理 Avro 数据。                                                                                                                                                    |
| **Parquet**      | Parquet 是基于 Dremel 的数据模型和算法实现的，面向分析型业务的列式存储格式。它通过按列进行高效压缩和特殊的编码技术，从而在降低存储空间的同时提高了 IO 效率。                                                                                                                                                                     |



