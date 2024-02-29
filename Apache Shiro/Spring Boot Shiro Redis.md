## Spring Boot Shiro Redis

在Shiro中加入缓存可以避免频繁访问数据库获取权限信息

### 引入依赖

```xml
<dependency>
    <groupId>org.crazycake</groupId>
    <artifactId>shiro-redis</artifactId>
    <version>3.3.1</version>
</dependency>
```

### applocation配置

```yaml
spring:
  redis:
    host: localhost
    port: 6379
    pool:
      max-active: 8
      max-wait: -1
      max-idle: 8
      min-idle: 0
    timeout: 0
```

### ShiroConfig配置

```java
public RedisManager redisManager() {
    return new RedisManager();
}

public RedisCacheManager cacheManager() {
    RedisCacheManager redisCacheManager = new RedisCacheManager();
    redisCacheManager.setRedisManager(redisManager());
    return redisCacheManager;
}
```

然后将SecurityManager中加入RedisCacheManager

```java
@Bean  
public SecurityManager securityManager(){  
    DefaultWebSecurityManager securityManager =  new DefaultWebSecurityManager();
    // ...
    securityManager.setCacheManager(cacheManager());
    return securityManager;  
}
```
