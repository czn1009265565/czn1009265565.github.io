# Spring Boot 分布式锁

锁，解决的是多线程或多进程情况下的数据一致性问题；分布式锁，解决的是分布式集群下的数据一致性问题。

## Redis与Zookeeper区别

Redis与Zookeeper均可以实现分布式锁，但各有其优缺点。

### Redis

Redis 分布式锁适用于对性能要求较高的场景，例如短期的锁定操作、高并发请求和对并发性能有较高要求的情况。
由于Redis的简单性和高性能，它在大多数场景下都是一个不错的选择。
但需要注意的是，由于Redis是内存数据库，如果持有锁的客户端发生故障或网络问题，可能会导致锁丢失或死锁的问题。

### ZooKeeper

ZooKeeper 分布式锁适用于对可靠性和顺序性要求较高的场景。它提供了强一致性和顺序性的保证，适用于需要严格的锁顺序访问的场景。
ZooKeeper的分布式锁实现相对复杂一些，但提供了更多的功能和保证，如阻塞等待、超时处理、重入锁等。如果你的应用程序需要这些高级功能，ZooKeeper是一个较好的选择。
但需要注意的是，ZooKeeper的部署和维护相对复杂，并且性能较低，因此在对性能要求较高的场景下可能不太适合使用。

## Spring Boot Redisson

### 依赖配置

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.23.3</version>
</dependency>
```

### 配置项

```
# common spring boot settings
spring.redis.database=0
spring.redis.host=127.0.0.1
spring.redis.port=6379
#spring.redis.password=
#spring.redis.ssl=
spring.redis.timeout=300ms
#spring.redis.cluster.nodes=
#spring.redis.sentinel.master=
#spring.redis.sentinel.nodes=
```

### 实现
#### 分布式锁注解

```java
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
public @interface RedisLock {

    String key() default "";
}
```

#### AOP实现

```java
@Slf4j
@Aspect
@Component
public class RedisLockAspect {

    @Pointcut("@annotation(com.example.springbootredisson.annotation.RedisLock)")
    public void pointCut(){}

    @Resource
    private RedissonClient redissonClient;


    @Around("pointCut()")
    public Object doAround(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = null;
        Method method = getMethod(joinPoint);
        RedisLock annotation = method.getAnnotation(RedisLock.class);
        String key = annotation.key();
        RLock lock = redissonClient.getLock(key);
        try {
            if (!lock.tryLock(1, TimeUnit.SECONDS)) {
                throw new RuntimeException("[RedisLock] lock is take up");
            }
            result = joinPoint.proceed();
        } catch (Exception e) {
            log.error("[RedisLock Error] ", e);
        } finally {
            lock.unlock();
        }
        return result;
    }

    /** 获取当前执行的方法 */
    private Method getMethod(ProceedingJoinPoint point) throws NoSuchMethodException {
        MethodSignature methodSignature = (MethodSignature) point.getSignature();
        Method method = methodSignature.getMethod();
        return point.getTarget().getClass().getMethod(method.getName(), method.getParameterTypes());
    }
}
```

#### ProductService
```java
@Slf4j
@Service
public class ProductService {

    @Resource
    private RedissonClient redissonClient;

    @Resource
    private RedisService redisService;

    @PostConstruct
    private void init() {
        // 初始化库存
        redisService.set("product:0", 100);
    }

    public void nonLockSecKill() {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (Exception ignore){
        }

        //减库存
        int stock = (int) redisService.get("product:0");
        if (stock <= 0) {
            throw new RuntimeException("[secKill] stock is empty");
        }
        Long decr = redisService.decr("product:0", 1);
        log.info("[secKill] 扣减成功，剩余库存:" + decr);
    }

    public void handLockSecKill() {
        RLock lock = redissonClient.getLock("key:product:0");
        try {
            if (!lock.tryLock(1, TimeUnit.SECONDS)) {
                throw new RuntimeException("[secKill] lock is take up");
            }
            //减库存
            nonLockSecKill();
        } catch (Exception e) {
            log.error("[secKill] ", e);
        } finally {
            lock.unlock();
        }
    }

    @RedisLock(key="key:product")
    public void autoLockSecKill() {
        nonLockSecKill();
    }
}
```

#### SecKillController

```java
@Slf4j
@RestController
public class SecKillController {

    @Resource
    private ProductService productService;

    @GetMapping("/handLockSecKill")
    public String handLockSecKill() throws InterruptedException {
        productService.handLockSecKill();
        return "success";
    }

    @GetMapping("/autoLockSecKill")
    public String autoLockSecKill() throws InterruptedException {
        productService.autoLockSecKill();
        return "success";
    }
}
```

## Spring Boot Zookeeper

### 依赖配置

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-aop</artifactId>
    </dependency>

    <!-- curator 版本4.1.0 对应 zookeeper 版本 3.5.x -->
    <!-- curator 与 zookeeper 版本对应关系：https://curator.apache.org/zk-compatibility.html -->
    <dependency>
        <groupId>org.apache.curator</groupId>
        <artifactId>curator-recipes</artifactId>
        <version>4.1.0</version>
    </dependency>

    <dependency>
        <groupId>cn.hutool</groupId>
        <artifactId>hutool-all</artifactId>
    </dependency>

    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```


