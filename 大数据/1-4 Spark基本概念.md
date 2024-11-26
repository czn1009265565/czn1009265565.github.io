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

### 读写CSV

```java
public class SparkSQLApplication {
    public static void main(String[] args) {
        //1. 创建配置对象
        SparkConf conf = new SparkConf().setAppName("sparksql").setMaster("local[*]");

        //2. 获取sparkSession
        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        //3. 编写代码
        DataFrameReader reader = spark.read();

        // 添加参数读取CSV,CSV读取的字段默认都是String类型
        Dataset<Row> userDS = reader
                .option("header", "true")//默认为false 不读取列名
                .option("sep",",") // 默认为, 列的分割
                // 不需要写压缩格式  自适应
                .csv("input/user.csv");
        userDS.show();

        DataFrameWriter<Row> writer = userDS.write();
        writer.option("seq",";")
                .option("header","true")
                // 压缩格式
                // .option("compression","gzip")
                // 写出模式 append-追加,Ignore-忽略本次写出,Overwrite-覆盖写,ErrorIfExists-如果存在报错
                .mode(SaveMode.Append)
                .csv("output");

        //4. 关闭sparkSession
        spark.close();

    }
}      
```
### 读写JSON

```java
public class SparkSQLApplication {
    public static void main(String[] args) {
        //1. 创建配置对象
        SparkConf conf = new SparkConf().setAppName("sparksql").setMaster("local[*]");

        //2. 获取sparkSession
        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        //3. 编写代码 
        // 1. 完整的 json 需要以紧凑的形式保存在一行中
        // 2. json数据可以读取数据的数据类型
        Dataset<Row> json = spark.read().json("input/user.json");
        json.show();

        // 读取别的类型的数据也能写出为json
        DataFrameWriter<Row> writer = json.write();

        writer.json("output");

        //4. 关闭sparkSession
        spark.close();
    }
}
```

### 读写MySQL

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
    // 筛选条件
    String[] predicates = {"id > 100"};

    // 3.2 读取表数据
    spark.read()
            .jdbc("jdbc:mysql://127.0.0.1:3306/dbname",
                    "t1",
                    predicates,
                    properties)
            // 创建临时视图
            .createOrReplaceTempView("node_1");

    spark.sql("select * from node_1 limit 10").createOrReplaceTempView("node_2");
    Dataset<Row> dataset = spark.sql("select * from node_2 order by id");
    dataset.show();

    // 写入
    dataset.write()
            .mode(SaveMode.Append)
            .jdbc("jdbc:mysql://127.0.0.1:3306/dbname", "t2", properties);

    //4. 关闭sparkSession
    spark.close();
  }
}
```

### 用户自定义函数

#### UDF
输入一行返回一行

```java
public class UDFApplication {
  public static void main(String[] args) {
    //1. 创建配置对象
    SparkConf conf = new SparkConf().setAppName("sparksql").setMaster("local[*]");

    //2. 获取sparkSession
    SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

    //3. 编写代码
    Dataset<Row> lineRDD = spark.read().json("user.json");
    lineRDD.createOrReplaceTempView("user");

    // 注册UDF
    spark.udf().register("get_json_path", getJsonPath());
    spark.udf().register("get_upper_case", getUpperCase());

    spark.sql("select get_upper_case(name) as name,age from user").show();
    spark.sql("select name,age,get_json_path(desc, '$.detail') as detail from user").show();

    //4. 关闭sparkSession
    spark.close();
  }

  /** 字符串转大写 */
  public static UserDefinedFunction getUpperCase() {
    //需要首先导入依赖 import static org.apache.spark.sql.functions.udf;
    return udf(new UDF1<String, String>() {
      @Override
      public String call(String value) throws Exception {
        return value.toUpperCase();
      }
    }, DataTypes.StringType);
  }

  /** JSON解析 */
  public static UserDefinedFunction getJsonPath() {
    // 需要首先导入依赖 import static org.apache.spark.sql.functions.udf;
    return udf(new UDF2<String,String, String>() {
      @Override
      public String call(String jsonValue,String jsonPath) throws Exception {
        return JsonPath.read(jsonValue, jsonPath).toString();
      }
    }, DataTypes.StringType);
  }
}
```

#### UDAF
输入多行，返回一行。通常和groupBy一起使用，如果直接使用UDAF函数，默认将所有的数据合并在一起。

```java
public class UDAFApplication {
    public static void main(String[] args) {

        //1. 创建配置对象
        SparkConf conf = new SparkConf().setAppName("sparksql").setMaster("local[*]");

        //2. 获取sparkSession
        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        //3. 编写代码
        spark.read().json("user.json").createOrReplaceTempView("user");

        // 注册需要导入依赖 import static org.apache.spark.sql.functions.udaf;
        spark.udf().register("avgAge",udaf(new MyAvg(), Encoders.LONG()));

        spark.sql("select avgAge(age) newAge from user").show();

        //4. 关闭sparkSession
        spark.close();
    }

    public static class Buffer implements Serializable {
        private Long sum;
        private Long count;

        public Buffer() {
        }

        public Buffer(Long sum, Long count) {
            this.sum = sum;
            this.count = count;
        }

        public Long getSum() {
            return sum;
        }

        public void setSum(Long sum) {
            this.sum = sum;
        }

        public Long getCount() {
            return count;
        }

        public void setCount(Long count) {
            this.count = count;
        }
    }

    public static class MyAvg extends Aggregator<Long,Buffer,Double> {

        @Override
        public Buffer zero() {
            return new Buffer(0L,0L);
        }

        @Override
        public Buffer reduce(Buffer b, Long a) {
            b.setSum(b.getSum() + a);
            b.setCount(b.getCount() + 1);
            return b;
        }

        @Override
        public Buffer merge(Buffer b1, Buffer b2) {

            b1.setSum(b1.getSum() + b2.getSum());
            b1.setCount(b1.getCount() + b2.getCount());

            return b1;
        }

        @Override
        public Double finish(Buffer reduction) {
            return reduction.getSum().doubleValue() / reduction.getCount();
        }

        @Override
        public Encoder<Buffer> bufferEncoder() {
            // 可以用kryo进行优化
            return Encoders.kryo(Buffer.class);
        }

        @Override
        public Encoder<Double> outputEncoder() {
            return Encoders.DOUBLE();
        }
    }
}
```

## Spark Streaming

Spark Streaming 是 Apache Spark 的一个扩展模块，专门用于处理实时数据流。
它通过将数据流切分为一系列小批次（微批次）进行处理，使得开发者能够使用与批处理相同的 API 来处理流数据。
这种微批处理的架构允许 Spark Streaming 高效地处理实时数据，并且提供了高容错性和可扩展性。

Spark Streaming 可以从各种数据源中接收实时数据，如 Apache Kafka、Flume、HDFS等，并且可以将处理结果存储到文件系统、数据库或实时仪表板中。

### DStream特性
在 Spark Streaming 中，DStream（离散化流）是数据流的基本抽象。

- 时间间隔: DStream 会按设定的时间间隔生成一个新的 RDD，并将其作为批次处理的单位。该时间间隔可以由用户定义，通常该间隔时间需要大于计算时间，否则会造成任务叠加。
- 容错机制: 通过将数据持久化到 HDFS 或启用 Checkpoint 机制，DStream 能够在系统故障或失败时恢复数据，并继续处理。
- 转换操作: DStream 提供了一系列的转换操作，如 map、filter、reduceByKey 等，这些操作会作用于每个 RDD，并生成新的 DStream。

### DStream编程

#### 引入依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-streaming_2.12</artifactId>
    <version>${spark.version}</version>
  </dependency>

  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.12</artifactId>
    <version>${spark.version}</version>
  </dependency>

  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-streaming-kafka-0-10_2.12</artifactId>
    <version>${spark.version}</version>
  </dependency>
</dependencies>
```

#### Kafka实例

```java
public class KafkaApplication {
  public static void main(String[] args) throws InterruptedException {
    // 创建流环境
    JavaStreamingContext javaStreamingContext = new JavaStreamingContext(
            "local[*]", "KafkaApplication", Duration.apply(3000));

    // 创建配置参数
    HashMap<String, Object> map = new HashMap<>();
    map.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"hadoop101:9092,hadoop102:9092,hadoop103:9092");
    map.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
    map.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
    map.put(ConsumerConfig.GROUP_ID_CONFIG,"spark_stream");
    // 设置消费模式‌ earliest、‌latest
    map.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"latest");

    // 需要消费的主题
    ArrayList<String> strings = new ArrayList<>();
    strings.add("spark_stream_topic");

    JavaInputDStream<ConsumerRecord<String, String>> directStream = KafkaUtils.createDirectStream(javaStreamingContext,
            LocationStrategies.PreferBrokers(),
            ConsumerStrategies.<String, String>Subscribe(strings,map));

    directStream.map(new Function<ConsumerRecord<String, String>, String>() {
      @Override
      public String call(ConsumerRecord<String, String> v1) throws Exception {
        return v1.value();
      }
    }).print(100);

    // 执行流的任务
    javaStreamingContext.start();
    javaStreamingContext.awaitTermination();
  }
}
```