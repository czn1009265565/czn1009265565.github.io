# Spark

Spark是一种基于内存的快速、通用、可扩展的大数据分析计算引擎

## 内置模块

![Spark内置模块](./imgs/Spark内置模块.png)

- Spark Core: 实现了Spark的基本功能，包含任务调度、内存管理、错误恢复、与存储系统交互等模块。Spark Core中还包含了对弹性分布式数据集(Resilient Distributed DataSet，简称RDD)的API定义。
- Spark SQL: 是Spark用来操作结构化数据的程序包。通过Spark SQL，我们可以使用 SQL或者Apache Hive版本的HQL来查询数据。Spark SQL支持多种数据源，比如Hive表、Parquet以及JSON等。
- Spark Streaming: 是Spark提供的对实时数据进行流式计算的组件。提供了用来操作数据流的API，并且与Spark Core中的 RDD API高度对应。
- Spark MLlib: 提供常见的机器学习功能的程序库。包括分类、回归、聚类、协同过滤等，还提供了模型评估、数据 导入等额外的支持功能。
- Spark GraphX: 主要用于图形并行计算和图挖掘系统的组件。
- 集群管理器: Spark设计为可以高效地在一个计算节点到数千个计算节点之间伸缩计算。为了实现这样的要求，同时获得最大灵活性，Spark支持在各种集群管理器(Cluster Manager)上运行，包括Hadoop YARN、Apache Mesos，以及Spark自带的调度器Standalone。

## Spark Core

### RDD特性
RDD(Resilient Distributed Dataset)叫做弹性分布式数据集，是Spark中最基本的数据抽象。

- 基于内存: 核心思想是将数据加载到内存中以加快处理速度
- 可持久性: RDD（可持久性（Persistence）是指将 RDD 的计算结果存储在内存或磁盘中，以避免在后续操作中重新计算。
- 惰性计算: RDD中的算子可以划分为转换算子(Transformation)和行动算子(Action)，转换算子是惰性计算的并不会立即执行，行动算子则触发实际计算。
- 分区性: RDD 的分区是指将数据集按照一定的规则分割成若干个部分，每个部分称为一个分区，这些分区可以分布在集群中的不同节点上进行并行处理。
- 容错保证: 每个RDD都维护了完整的转换记录(依赖关系)，因此某个分区数据丢失都可以基于转换记录重新计算，而不需要重新计算整个RDD
- 优先位置: 尽可能地把计算分配到靠近数据的位置，减少数据网络传输
- 不可变性: RDD一旦创建，它的内容就不能被修改。这意味着对RDD的任何操作都会生成一个新的RDD，而不会改变原始RDD的内容。

### RDD编程

#### 引入依赖

```xml
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.12</artifactId>
    <version>${spark.version}</version>
</dependency>
```

#### 创建RDD

在Spark中创建RDD的创建方式可以分为三种：从集合中创建RDD、从外部存储创建RDD、从其他RDD创建

```java
public class RDDApplication {
    public static void main(String[] args) {
        // 1.创建配置对象
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("sparkCore");

        // 2. 创建sparkContext
        JavaSparkContext sc = new JavaSparkContext(conf);

        // 3.1 从集合创建
        JavaRDD<String> collectRDD = sc.parallelize(Arrays.asList("hadoop", "spark"));
        List<String> collectList = collectRDD.collect();
        collectList.forEach(System.out::println);

        // 3.2 从外部存储创建
        JavaRDD<String> fileRDD = sc.textFile("input");

        // 3.3 其他RDD转换
        JavaRDD<String> transformRDD = collectRDD.map((Function<String, String>) s -> s.toUpperCase());

        // 4. 关闭sc
        sc.stop();
    }
}
```

#### 转换算子
Transformation转换算子又可以分为Value和Key-Value两类。但是Key-Value类型的算子首先需要使用特定的方法转换为PairRDD

- Value类型: map,flatMap,filter,distinct,groupBy,sortBy
  ```java
    public class RDDApplication {
    public static void main(String[] args) {
    // 1.创建配置对象
    SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("sparkCore");
    
            // 2. 创建sparkContext
            JavaSparkContext sc = new JavaSparkContext(conf);
    
            // 3. 基于集合创建RDD
            JavaRDD<String> collectRDD = sc.parallelize(Arrays.asList("hadoop", "spark"));
            
            // map映射
            JavaRDD<String> mapRDD = collectRDD.map((Function<String, String>) s -> s.toUpperCase());
            // flatMap扁平化
            JavaRDD<String> flatMapRDD = collectRDD.flatMap(
                    (FlatMapFunction<String, String>) s -> Arrays.stream(s.split(" ")).iterator()
            );
            // filter过滤
            JavaRDD<String> filterRDD = collectRDD.filter((Function<String, Boolean>) s -> s.length() == 6);
            // distinct去重
            JavaRDD<String> distinctRDD = collectRDD.distinct();
            // groupBy
            JavaPairRDD<String, Iterable<String>> groupByJavaPairRDD = collectRDD.groupBy((Function<String, String>) s -> s);
            // sortBy (1)排序字段  (2) true为正序  (3) 排序之后的分区个数
            JavaRDD<String> sortByRDD = collectRDD.sortBy((Function<String, String>) s -> s, true, 2);
    
            // 4. 关闭sc
            sc.stop();
        }
    }
    ```
- Key-Value类型: mapValues,groupByKey,reduceByKey,sortByKey
  ```java
    public class RDDApplication {
    public static void main(String[] args) {
    // 1.创建配置对象
    SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("sparkCore");
    
            // 2. 创建sparkContext
            JavaSparkContext sc = new JavaSparkContext(conf);
    
            // 3. 基于集合创建RDD
            JavaRDD<String> collectRDD = sc.parallelize(Arrays.asList("hadoop", "spark"));
            // 转换为PairRDD
            JavaPairRDD<String, Integer> pairRDD = collectRDD.mapToPair(
                    (PairFunction<String, String, Integer>) s -> new Tuple2<>(s, 1)
            );
            
            // 4. 关闭sc
            sc.stop();
        }
    }
    ```
#### Action行动算子
转换算子都是懒加载，并不会立即执行，而真正触发整个作业的执行的则是行动算子

主要包括: collect,count,first,take,countByValue,countByKey,saveAsTextFile,foreach,foreachPartition

```java
public class RDDApplication {
    public static void main(String[] args) {
        // 1.创建配置对象
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("sparkCore");

        // 2. 创建sparkContext
        JavaSparkContext sc = new JavaSparkContext(conf);

        // 3. 基于集合创建RDD
        JavaRDD<String> collectRDD = sc.parallelize(Arrays.asList("hadoop", "spark"));
        // collect 以数组形式返回
        List<String> collect = collectRDD.collect();
        // count 返回RDD中元素个数
        long count = collectRDD.count();
        // first 返回RDD中第一个元素
        String first = collectRDD.first();
        // take 返回RDD中前N个元素组成的数组
        List<String> take = collectRDD.take(2);
        // countByValue 计数
        Map<String, Long> stringLongMap = collectRDD.countByValue();
        // save 保存为TXT文件
        collectRDD.saveAsTextFile("output");
        // foreach 遍历RDD中每个元素
        collectRDD.foreach(System.out::println);
        // foreachPartition 遍历RDD中每个分区
        collectRDD.foreachPartition(new VoidFunction<Iterator<String>>() {
            @Override
            public void call(Iterator<String> integerIterator) throws Exception {
                // 一次处理一个分区的数据
                while (integerIterator.hasNext()) {
                    String next = integerIterator.next();
                    System.out.println(next);
                }
            }
        });

        // 4. 关闭sc
        sc.stop();
    }
}
```

#### WordCount实例

```java
public class WordCountApplication {
  public static void main(String[] args) {
    String inputPath = args[0];
    String outputPath = args[1];
    // 1.创建配置对象
    SparkConf conf = new SparkConf().setMaster("local").setAppName("sparkCore");

    // 2. 创建sparkContext
    JavaSparkContext sc = new JavaSparkContext(conf);

    // 3. 编写代码
    // 读取数据
    JavaRDD<String> javaRDD = sc.textFile(inputPath);

    // 长字符串切分为单个单词
    JavaRDD<String> flatMapRDD = javaRDD.flatMap(
            (FlatMapFunction<String, String>) s -> Arrays.stream(s.split(" ")).iterator()
    );

    // 转换格式为  (单词,1)
    JavaPairRDD<String, Integer> pairRDD = flatMapRDD.mapToPair(
            (PairFunction<String, String, Integer>) s -> new Tuple2<>(s, 1)
    );

    // 合并相同单词
    JavaPairRDD<String, Integer> javaPairRDD = pairRDD.reduceByKey(
            (Function2<Integer, Integer, Integer>) (v1, v2) -> v1 + v2
    );

    javaPairRDD.collect().forEach(System.out::println);
    javaPairRDD.saveAsTextFile(outputPath);
    // 4. 关闭sc
    sc.stop();
  }
}
```

执行任务  
```shell
bin/spark-submit \
--class com.example.sparkexamples.WordCountApplication \
--master local \
./spark-examples-0.0.1-SNAPSHOT.jar \
./input.txt \
./output
```

## Spark SQL
Spark SQL是用于结构化数据处理的Spark模块。与基本的Spark RDD API不同，Spark SQL提供的接口为Spark提供了有关数据结构和正在执行的计算的更多信息。
在内部，Spark SQL使用这些额外的信息来执行额外的优化。与Spark SQL交互的方式有多种，包括SQL和Dataset API。
计算结果时，使用相同的执行引擎，与您用于表达计算的API/语言无关。

### RDD VS DataFrame VS DataSet
RDD(Spark1.0)=》Dataframe(Spark1.3)=》Dataset(Spark1.6)

 

### 引入依赖

```shell
<dependencies>
    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-core_2.12</artifactId>
        <version>${spark.version}</version>
    </dependency>

    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-sql_2.12</artifactId>
        <version>${spark.version}</version>
    </dependency>
</dependencies>
```


### MySQL读写实例

```java
public class MySQLApplication {
    public static void main(String[] args) {
        //1. 创建配置对象
        SparkConf conf = new SparkConf().setAppName("sparksql").setMaster("local[*]");

        //2. 获取sparkSession
        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        //3. 编写代码

        // 3.1 配置连接参数
        Properties properties = new Properties();
        properties.setProperty("user", "root");
        properties.setProperty("password", "root");

        // 3.2 读取表数据
        Dataset<Row> lineDS = spark.read()
                .jdbc("jdbc:mysql://127.0.0.1:3306/dbname", "t1", properties);
        // 3.3 创建临时视图
        lineDS.createOrReplaceTempView("node_1");
        lineDS = spark.sql("select * from node_1 limit 100");
        lineDS.createOrReplaceTempView("node_2");
        lineDS = spark.sql("select * from node_2 order by id");
        lineDS.show();

        // 写入
        lineDS.write()
                .mode(SaveMode.Append)
                .jdbc("jdbc:mysql://127.0.0.1:3306/dbname", "t2", properties);

        //4. 关闭sparkSession
        spark.close();
    }
}
```