# Spring Boot Guava

## Guava Cache
### 简介
Guava Cache 是 google 开源的一款本地缓存工具库。  
![Guava Cache](./pictures/Guava%20Cache.png)

传统的JVM 缓存，是堆缓存，其实就是创建一些全局容器，例如：List、Set、Map、ConcurrentHashMap等。
这些容器可以存储数据，却不能按照一定的规则淘汰数据，如 LRU，LFU，FIFO 等，也没有清除数据时的回调通知。

### 适用场景

1. 对于访问速度有较大要求
2. 存储的数据不经常变化
3. 数据量不大，占用内存较小
4. 需要访问整个集合
5. 能够容忍数据不是实时的

### 引入依赖

```xml
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>33.3.1-jre</version>
</dependency>
```

### 容器创建

```java
public interface GuavaCacheService {

    void set(String key, Object value);

    Object get(String key);
}
```

```java
@Slf4j
@Service
public class GuavaCacheServiceImpl implements GuavaCacheService{
    private static Cache<String, Object> commonCache;

    static {
        commonCache = CacheBuilder.newBuilder()
                .initialCapacity(1000) // 初始容量
                .maximumSize(10000L)   // 设定最大容量
                .expireAfterWrite(30L, TimeUnit.MINUTES) // 设定写入过期时间
                .concurrencyLevel(8)  // 设置最大并发写操作线程数
                .recordStats() // 开启缓存执行情况统计
                .build();
    }

    @Override
    public void set(String key, Object value) {
        commonCache.put(key, value);
    }

    @Override
    public Object get(String key) {
        return commonCache.getIfPresent(key);
    }
}
```