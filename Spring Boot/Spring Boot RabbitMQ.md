## Spring Boot RabbitMQ


### 依赖配置
```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

### application配置

```
spring:
  rabbitmq:
    host: localhost # rabbitmq的连接地址
    port: 5672 # rabbitmq的连接端口号
    virtual-host: /mall # rabbitmq的虚拟host,一般采用应用名称
    username: mall # rabbitmq的用户名
    password: mall # rabbitmq的密码
#    publisher-confirms: true #如果对异步消息需要回调必须设置为true
```

### 配置文件

```
@Configuration
public class RabbitMqConfig {

    public static final String DIRECT_QUEUE = "direct.queue";

    public static final String TOPIC_QUEUE = "topic.queue";
    public static final String TOPIC_EXCHANGE = "topicExchange";

    public static final String FANOUT_QUEUE = "fanout.queue";
    public static final String FANOUT_EXCHANGE = "fanoutExchange";

    /**
     * MessageConverter用于将Java对象转换为RabbitMQ的消息。默认情况下，
     * Spring Boot使用SimpleMessageConverter，只能发送String和byte[]类型的消息，不太方便。
     * 使用Jackson2JsonMessageConverter，我们就可以发送JavaBean对象，由Spring Boot自动序列化为JSON并以文本消息传递。
     */
    @Bean
    public MessageConverter createMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    /**
     * Direct 模式
     * @return Queue
     */
    @Bean
    public Queue queue() {
        return new Queue(DIRECT_QUEUE, true);
    }


    /**
     * Topic 模式
     * @return Queue
     */
    @Bean
    public Queue topicQueue() {
        return new Queue(TOPIC_QUEUE, true);
    }

    @Bean
    public TopicExchange topicExchange(){
        return new TopicExchange(TOPIC_EXCHANGE);
    }

    @Bean
    public Binding topicBinding() {
        return BindingBuilder.bind(topicQueue()).to(topicExchange()).with("topic.#");
    }

    /**
     * Fanout 模式
     * @return Queue
     */
    @Bean
    public Queue fanoutQueue() {
        return new Queue(FANOUT_QUEUE, true);
    }

    @Bean
    public FanoutExchange fanoutExchange(){
        return new FanoutExchange(FANOUT_EXCHANGE);
    }

    @Bean
    public Binding FanoutBinding() {
        return BindingBuilder.bind(fanoutQueue()).to(fanoutExchange());
    }
}
```


### 生产者

定义Message实体类
```
@Data
public class Message {
    private Integer code;
    private String message;

    public Message() {
    }

    public Message(Integer code, String message) {
        this.code = code;
        this.message = message;
    }
}
```

生产者示例
```
@Service
public class MessageSender {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void sendDirect(Integer code, String message) {
        rabbitTemplate.convertAndSend(RabbitMqConfig.DIRECT_QUEUE, new Message(code, message));
    }

    public void sendTopic(Integer code, String message) {
        rabbitTemplate.convertAndSend(RabbitMqConfig.TOPIC_EXCHANGE, RabbitMqConfig.TOPIC_QUEUE, new Message(code, message));
    }
}
```

### 消费者
```
@Slf4j
@Component
public class MessageListener {

    @RabbitListener(queues = RabbitMqConfig.DIRECT_QUEUE)
    public void receiveDirect(@Payload Message message, @Headers Map<String,Object> headers, Channel channel) throws IOException {
        log.info("消息接收 message code:{}", message.getCode());
        Long deliveryTag = (Long) headers.get(AmqpHeaders.DELIVERY_TAG);

        channel.basicAck(deliveryTag, false);
    }

    @RabbitListener(queues = RabbitMqConfig.TOPIC_QUEUE)
    public void receiveTopic(@Payload Message message, @Headers Map<String,Object> headers, Channel channel) throws IOException {
        log.info("消息接收 message code:{}", message.getCode());
        /**
         * Delivery Tag 用来标识信道中投递的消息。RabbitMQ 推送消息给 Consumer 时，会附带一个 Delivery Tag，
         * 以便 Consumer 可以在消息确认时告诉 RabbitMQ 到底是哪条消息被确认了。
         * RabbitMQ 保证在每个信道中，每条消息的 Delivery Tag 从 1 开始递增。
         */
        Long deliveryTag = (Long) headers.get(AmqpHeaders.DELIVERY_TAG);
        /**
         *  multiple 取值为 false 时，表示通知 RabbitMQ 当前消息被确认
         *  如果为 true，则额外将比第一个参数指定的 delivery tag 小的消息一并确认
         */
        channel.basicAck(deliveryTag, false);
    }
}
```