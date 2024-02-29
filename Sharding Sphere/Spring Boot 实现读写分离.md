# Spring Boot 实现读写分离

## 核心依赖

```xml
<properties>
    <java.version>11</java.version>
    <spring-boot-version>2.7.12</spring-boot-version>
    <mysql.version>8.0.28</mysql.version>
    <mybatis.version>2.2.1</mybatis.version>
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
</dependencies>
```

## application配置项


```
server.port=8088

#指定mybatis信息
mybatis.mapper-locations=classpath:mapper/*.xml

spring.shardingsphere.datasource.names=master,slave0

# 数据源 主库
spring.shardingsphere.datasource.master.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.master.driver-class-name=com.mysql.cj.jdbc.Driver
spring.shardingsphere.datasource.master.jdbc-url=jdbc:mysql://localhost:3306/master?characterEncoding=utf-8&useSSL=false
spring.shardingsphere.datasource.master.username=root
spring.shardingsphere.datasource.master.password=Admin123.

# 数据源 从库
spring.shardingsphere.datasource.slave0.type=com.zaxxer.hikari.HikariDataSource
spring.shardingsphere.datasource.slave0.driver-class-name=com.mysql.cj.jdbc.Driver
spring.shardingsphere.datasource.slave0.jdbc-url=jdbc:mysql://localhost:3306/slave0?characterEncoding=utf-8&useSSL=false
spring.shardingsphere.datasource.slave0.username=root
spring.shardingsphere.datasource.slave0.password=Admin123.

# 读写分离
spring.shardingsphere.masterslave.load-balance-algorithm-type=round_robin
spring.shardingsphere.masterslave.name=ms
spring.shardingsphere.masterslave.master-data-source-name=master
spring.shardingsphere.masterslave.slave-data-source-names=slave0

#打印sql
spring.shardingsphere.props.sql.show=true
```

## 代码实现

1. 实体类

```java
@Data
public class UserDO {
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
public interface UserDao {
    void insert(@Param("userDO") UserDO userDO);
    List<UserDO> selectAll();
}
```

3. Mapper实现

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.readwrite.dao.UserDao">
    <insert id="insert">
        insert into tab_user(id, name, sex, age, create_time, update_time, status)
        values (#{userDO.id}, #{userDO.name}, #{userDO.sex}, #{userDO.age}, now(), now(), #{userDO.status})
    </insert>
    <select id="selectAll" resultType="com.example.readwrite.entity.UserDO">
        select * from tab_user
    </select>
</mapper>
```

4. Controller层

```java
@RestController
@RequestMapping("user")
public class UserController {
    @Resource
    private UserDao userDao;

    @PostMapping(value = "save")
    public UserDO save(@RequestBody @Validated UserDO userDO) {
        userDao.insert(userDO);
        return userDO;
    }

    @GetMapping(value = "list")
    public List<UserDO> list() {
        return userDao.selectAll();
    }
}
```

