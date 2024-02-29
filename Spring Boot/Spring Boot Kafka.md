## Spring Boot 整合 Kafka

### 依赖配置
Spring Boot 版本和 Spring-Kafka 的版本对应关系：https://spring.io/projects/spring-kafka

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
```

### application 配置

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    # 生产者配置
    producer:
      retries: 0
      batch-size: 16384
      buffer-memory: 33554432
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
    # 消费者配置
    consumer:
      group-id: spring-boot-mq-kafka
      # 手动提交
      enable-auto-commit: false
      auto-offset-reset: latest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      properties:
        session.timeout.ms: 60000
    listener:
      log-container-config: false
      concurrency: 5
      # 手动提交
      ack-mode: manual_immediate
```
### KafkaConfig

```java
@Configuration
@EnableConfigurationProperties({KafkaProperties.class})
@EnableKafka
@AllArgsConstructor
public class KafkaConfig {
    private final KafkaProperties kafkaProperties;

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }

    @Bean
    public ProducerFactory<String, String> producerFactory() {
        return new DefaultKafkaProducerFactory<>(kafkaProperties.buildProducerProperties());
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, String> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.setConcurrency(KafkaConsts.DEFAULT_PARTITION_NUM);
        factory.setBatchListener(true);
        factory.getContainerProperties().setPollTimeout(3000);
        return factory;
    }

    @Bean
    public ConsumerFactory<String, String> consumerFactory() {
        return new DefaultKafkaConsumerFactory<>(kafkaProperties.buildConsumerProperties());
    }

    @Bean("ackContainerFactory")
    public ConcurrentKafkaListenerContainerFactory<String, String> ackContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, String> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
        factory.setConcurrency(KafkaConsts.DEFAULT_PARTITION_NUM);
        return factory;
    }
}
```

### Kafka常量

```java
public interface KafkaConstants {

    /**
     * 默认分区大小
     */
    Integer DEFAULT_PARTITION_NUM = 3;

    /**
     * Topic 名称
     */
    String TOPIC_NAME_TEST = "test";
}
```

### 发布消息

```
@Slf4j
@RestController
public class SendMessageController {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @GetMapping("/send/{message}")
    public void send(@PathVariable String message) {
        log.info(message);
        this.kafkaTemplate.send(KafkaConstants.TOPIC_NAME_TEST, message);
    }

    @GetMapping("/sendAndConfirm/{message}")
    public void sendAndConfirm(@PathVariable String message) {
        ListenableFuture<SendResult<String, String>> future = this.kafkaTemplate.send(KafkaConstants.TOPIC_NAME_TEST, message);
        future.addCallback(new ListenableFutureCallback<SendResult<String, String>>() {
            @Override
            public void onSuccess(SendResult<String, String> result) {
                log.info("成功发送消息：{}，offset=[{}]", message, result.getRecordMetadata().offset());
            }

            @Override
            public void onFailure(Throwable ex) {
                log.error("消息：{} 发送失败，原因：{}", message, ex.getMessage());
            }
        });
    }
}
```

### 消息监听

```java
@Slf4j
@Component
public class MessageListener {

    @KafkaListener(topics = KafkaConstants.TOPIC_NAME_TEST, containerFactory = "ackContainerFactory")
    public void handleMessage(ConsumerRecord record, Acknowledgment acknowledgment) {
        try {
            String message = (String) record.value();
            log.info("收到消息: {}", message);
        } catch (Exception e) {
            log.error(e.getMessage(), e);
        } finally {
            // 手动提交 offset
            acknowledgment.acknowledge();
        }
    }
}
```