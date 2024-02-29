## Spark Java Word Count

### 引入依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-core_2.12</artifactId>
        <version>3.0.0</version>
    </dependency>

    <dependency>
        <groupId>org.apache.spark</groupId>
        <artifactId>spark-sql_2.12</artifactId>
        <version>3.0.0</version>
    </dependency>
</dependencies>
```

### 实现 WordCount

```java
public class WordCount {

    public static void main(String[] args) {
        // 接受输入、输出
        String inputPath = args[0];
        String outputPath = args[1];

        // 创建SparkContext实例
        SparkSession sparkSession = SparkSession.builder()
                .appName("wordCount").getOrCreate();
        JavaSparkContext sc = new JavaSparkContext(sparkSession.sparkContext());

        // 读取input下所有文件
        JavaPairRDD<String, String> textFiles = sc.wholeTextFiles(inputPath);
        // 将文件内容分割得到word
        JavaRDD<String> stringJavaRDD = textFiles.flatMap(file -> Arrays.stream(file._2.split("\\s+"))
                .collect(Collectors.toList()).iterator());
        // 生成 (word,1) 元组
        JavaPairRDD<String, Integer> wordTuple = stringJavaRDD.mapToPair(word -> new Tuple2<>(word, 1));
        // 统计计数
        JavaPairRDD<String, Integer> result = wordTuple.reduceByKey((a, b) -> a + b);
        // 写出到output
        result.saveAsTextFile(outputPath);
        // 停止Spark实例
        sparkSession.stop();
    }
}
```

### 编译生成Jar包
```shell
mvn clean install -Dmaven.test.skip=true
```
编译生成 `spark-example-1.0-SNAPSHOT.jar`


### 任务提交

```shell
# Standalone
spark-submit --master spark://hadoop001:7077 --class imooc.spark.WordCount spark-example-1.0-SNAPSHOT.jar /root/sparktest/input /root/sparktest/output

# Yarn
spark-submit --master yarn --class imooc.spark.WordCount spark-example-1.0-SNAPSHOT.jar /sparkinput /sparkoutput
```