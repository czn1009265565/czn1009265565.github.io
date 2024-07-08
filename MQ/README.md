## 消息队列
MQ全称为Message Queue 消息队列（MQ）是一种应用程序对应用程序的通信方法。
MQ是消费-生产者模型的一个典型的代表，一端往消息队列中不断写入消息，而另一端则可以读取队列中的消息。
消息发布者只管把消息发布到 MQ 中而不用管谁来取，消息使用者只管从 MQ 中取消息而不管是谁发布的，这样发布者和使用者都不用知道对方的存在。

### 为什么使用消息队列

1. 异步: 邮件、短信等
2. 解耦: 事件监听
3. 削峰: 秒杀

### 带来的问题

1. 系统复杂度增加  
    - 消息丢失
    - 消息重复
    - 如何保证消息顺序
    - 数据一致性 （系统ABC同时监听消息队列Q，AB系统消费成功，C系统消费失败）
2. 系统可用性降低(系统引入的外部依赖越多，越容易挂掉。例如: MQ宕机导致整个业务不可用)


### 技术选型

| 对比    | RabbitMQ      | RocketMQ    | Kafka                        |
|-------|---------------|-------------|------------------------------|
| 单机吞吐  | 万级            | 10 万级，支撑高吞吐 | 10 万级以上，甚至有文献称，可以达到单机百万级TPS。 |
| 时延    | 微秒级，延迟最低      | 毫秒时延        | 毫秒时延                         |
| 可用性   | 高，基于主从架构实现高可用 | 非常高，分布式架构   | 非常高，分布式架构                    |
| 消息可靠性 | 基本不丢          | 可以做到 0 丢失   | 可以做到 0 丢失                    |

- RabbitMQ 适用于小型企业、项目
- Kafka适用于日志,埋点,监控,大数据,流处理
