## Spark 安装部署
本文介绍spark-3.0.0-bin-hadoop3.2 安装部署

1. Standalone 独立集群
2. ON YARN 共用Hadoop 资源集群

### Standalone

1. 解压

```shell
tar -zxvf spark-3.0.0-bin-hadoop3.2.tgz
mv spark-3.0.0-bin-hadoop3.2 /usr/local/spark
```
2. 配置文件 spark-env.sh

在文件末尾增加这两行内容，指定JAVA_HOME和主节点的主机名
   
```shell
cp spark-env.sh.template spark-env.sh

vim spark-env.sh
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export SPARK_MASTER_HOST=hadoop001
```
3. 配置文件 slaves.template

将文件末尾的localhost去掉，增加hadoop002和hadoop003这两个从节点的主机名。
伪分布式安装无需添加hadoop002,hadoop003 默认localhost即可

```shell
cp slaves.template slaves

hadoop002
hadoop003
```

4. 将修改好配置的spark安装包，拷贝到hadoop002和hadoop003上

```shell
scp -rq /usr/local/spark hadoop002:/usr/local/spark
scp -rq /usr/local/spark hadoop003:/usr/local/spark
```
5. 启动spark集群

```shell
# 启动集群
/usr/local/spark/sbin/start-all.sh

# 连接集群
/usr/local/spark/bin/spark-shell --master spark://hadoop001:7077
```

6. 停止spark集群

```shell
/usr/local/spark/sbin/stop-all.sh
```
   
### ON YARN

1. 解压

```shell
tar -zxvf spark-3.0.0-bin-hadoop3.2.tgz
mv spark-3.0.0-bin-hadoop3.2 /usr/local/spark
```

2. 配置文件 spark-env.sh

在文件末尾增加这两行内容，指定JAVA_HOME和主节点的主机名

```shell
cp spark-env.sh.template spark-env.sh

export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
```

3. 任务提交

```shell
./bin/spark-submit \
--class org.apache.spark.examples.SparkPi \
--master yarn \
--deploy-mode cluster \
./examples/jars/spark-examples_2.12-3.0.0.jar \
2
```
4. 添加环境变量

```shell
vim /etc/profile

export SPARK_HOME=/usr/local/spark
export PATH=$PATH:$SPARK_HOME/bin

source /etc/profile
```