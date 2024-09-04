# Kafka设计

Kafka 是一个分布式流式处理平台

Kafka 主要有两大应用场景：

- 消息队列：建立实时流数据管道，以可靠地在系统或应用程序之间获取数据。
- 数据处理： 构建实时的流数据处理程序来转换或处理数据流。

## 架构

1. **`Broker`**：一台kafka服务器就是一个Broker。一个集群由多个Broker组成
2. **`Producer`**：消息生产者
3. **`Consumer`**：消息消费者
4. **`Consumer Group`**：消费者组，由多个Consumer组成。  
   - 消费者组内每个消费者负责消费不同分区的数据，一个分区只能由一个消费者消费
   - 消费者组之间互不影响
5. **`Topic`**：主题，Producer 将消息发送到特定的主题，Consumer 通过订阅特定的 Topic(主题) 来消费消息。
6. **`Partition`**：Partition 属于 Topic 的一部分。一个 Topic 可以有多个 Partition ，并且同一 Topic 下的 Partition 可以分布在不同的 Broker 上

![Kafka.png](imgs%2FKafka.png)

## 多副本机制（消息丢失）

- 每个Partition都有多个副本，均匀分布在不同节点。其中一个副本作为Leader，其余的作为Follower
- Leader负责处理分区的所有读写请求，Follower则仅仅从Leader复制数据
- 如果Leader失效，其中一个Follower会被选举为新的Leader

带来的好处:  

1. Kafka 通过给特定 Topic 指定多个 Partition, 而各个 Partition 可以分布在不同的 Broker 上, 这样便能提供比较好的并发能力（负载均衡）。
2. Partition 可以指定对应的 Replica 数, 这也极大地提高了消息存储的安全性, 提高了容灾能力，不过也相应的增加了所需要的存储空间。


## 顺序消费

Kafka 中发送 1 条消息的时候，可以指定 topic, partition, key,data（数据） 4 个参数。
发送消息的时候指定了 Partition 的话，所有消息都会被发送到指定的 Partition。
同一个 key 的消息也可以保证只发送到同一个 partition。

1. 1 个 Topic 只对应一个 Partition
2. 发送消息的时候指定 key或者Partition（推荐）


## 消息丢失

### 生产者消息丢失
生产者(Producer) 调用send方法发送消息之后，消息可能因为网络问题并没有发送过去。

解决方式:  

1. 设置Producer重试次数以及重试间隔
2. 添加回调函数，打印消息发送失败日志


### 消费者消息丢失

消息在被追加到 Partition(分区)的时候都会分配一个特定的偏移量（offset）。偏移量（offset)表示 Consumer 当前消费到的 Partition(分区)的所在的位置

当消费者拉取到了分区的某个消息之后，消费者会自动提交了 offset。
自动提交的话会有一个问题，当消费者刚拿到这个消息准备进行真正消费的时候，突然挂掉了，消息实际上并没有被消费，但是 offset 却被自动提交了。

解决方式:  
关闭自动提交 offset，每次在真正消费完消息之后再自己手动提交 offset (但也带来了重复消费问题)

### Kafka消息丢失
Kafka 为分区（Partition）引入了多副本（Replica）机制，
假如 leader 副本所在的 broker 突然挂掉，那么就要从 follower 副本重新选出一个 leader ，
但是 leader 的数据还有一些没有被 follower 副本的同步的话，就会造成消息丢失。

解决方式:  
1. 设置 replication.factor >= 3，这样表示每个分区(partition) 至少有 3 个副本

2. 设置 min.insync.replicas > 1，这样配置代表消息至少要被写入到 2 个副本才算是被成功发送，min.insync.replicas 的默认值为 1 ，在实际生产中应尽量避免默认值 1。

### 重复消费

kafka 出现消息重复消费的原因：

1. 服务端侧已经消费的数据没有成功提交 offset（主要原因）
2. Kafka 侧 由于服务端处理业务时间长或者网络链接等等原因让 Kafka 认为服务假死，触发了分区 rebalance。

解决方式:  
在业务端实现，任意多次执行所产生的影响均与一次执行的影响相同。例如每条消息都有唯一键标识