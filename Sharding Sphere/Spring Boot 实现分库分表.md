# Spring Boot 实现分库分表

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

##打印sql
spring.shardingsphere.props.sql.show=true

spring.shardingsphere.datasource.names=ds0,ds1

spring.shardingsphere.datasource.ds0.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.ds0.driver-class-name=com.mysql.jdbc.Driver
spring.shardingsphere.datasource.ds0.jdbc-url=jdbc:mysql://localhost:3306/subdb0?characterEncoding=utf-8
spring.shardingsphere.datasource.ds0.username=root
spring.shardingsphere.datasource.ds0.password=Admin123.

spring.shardingsphere.datasource.ds1.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.ds1.driver-class-name=com.mysql.jdbc.Driver
spring.shardingsphere.datasource.ds1.jdbc-url=jdbc:mysql://localhost:3306/subdb1?characterEncoding=utf-8
spring.shardingsphere.datasource.ds1.username=root
spring.shardingsphere.datasource.ds1.password=Admin123.

# 根据年龄分库 groovy语法
spring.shardingsphere.sharding.default-database-strategy.inline.sharding-column=age
spring.shardingsphere.sharding.default-database-strategy.inline.algorithm-expression=ds$->{age % 2}
# 根据id分表 
spring.shardingsphere.sharding.tables.tab_user.actual-data-nodes=ds$->{0..1}.tab_user$->{0..2}
spring.shardingsphere.sharding.tables.tab_user.table-strategy.inline.sharding-column=id
spring.shardingsphere.sharding.tables.tab_user.table-strategy.inline.algorithm-expression=tab_user$->{id % 3}
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
