# Kafka设计

## 多副本机制（消息丢失）

- 每个Partition都有多个副本，其中一个副本作为leader，其余的作为follower
- leader负责处理分区的所有读写请求，follower则从leader复制数据
- 如果leader失效，其中一个follower会自动晋升为新的leader