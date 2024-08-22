# Kafka分布式部署

## 集群规划

|hadoop101|hadoop102|hadoop103|
|---|---|---|
|zk    |zk|    zk|
|kafka|    kafka    |kafka|

## 集群部署
下载地址: http://kafka.apache.org/downloads.html

### 前置准备

Zookeeper集群安装部署

### 解压
```shell
tar -zxvf kafka_2.12-3.3.1.tgz -C /opt/module/

mv /opt/module/kafka_2.12-3.3.1 /opt/module/kafka
```

### 修改配置文件
```shell
vim /opt/module/kafka/config/server.properties
```

```properties
#broker的全局唯一编号，不能重复，只能是数字。（每个节点单独配置）
broker.id=1

#broker对外暴露的IP和端口 （每个节点单独配置）
advertised.listeners=PLAINTEXT://hadoop101:9092
#处理网络请求的线程数量
num.network.threads=3
#用来处理磁盘IO的线程数量
num.io.threads=8
#发送套接字的缓冲区大小
socket.send.buffer.bytes=102400
#接收套接字的缓冲区大小
socket.receive.buffer.bytes=102400
#请求套接字的缓冲区大小
socket.request.max.bytes=104857600
#kafka运行日志(数据)存放的路径
log.dirs=/opt/module/kafka/datas
#topic在当前broker上的分区个数
num.partitions=1
#用来恢复和清理data下数据的线程数量
num.recovery.threads.per.data.dir=1
# 每个topic创建时的副本数，默认时1个副本
offsets.topic.replication.factor=1
#segment文件保留的最长时间，超时将被删除
log.retention.hours=168
#每个segment文件的大小，默认最大1G
log.segment.bytes=1073741824
# 检查过期数据的时间，默认5分钟检查一次是否数据过期
log.retention.check.interval.ms=300000
#配置连接Zookeeper集群地址（在zk根目录下创建/kafka，方便管理）
zookeeper.connect=hadoop101:2181,hadoop102:2181,hadoop103:2181/kafka
```

### 分发Kafka

```shell
scp -r /opt/module/kafka hadoop@hadoop102:/opt/module/kafka
scp -r /opt/module/kafka hadoop@hadoop103:/opt/module/kafka
```

修改配置项
```properties
# hadoop102
broker.id=2
advertised.listeners=PLAINTEXT://hadoop102:9092
```

```properties
# hadoop103
broker.id=3
advertised.listeners=PLAINTEXT://hadoop103:9092
```

### 配置环境变量

```shell
sudo vim /etc/profile.d/hadoop_env.sh

#KAFKA_HOME
export KAFKA_HOME=/opt/module/kafka
export PATH=$PATH:$KAFKA_HOME/bin

source /etc/profile
```

### 启动集群

```shell
# 依次在hadoop101、hadoop102、hadoop103启动zookeeper
/opt/module/zookeeper/bin/zkServer.sh start

# 依次在hadoop101、hadoop102、hadoop103启动Kafka
/opt/module/kafka/bin/kafka-server-start.sh -daemon /opt/module/kafka/config/server.properties
```

### 关闭集群

```shell
# 依次在hadoop101、hadoop102、hadoop103关闭Kafka集群
/opt/module/kafka/bin/kafka-server-stop.sh 
```

### 查看进程

```
--------- hadoop101 ----------
3768 QuorumPeerMain
4251 Kafka
4349 Jps
--------- hadoop102 ----------
4769 Kafka
4292 QuorumPeerMain
4878 Jps
--------- hadoop103 ----------
3298 Jps
3206 Kafka
2719 QuorumPeerMain
```