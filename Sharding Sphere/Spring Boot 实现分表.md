# Spring Boot 实现分表

## 核心依赖

```xml
<properties>
	<java.version>11</java.version>
    <spring-boot-version>2.7.12</spring-boot-version>
    <mysql.version>8.0.28</mysql.version>
    <mybatis.version>2.2.1</mybatis.version>
    <mybatis.plus.version>3.5.1</mybatis.plus.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.apache.shardingsphere</groupId>
        <artifactId>sharding-jdbc-spring-boot-starter</artifactId>
        <version>4.1.1</version>
    </dependency>

    <dependency>
        <groupId>org.apache.shardingsphere</groupId>
        <artifactId>sharding-jdbc-spring-namespace</artifactId>
        <version>4.1.1</version>
    </dependency>

    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>${mysql.version}</version>
    </dependency>

    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>${mybatis.version}</version>
    </dependency>

    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-boot-starter</artifactId>
        <version>${mybatis.plus.version}</version>
    </dependency>
</dependencies>
```

## application配置项

```
server.port=8088

#指定mybatis信息
mybatis.mapper-locations=classpath:mapper/*.xml

spring.shardingsphere.datasource.names=master

# 数据源 主库
spring.shardingsphere.datasource.master.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.master.driver-class-name=com.mysql.jdbc.Driver
spring.shardingsphere.datasource.master.jdbc-url=jdbc:mysql://localhost:3306/master?characterEncoding=utf-8
spring.shardingsphere.datasource.master.username=root
spring.shardingsphere.datasource.master.password=Admin123.

#数据分表规则
#指定所需分的表
spring.shardingsphere.sharding.tables.tab_user.actual-data-nodes=master.tab_user$->{0..2}
#指定主键
spring.shardingsphere.sharding.tables.tab_user.table-strategy.inline.sharding-column=id
#分表规则为主键除以3取模
spring.shardingsphere.sharding.tables.tab_user.table-strategy.inline.algorithm-expression=tab_user$->{id % 3}

#打印sql
spring.shardingsphere.props.sql.show=true
```

## 代码实现

1. 实体类

```java
@Data
@TableName(value = "tab_user")
public class UserDO {
    @TableId
    private Long id;
    private String name;
    private String sex;
    private Integer age;
    private Date createTime;
    private Date updateTime;
    private Integer status;
}
```

2. Dao层

```java
@Mapper
public interface UserDao extends BaseMapper<UserDO> {
}
```

```java
@Repository
public class UserBatchDao extends ServiceImpl<UserDao, UserDO> {
}
```
