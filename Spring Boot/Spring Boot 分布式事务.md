# Spring Boot 分布式事务

## 背景
在微服务架构中，业务逻辑常被拆分为多个独立服务，各服务拥有专属数据库。
这种设计提升了系统灵活性与可扩展性，但也带来了数据一致性的挑战。尤其在分布式场景下，如何保证跨服务的事务一致性成为关键问题

## 常见场景与问题
典型的业务场景如电商下单：需要同时处理订单服务（写订单表）、库存服务（扣减库存）和支付服务（生成支付记录）。
若其中一个服务失败，需保证所有操作回滚，否则会出现数据不一致（如扣了库存但未生成订单）。
传统单体应用可通过本地事务（如Spring的@Transactional）保证ACID，但微服务中数据库分散，无法直接使用本地事务。

## 解决方案与实践

### 两阶段提交（2PC）(不推荐)
2PC是一种强一致性协议，但存在性能瓶颈和阻塞风险。
在SpringBoot中可通过JTA（Java Transaction API）实现，但通常需依赖外部事务管理器（如Narayana、Atomikos）。
代码示例:

```java
@Transactional
public void placeOrder(OrderRequest request) {
    // 阶段一：预提交
    orderService.prepare(request);
    inventoryService.prepareDeduct(request);
    paymentService.prepareCharge(request);
    
    // 阶段二：提交/回滚
    if (allPreparedSuccess) {
        orderService.commit();
        inventoryService.commit();
        paymentService.commit();
    } else {
        // 统一回滚
        orderService.rollback();
        inventoryService.rollback();
        paymentService.rollback();
    }
}
```
缺点：不适合高并发场景，且需各服务支持XA协议。

### 最终一致性方案(推荐使用)

1. 本地消息表（异步确保）  
   在业务数据库中创建消息表，与业务操作在同一事务中写入消息记录，后通过定时任务推送消息至其他服务。
```java
@Service
public class OrderService {
    @Autowired
    private MessageRepository messageRepo;

    @Transactional
    public void createOrder(Order order) {
        // 1. 写订单表
        orderRepo.save(order);
        // 2. 同一事务中写入消息表
        messageRepo.save(new Message("INVENTORY_DEDUCT", order.getProductId()));
    }
}

// 定时任务扫描消息表并发送至MQ
@Scheduled(fixedDelay = 5000)
public void pollMessages() {
    List<Message> messages = messageRepo.findUnsent();
    messages.forEach(msg -> rabbitTemplate.convertAndSend("exchange", "key", msg));
}
```

2. 事件驱动（Pub/Sub模式）  
   借助消息中间件（如RabbitMQ、Kafka）实现解耦

生产者
```java
@EnableBinding(Source.class)
public class OrderService {
    @Autowired
    private Source source;
    
    @Transactional
    public void createOrder(Order order) {
        orderRepo.save(order);
        // 发送事件至MQ
        source.output().send(MessageBuilder.withPayload(order).build());
    }
}
```

消费者
```java
@EnableBinding(Sink.class)
public class InventoryService {
    @StreamListener(Sink.INPUT)
    public void deductInventory(Order order) {
        inventoryRepo.deduct(order.getProductId());
    }
}
```
需处理消息重复消费（幂等设计）和消息丢失（重试机制）问题。

## TCC补偿事务 (适用复杂业务)

TCC（Try-Confirm-Cancel）适用于需要强一致性的场景。各服务需实现三个阶段：

- Try：预留资源（如冻结库存）
- Confirm：确认操作（扣减真实库存）
- Cancel：取消操作（释放冻结）

SpringBoot中可通过自定义注解和AOP实现：
```java
// 定义TCC注解
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface TccAction {
    String confirmMethod();
    String cancelMethod();
}

// 切面处理TCC逻辑
@Aspect
@Component
public class TccAspect {
    @Around("@annotation(tccAction)")
    public Object around(ProceedingJoinPoint pjp, TccAction tccAction) {
        try {
            // 执行Try阶段
            Object result = pjp.proceed();
            // 记录日志用于后续Confirm/Cancel
            tccLogService.logTryPhase();
            return result;
        } catch (Exception e) {
            // 触发Cancel
            invokeCancelMethod(tccAction.cancelMethod());
            throw e;
        }
    }
}
```

## 容错与监控

幂等设计：为所有操作生成唯一ID（如UUID），避免重复处理。
重试机制：使用Spring Retry或Resilience4j实现异步重试。
分布式追踪：集成Sleuth+Zipkin，定位数据不一致问题。
人工干预通道：提供补偿查询接口，用于异常时手动修复。


## 总结
在Java+SpringBoot微服务体系中，保障数据一致性需根据业务场景选择方案：

- 低频率强一致性：TCC或2PC
- 高频率最终一致性：事件驱动+消息队列
- 简单场景：本地消息表
- 最终一致性是微服务架构中的主流选择，通过异步化和幂等设计，在保证系统吞吐量的同时实现数据可靠同步。

核心建议：在业务设计初期明确一致性要求，选择合适模式并配套监控措施，避免过度设计。