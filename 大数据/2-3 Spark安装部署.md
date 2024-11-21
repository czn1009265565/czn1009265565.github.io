# Spark 安装部署

1. Local模式: 在本地部署单个Spark服务
2. Standalone模式: Spark自带的任务调度模式
3. Yarn模式: Spark使用Hadoop的Yarn组件进行资源与任务调度
4. Mesos模式: Spark使用Mesos平台进行资源与任务调度

[下载地址](https://spark.apache.org/downloads.html)

## Local模式

### 安装使用

解压

```shell
tar -zxvf spark-3.3.1-bin-hadoop3.tgz
mv spark-3.3.1-bin-hadoop3 /opt/module/spark-local
```

官方求PI示例

```shell
bin/spark-submit \
--class org.apache.spark.examples.SparkPi \
--master local[2] \
./examples/jars/spark-examples_2.12-3.3.1.jar \
10
```

参数介绍:

- `--class` 表示要执行程序的主类
- `--master` 运行模式
    - `local`: 所有计算都运行在一个线程当中，没有任何并行计算
    - `local[K]`: 指定使用K个CPU核心来并行计算
    - `local[*]`: 基于CPU核心数自动指定
    - `spark://host:port`: Standalone模式
    - `yarn-client` 与 `yarn-cluster`: Yarn模式
    - `mesos://host:port`: Mesos模式
- `spark-examples_2.12-3.3.1.jar`: 运行的程序
- `10`: 要运行程序的输入参数

Spark Yarn模式有`yarn-client`和`yarn-cluster`两种模式，主要区别在于: Driver程序的运行节点

- `yarn-client`: Driver程序运行在客户端，适用于交互、调试，希望立即看到app的输出。
- `yarn-cluster`: Driver程序运行在由ResourceManager启动的APPMaster，适用于生产环境。

## Standalone 模式

### 集群规划

| 机器        | 服务              |
|-----------|-----------------|
| hadoop101 | Master & Worker |
| hadoop102 | Worker          |
| hadoop103 | Worker          |

### 安装使用
解压  
```shell
tar -zxvf spark-3.3.1-bin-hadoop3.tgz
mv spark-3.3.1-bin-hadoop3 /opt/module/spark-standalone
```
配置Master
```shell
cp spark-env.sh.template spark-env.sh
vim spark-env.sh

SPARK_MASTER_HOST=hadoop101
SPARK_MASTER_PORT=7077
```
配置Worker
```shell
cp workers.template workers
vim workers

hadoop101
hadoop102
hadoop103
```
启动集群
```shell
sbin/start-all.sh
```

## Yarn 模式

### 安装使用
解压  
```shell
tar -zxvf spark-3.3.1-bin-hadoop3.tgz
mv spark-3.3.1-bin-hadoop3 /opt/module/spark-yarn
```
配置YARN信息
```shell
cp spark-env.sh.template spark-env.sh
vim spark-env.sh

YARN_CONF_DIR=/opt/module/hadoop/etc/hadoop
```
配置历史服务器  
```shell
cp spark-defaults.conf.template spark-defaults.conf
vim spark-defaults.conf
```