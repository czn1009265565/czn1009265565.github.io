## Kafka 集群搭建
Kafka 是消息引擎系统，也是分布式流处理平台!

1. 异步
2. 解耦
3. 削峰

### 版本演进
1. 0.7版本：只提供了最基础的消息队列功能。

2. 0.8版本：引入了副本机制，至此kafka成为了一个真正意义上完备的分布式高可靠消息队列解决方案。

3. 0.9.0.0版本：增加了基础的安志认证/权限功能；使用java重写了此版本消费者API；引入了kafka connect组件。

4. 0.10.0.0版本：引入了Kafka Streams，正式升级成分布式流处理平台。

5. 0.11.0.0版本：提供了幂等性Producer API；对kafka消息格式做了重构。

6. 1.0和2.0版本：主要还是kafka streams的各种改进


### 线上集群部署
1. 修改hosts文件
	```
	10.192.77.203 zookeeper001
	10.192.77.203 zookeeper002
	10.192.77.203 zookeeper003

	10.192.77.203 kafka001
	10.192.77.203 kafka002
	10.192.77.203 kafka003
	```

1. 解压
	```
	$ tar -zxvf kafka_2.12-2.8.1.tgz

	$ mv kafka_2.12-2.8.1 /usr/local/kafka
	```
2. 修改部分配置
	```
	# cp server.properties server-1.properties
	# cp server.properties server-2.properties
	# cp server.properties server-3.properties
	```
	1. server-1.properties
		```
		# The id of the broker. 集群中每个节点的唯一标识
		broker.id=0
		# 监听地址
		listeners=PLAINTEXT://kafka001:9092
		# 数据的存储位置
		log.dirs=/usr/local/kafka-logs/00
		# Zookeeper连接地址
		zookeeper.connect=zookeeper001:2181,zookeeper002:2182,zookeeper003:2183
		```
	
	2. server-2.properties
		```
		broker.id=1
		listeners=PLAINTEXT://kafka002:9093
		log.dirs=/usr/local/kafka-logs/01
		zookeeper.connect=zookeeper001:2181,zookeeper002:2182,zookeeper003:2183
		```
	3. server-3.properties
		```
		broker.id=2
		listeners=PLAINTEXT://kafka003:9094
		log.dirs=/usr/local/kafka-logs/02
		zookeeper.connect=zookeeper001:2181,zookeeper002:2182,zookeeper003:2183
		```
3. 启动集群
	```
	$ bin/kafka-server-start.sh -daemon config/server-1.properties
	$ bin/kafka-server-start.sh -daemon config/server-2.properties
	$ bin/kafka-server-start.sh -daemon config/server-3.properties
	```
注意点:

Kafka Tools远程连接需要配置 hosts文件(远程机需要能够连接到Kafka配置文件中的`zookeeper.connect`)
```
10.192.77.203 kafka001
10.192.77.203 kafka002
10.192.77.203 kafka003
```

### 参数调优
#### Broker 端参数
- log.dirs:这是非常重要的参数，指定了 Broker 需要使用的若干个文件目录路径,例如`/home/kafka1,/home/kafka2,/home/kafka3`,必须指定!!!
- log.dir:注意这是 dir，结尾没有 s，说明它只能表示单个路径，它是补充上一个参数用的。
- zookeeper.connect:`zk1:2181,zk2:2181,zk3:2181`,当存在多个Kafka集群试用同个zookeeper集群时参数可以这样指定`zk1:2181,zk2:2181,zk3:2181/kafka1`,`zk1:2181,zk2:2181,zk3:2181/kafka2`
- listeners:`PLAINTEXT://localhost:9092` 用于对内发布,内网ip
- advertised.listeners:监听器是 Broker 用于对外发布,例如公网ip
- auto.create.topics.enable：是否允许自动创建 Topic,建议false
- unclean.leader.election.enable：是否允许 Unclean Leader 选举,建议false(如果设置成ture)
- auto.leader.rebalance.enable：是否允许定期进行 Leader 选举,建议false(更换Leader代价很高,且没有性能收益)
- log.retention.{hour|minutes|ms}：这是个"三兄弟"，都是控制一条消息数据被保存多长时间。从优先级上来说 ms 设置最高、minutes 次之、hour 最低。
- log.retention.bytes：这是指定 Broker 为消息保存的总磁盘容量大小,默认-1,表示无限大
- message.max.bytes：控制 Broker 能够接收的最大消息大小。

#### Topic 参数
优先级高于Broker端参数

- retention.ms：规定了该 Topic 消息被保存的时长。默认是 7 天，即该 Topic 只保存最近 7 天的消息。一旦设置了这个值，它会覆盖掉 Broker 端的全局参数值。
- retention.bytes：规定了要为该 Topic 预留多大的磁盘空间。和全局参数作用相似，这个值通常在多租户的 Kafka 集群中会有用武之地。当前默认值是 -1，表示可以无限使用磁盘空间。

- message.max.bytes：控制 Topic 能够接收的最大消息大小。

#### JVM 参数
- KAFKA_HEAP_OPTS：指定堆大小。默认1G,推荐6G
- KAFKA_JVM_PERFORMANCE_OPTS：指定 GC 参数。设置G1即可

启动前设置环境变量即可
```
$> export KAFKA_HEAP_OPTS="-Xms6g -Xmx6g"
$> export KAFKA_JVM_PERFORMANCE_OPTS="-server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:+ExplicitGCInvokesConcurrent -Djava.awt.headless=true"
$> bin/kafka-server-start.sh config/server.properties
```
