# Kafka设计

Kafka是**一个分布式的基于发布/订阅模式的消息队列**，主要应用于大数据实时处理领域。

## 架构

1. **`Producer`**：消息生产者，就是向kafka broker发消息的客户端
2. **`Consumer`**：消息消费者，向kafka broker取消息的客户端
3. **`Consumer Group`**：消费者组，由多个consumer组成。**消费者组内每个消费者负责消费不同分区的数据，一个分区只能由一个消费者消费；消费者组之间互不影响**。所有的消费者都属于某个消费者组，即**消费者组是逻辑上的一个订阅者** 
4. **`Broker`**：一台kafka服务器就是一个broker。一个集群由多个broker组成。一个broker可以容纳多个topic。  
5. **`Topic`**：可以理解为一个队列，**生产者和消费者面向的都是一个topic**；  
6. **`Partition`**：分区，一个非常大的topic可以分布到多个broker（即服务器）上，**一个topic可以分为多个partition**，每个partition是一个有序的队列；  
7. **`Replication`**：副本，为保证集群中的某个节点发生故障时，**该节点上的partition数据不丢失，且kafka仍然能够继续工作**，kafka提供了副本机制，一个topic的每个分区都有若干个副本，一个leader和若干个follower。  
8. **`Leader`**：每个分区多个副本的“主”，生产者发送数据的对象，以及消费者消费数据的对象都是leader。  
9. **`Follower`**：每个分区多个副本中的“从”，实时从leader中同步数据，保持和leader数据的同步。leader发生故障时，某个follower会成为新的follower。

## 多副本机制（消息丢失）

- 每个Partition都有多个副本，均匀分布在不同节点。其中一个副本作为leader，其余的作为follower
- leader负责处理分区的所有读写请求，follower则从leader复制数据
- 如果leader失效，其中一个follower会自动晋升为新的leader