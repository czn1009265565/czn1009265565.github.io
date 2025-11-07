# Spring Boot 分布式锁

锁，解决的是多线程或多进程情况下的数据一致性问题；分布式锁，解决的是分布式集群下的数据一致性问题。

## Redis与Zookeeper区别

[分布式锁](分布式/1-3 分布式锁.md)

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
        <groupId>org.apache.curator</groupId>
        <artifactId>curator-framework</artifactId>
        <version>5.5.0</version>
    </dependency>

    <dependency>
        <groupId>org.apache.curator</groupId>
        <artifactId>curator-recipes</artifactId>
        <version>5.5.0</version>
    </dependency>

    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

### 配置项

```ymal
spring:
  application:
    name: spring-boot-distribute-key

zookeeper:
  address: 127.0.0.1:2181  # ZooKeeper服务器地址
  session-timeout: 60000   # 会话超时（毫秒）
  connection-timeout: 15000 # 连接超时（毫秒）
  base-sleep-time: 1000
  max-retries: 3
```

### ZookeeperConfig

```java
@Configuration
@Slf4j
public class ZookeeperConfig {

    @Value("${zookeeper.address}")
    private String zkAddress;

    @Value("${zookeeper.session-timeout}")
    private int sessionTimeout;

    @Value("${zookeeper.connection-timeout}")
    private int connectionTimeout;

    @Value("${zookeeper.base-sleep-time}")
    private int baseSleepTime;

    @Value("${zookeeper.max-retries}")
    private int maxRetries;

    @Value("${spring.application.name}")
    private String applicationName;

    @Bean(initMethod = "start", destroyMethod = "close")
    public CuratorFramework curatorFramework() {
        RetryPolicy retryPolicy = new ExponentialBackoffRetry(
                baseSleepTime,
                maxRetries
        );

        CuratorFramework client = CuratorFrameworkFactory.builder()
                .connectString(zkAddress)
                .sessionTimeoutMs(sessionTimeout)
                .connectionTimeoutMs(connectionTimeout)
                .retryPolicy(retryPolicy)
                .namespace(applicationName)
                .build();

        // 添加连接状态监听
        client.getConnectionStateListenable().addListener((c, newState) -> {
            log.info("ZooKeeper连接状态变化: {}", newState);
            if (newState == ConnectionState.LOST) {
                log.error("ZooKeeper连接丢失");
            } else if (newState == ConnectionState.RECONNECTED) {
                log.info("ZooKeeper重新连接成功");
            }
        });

        return client;
    }
}
```


### DistributedLockService

分布式锁接口类定义

```java
public interface DistributedLockService {

    /**
     * 执行带锁的操作（互斥锁）
     */
    <T> T executeWithLock(String lockKey, long waitTime, TimeUnit timeUnit, Supplier<T> supplier);

    /**
     * 执行带锁的操作（无返回值）
     */
    void executeWithLock(String lockKey, long waitTime, TimeUnit timeUnit, Runnable runnable);

    /**
     * 执行读锁操作
     */
    <T> T executeWithReadLock(String lockKey, long waitTime, TimeUnit timeUnit, Supplier<T> supplier);

    /**
     * 执行写锁操作
     */
    <T> T executeWithWriteLock(String lockKey, long waitTime, TimeUnit timeUnit, Supplier<T> supplier);

    /**
     * 尝试获取锁（不阻塞）
     */
    boolean tryLock(String lockKey, long time, TimeUnit unit);

    /**
     * 释放锁
     */
    void unlock(String lockKey);
}
```

### ZookeeperDistributedLockServiceImpl

```java
@Slf4j
@Service
public class ZookeeperDistributedLockServiceImpl implements DistributedLockService {
    @Resource
    private CuratorFramework curatorFramework;

    private final Map<String, InterProcessLock> lockCache = new ConcurrentHashMap<>();
    private static final String LOCK_ROOT = "/distributed-locks";

    @Override
    public <T> T executeWithLock(String lockKey, long waitTime, TimeUnit timeUnit, Supplier<T> supplier) {
        String lockPath = buildLockPath("mutex", lockKey);
        InterProcessMutex lock = new InterProcessMutex(curatorFramework, lockPath);

        boolean acquired = false;
        long startTime = System.currentTimeMillis();

        try {
            log.debug("尝试获取锁: {}", lockPath);
            acquired = lock.acquire(waitTime, timeUnit);

            if (!acquired) {
                throw new RuntimeException("获取分布式锁超时: " + lockKey);
            }

            long lockTime = System.currentTimeMillis() - startTime;
            log.debug("成功获取锁: {}, 等待时间: {}ms", lockPath, lockTime);

            // 执行业务逻辑
            return supplier.get();

        } catch (Exception e) {
            log.error("执行业务逻辑异常, lockKey: {}", lockKey, e);
            throw new RuntimeException("业务执行失败: " + lockKey, e);
        } finally {
            if (acquired) {
                safeUnlock(lock, lockPath);
            }
        }
    }

    @Override
    public void executeWithLock(String lockKey, long waitTime, TimeUnit timeUnit, Runnable runnable) {
        executeWithLock(lockKey, waitTime, timeUnit, () -> {
            runnable.run();
            return null;
        });
    }

    @Override
    public <T> T executeWithReadLock(String lockKey, long waitTime, TimeUnit timeUnit, Supplier<T> supplier) {
        String lockPath = buildLockPath("rw", lockKey);
        InterProcessReadWriteLock rwLock = new InterProcessReadWriteLock(curatorFramework, lockPath);
        InterProcessMutex readLock = rwLock.readLock();

        boolean acquired = false;
        try {
            acquired = readLock.acquire(waitTime, timeUnit);
            if (!acquired) {
                throw new RuntimeException("获取读锁超时: " + lockKey);
            }

            log.debug("成功获取读锁: {}", lockPath);
            return supplier.get();

        } catch (Exception e) {
            log.error("读锁操作异常, lockKey: {}", lockKey, e);
            throw new RuntimeException("读锁操作失败: " + lockKey, e);
        } finally {
            if (acquired) {
                safeUnlock(readLock, lockPath);
            }
        }
    }

    @Override
    public <T> T executeWithWriteLock(String lockKey, long waitTime, TimeUnit timeUnit, Supplier<T> supplier) {
        String lockPath = buildLockPath("rw", lockKey);
        InterProcessReadWriteLock rwLock = new InterProcessReadWriteLock(curatorFramework, lockPath);
        InterProcessMutex writeLock = rwLock.writeLock();

        boolean acquired = false;
        try {
            acquired = writeLock.acquire(waitTime, timeUnit);
            if (!acquired) {
                throw new RuntimeException("获取写锁超时: " + lockKey);
            }

            log.debug("成功获取写锁: {}", lockPath);
            return supplier.get();

        } catch (Exception e) {
            log.error("写锁操作异常, lockKey: {}", lockKey, e);
            throw new RuntimeException("写锁操作失败: " + lockKey, e);
        } finally {
            if (acquired) {
                safeUnlock(writeLock, lockPath);
            }
        }
    }

    @Override
    public boolean tryLock(String lockKey, long time, TimeUnit unit) {
        String lockPath = buildLockPath("mutex", lockKey);
        InterProcessMutex lock = new InterProcessMutex(curatorFramework, lockPath);

        try {
            boolean acquired = lock.acquire(time, unit);
            if (acquired) {
                lockCache.put(lockKey, lock);
            }
            return acquired;
        } catch (Exception e) {
            log.error("尝试获取锁异常, lockKey: {}", lockKey, e);
            return false;
        }
    }

    @Override
    public void unlock(String lockKey) {
        InterProcessLock lock = lockCache.get(lockKey);
        if (lock != null) {
            safeUnlock(lock, buildLockPath("mutex", lockKey));
            lockCache.remove(lockKey);
        }
    }

    /**
     * 安全释放锁
     */
    private void safeUnlock(InterProcessLock lock, String lockPath) {
        try {
            if (lock != null && lock.isAcquiredInThisProcess()) {
                lock.release();
                log.debug("成功释放锁: {}", lockPath);
            }
        } catch (Exception e) {
            log.error("释放锁异常: {}", lockPath, e);
        }
    }

    /**
     * 构建锁路径
     */
    private String buildLockPath(String type, String key) {
        return LOCK_ROOT + "/" + type + "/" + key.replace("/", "-");
    }
}
```

### ProductService
稍作改造

```java
@Slf4j
@Service
public class ProductService {

    @Resource
    private DistributedLockService distributedLockService;

    /**
     * 线程不安全的
     */
    @Getter
    private Integer stock = 100;

    public void nonLockSecKill() {
        try {
            TimeUnit.MILLISECONDS.sleep(100);
        } catch (Exception ignore){
        }

        //减库存
        if (stock <= 0) {
            throw new RuntimeException("[secKill] stock is empty");
        }
        stock = stock - 1;
        log.info("[secKill] 扣减成功，剩余库存:" + stock);
    }

    public void handLockSecKill() {
        // 锁标识
        String lockKey = "product:0";
        try {
            // 尝试获取锁（等待最多5秒）
            if (distributedLockService.tryLock(lockKey, 5, TimeUnit.SECONDS)) {
                nonLockSecKill();
            } else {
                throw new RuntimeException("[secKill] lock is take up");
            }
        } finally {
            // 确保释放锁
            distributedLockService.unlock(lockKey);
        }
    }
}
```

