# Spring Boot JDBC

## 背景
JDBC是一种用于执行SQL语句的Java API，可以为多种关系数据库提供统一访问，它由一组用Java语言编写的类和接口组成。
JDBC提供了一种基准，据此可以构建更高级的工具和接口，使数据库开发人员能够编写数据库应用程序。

使用JDBC操作数据库步骤较为复杂:  
1. 加载数据库驱动
2. 建立数据库连接
3. 创建数据库操作对象
4. 定义操作的 SQL 语句
5. 执行数据库操作
6. 获取并操作结果集
7. 关闭对象，回收资源

`Spring Boot` 针对 `JDBC` 的使用提供了对应的 starter 包: `spring-boot-starter-jdbc`，
它其实就是在 `Spring JDBC` 上做了进一步的封装，替我们生成了默认的数据源以及JdbcTemplate对象。

## 引入依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
    </dependency>
</dependencies>
```

## 配置application

```yaml
spring:
  datasource:
    url: jdbc:mysql://127.0.0.1:3306/dbname?useUnicode=true&characterEncoding=utf-8&useSSL=false
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
```

## 基本使用

JdbcTemplate基本API:  
1. execute方法: 用于执行任何SQL语句，一般用于执行DDL语句
2. update方法及batchUpdate方法: update方法用于执行新增、修改、删除等语句; batchUpdate方法用于执行批处理相关语句
3. query、queryForList、queryForMap、queryForObject方法: 用于执行查询相关语句
4. call方法: 用于执行存储过程、函数相关语句

### 初始化建表语句

```mysql
CREATE TABLE user (
  id BIGINT(20) NOT NULL PRIMARY KEY COMMENT '用户Id',
  name VARCHAR(64) NOT NULL COMMENT '用户名',
  sex VARCHAR(32) NOT NULL COMMENT '性别',
  age INT(11) COMMENT '年龄',
  create_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
  update_time DATETIME NOT NULL DEFAULT NOW() COMMENT '更新时间',
  status INT(4) COMMENT '状态'
) COMMENT '用户表';
```

### 实体类定义
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

### 数据操作层

```java
@Repository
public class UserDao {
    @Resource
    private JdbcTemplate jdbcTemplate;

    public int save(UserDO userDO) {
        String sql = "insert into user(id, name, sex, age, create_time, update_time, status) values (?,?,?,?,?,?,?)";
        return jdbcTemplate.update(sql,
                userDO.getId(), userDO.getName(), userDO.getSex(),
                userDO.getAge(), userDO.getCreateTime(), userDO.getUpdateTime(), userDO.getStatus());
    }

    public int deleteById(Long id) {
        return jdbcTemplate.update("delete from user where id = ?", id);
    }

    public UserDO findById(Long id) {
        // 查询单条记录
        Object[] args = new Object[] {id};
        return jdbcTemplate.queryForObject("select * from user where id = ?", args, new BeanPropertyRowMapper<>(UserDO.class));
    }

    public List<UserDO> findAll() {
        // 查询多条记录
        return jdbcTemplate.query("select * from user", new BeanPropertyRowMapper<>(UserDO.class));
    }
}
```

### 自定义连接池

```java
@Component
public class DataSourceConfig {

    @Bean
    public HikariDataSource hikariDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://127.0.0.1:5432/postgres");
        config.setUsername("postgres");
        config.setPassword("postgres");
        // 可以省略
        // hikariDataSource.setDriverClassName("org.postgresql.Driver");
        // 最小连接数
        config.setMinimumIdle(5);
        // 最大连接数
        config.setMaximumPoolSize(10);
        // 是否自动提交，默认为true
        config.setAutoCommit(true);
        // 连接测试语句，一般为 select 1
        config.setConnectionTestQuery("select 1");
        // 连接超时时长，单位毫秒
        config.setConnectionTimeout(30000);
        // 最大生命时长，单位毫秒
        config.setMaxLifetime(1800000);
        // 连接池名称
        config.setPoolName("HikariCP");

        // 配置连接池
        return new HikariDataSource(config);
    }
}
```

### 自定义JdbcTemplate
```java
public class JDBCTest {
    public static void main(String[] args) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String username = "postgres";
        String password = "postgres";
        String driverClassName = "org.postgresql.Driver";

        Properties properties = new Properties();
        DriverDataSource driverDataSource = new DriverDataSource(url, driverClassName,
                properties, username, password);

        // JdbcTemplate完成查询后会自动释放连接
        JdbcTemplate jdbcTemplate = new JdbcTemplate(driverDataSource, true);
        Long count = jdbcTemplate.queryForObject("select 1", Long.class);
        System.out.println(count);
    }
}
```