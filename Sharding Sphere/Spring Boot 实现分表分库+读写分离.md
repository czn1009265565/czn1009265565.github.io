# 1-5 Spring Boot 实现分表分库+读写分离

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

#打印sql
spring.shardingsphere.props.sql.show=true

spring.shardingsphere.datasource.names=master0,slave0,master1,slave1

spring.shardingsphere.datasource.master0.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.master0.driver-class-name=com.mysql.cj.jdbc.Driver
spring.shardingsphere.datasource.master0.jdbc-url=jdbc:mysql://localhost:3306/master0?characterEncoding=utf-8
spring.shardingsphere.datasource.master0.username=root
spring.shardingsphere.datasource.master0.password=Admin123.

spring.shardingsphere.datasource.slave0.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.slave0.driver-class-name=com.mysql.cj.jdbc.Driver
spring.shardingsphere.datasource.slave0.jdbc-url=jdbc:mysql://localhost:3306/slave0?characterEncoding=utf-8
spring.shardingsphere.datasource.slave0.username=root
spring.shardingsphere.datasource.slave0.password=Admin123.

spring.shardingsphere.datasource.master1.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.master1.driver-class-name=com.mysql.cj.jdbc.Driver
spring.shardingsphere.datasource.master1.jdbc-url=jdbc:mysql://localhost:3306/master1?characterEncoding=utf-8
spring.shardingsphere.datasource.master1.username=root
spring.shardingsphere.datasource.master1.password=Admin123.

spring.shardingsphere.datasource.slave1.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.slave1.driver-class-name=com.mysql.cj.jdbc.Driver
spring.shardingsphere.datasource.slave1.jdbc-url=jdbc:mysql://localhost:3306/slave1?characterEncoding=utf-8
spring.shardingsphere.datasource.slave1.username=root
spring.shardingsphere.datasource.slave1.password=Admin123.

#根据年龄分库
spring.shardingsphere.sharding.default-database-strategy.inline.sharding-column=age
spring.shardingsphere.sharding.default-database-strategy.inline.algorithm-expression=master$->{age % 2}
#根据id分表
spring.shardingsphere.sharding.tables.tab_user.actual-data-nodes=master$->{0..1}.tab_user$->{0..1}
spring.shardingsphere.sharding.tables.tab_user.table-strategy.inline.sharding-column=id
spring.shardingsphere.sharding.tables.tab_user.table-strategy.inline.algorithm-expression=tab_user$->{id % 2}

#指定master0为主库，slave0为它的从库
spring.shardingsphere.sharding.master-slave-rules.master0.master-data-source-name=master0
spring.shardingsphere.sharding.master-slave-rules.master0.slave-data-source-names=slave0
#指定master1为主库，slave1为它的从库
spring.shardingsphere.sharding.master-slave-rules.master1.master-data-source-name=master1
spring.shardingsphere.sharding.master-slave-rules.master1.slave-data-source-names=slave1
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