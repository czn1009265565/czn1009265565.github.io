# Spring Boot 实现分布式事务

## 核心依赖

```xml
<dependency>
    <groupId>org.apache.shardingsphere</groupId>
    <artifactId>sharding-jdbc-spring-boot-starter</artifactId>
    <version>4.1.1</version>
</dependency>

<!-- 使用XA事务时，需要引入此模块 -->
<dependency>
    <groupId>org.apache.shardingsphere</groupId>
    <artifactId>sharding-transaction-xa-core</artifactId>
    <version>4.1.1</version>
</dependency>

<!-- 使用BASE事务时，需要引入此模块 -->
<!-- <dependency>
    <groupId>org.apache.shardingsphere</groupId>
    <artifactId>sharding-transaction-base-seata-at</artifactId>
    <version>4.1.1</version>
</dependency> -->
```

## 配置事务管理器

```java
@Configuration
@EnableTransactionManagement
public class TransactionConfiguration {

    @Bean
    public PlatformTransactionManager txManager(final DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }

    @Bean
    public JdbcTemplate jdbcTemplate(final DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```

## 代码中使用分布式事务

```java
public interface UserService {

    @Transactional
    @ShardingTransactionType(TransactionType.XA)
    void save(List<UserDO> userDOList);
}
```