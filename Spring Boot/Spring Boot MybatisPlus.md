## Spring Boot MybatisPlus

简化开发，提高效率

### 引入依赖

```xml
<properties>
    <!-- mybatis 与 mybatis-plus 对应版本-->
    <mybatis.version>2.2.1</mybatis.version>
    <mybatis.plus.version>3.5.1</mybatis.plus.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-boot-starter</artifactId>
        <version>${mybatis.plus.version}</version>
    </dependency>
</dependencies>
```

### application配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://127.0.0.1:5432/dbname
    username: postgres
    password: postgres
    driver-class-name: org.postgresql.Driver

mybatis-plus:
  mapper-locations: classpath:mapper/*.xml
  configuration:
    # 控制台日志配置,打出执行的sql语句
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

### 扫描Mapper文件

在 Spring Boot 启动类中添加 @MapperScan 注解，扫描 Mapper 文件夹

```java
@SpringBootApplication
@MapperScan("com.example.mybatisplus.dao")
public class SpringBootMybatisPlusApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringBootMybatisPlusApplication.class, args);
    }
}
```

### 建表语句
这里使用MySQL数据库

```sql
CREATE TABLE user (
    id BIGINT(20) NOT NULL PRIMARY KEY COMMENT '用户Id',
    username VARCHAR(64) NOT NULL COMMENT '用户名',
    nickname VARCHAR(64) COMMENT '昵称',
    age INT(11) COMMENT '年龄',
    email VARCHAR(64) NOT NULL COMMENT '邮箱',
    friends VARCHAR(255) COMMENT '好友',
    create_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT NOW() COMMENT '更新时间'
) COMMENT '用户表';
```

### 定义实体类 `UserDO.java`

此处使用了 Lombok 简化代码

```java
@Data
@TableName(value = "user", autoResultMap = true)
public class UserDO {
    @TableId(value = "id")
    private Long id;

    @TableField(value = "username")
    private String username;

    private String nickname;

    private Integer age;

    /** 更新时该字段不做非空校验 */
    @TableField(updateStrategy = FieldStrategy.IGNORED)
    private String email;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<UserDO> friends;
}
```

`@TableField`说明

|属性|类型|必须指定| 示例 |描述|
|---|---|---|---|---|
|value  | String | 否  | "" | 数据库字段名|
|exist  | boolean |否  | true  |  是否为数据库表字段|
|condition |  String | 否  | "" | 字段 where 实体查询比较条件|
|update | String | 否 |  "" | 字段 update set 部分注入，例如：当在version字段上注解update="%s+1" 表示更新时会 set version=version+1 （该属性优先级高于 el 属性）|
|insertStrategy | Enum  |  否 |  FieldStrategy.DEFAULT | 见注释 |
|updateStrategy | Enum  |  否 |  FieldStrategy.DEFAULT | 见注释 |
|whereStrategy  | Enum  |  否 |  FieldStrategy.DEFAULT | 见注释 |
|fill  |  Enum  |  否  | FieldFill.DEFAULT |  字段自动填充策略|
|select | boolean | 否 |  true  |  是否进行 select 查询|
|keepGlobalFormat |   boolean |否  | false  | 是否保持使用全局的 format 进行处理|
|jdbcType |   JdbcType  |  否  | JdbcType.UNDEFINED | JDBC 类型 (该默认值不代表会按照该值生效)|
|typeHandler | Class<? extends TypeHandler> |   否  | JacksonTypeHandler.class  |  类型处理器 需要配合`@TableName(autoResultMap = true)`|
|numericScale  |  String | 否 |  "" | 指定小数点后保留的位数|

```java
public enum FieldStrategy {
    /**
     * 忽略判断
     */
    IGNORED,
    /**
     * 非NULL判断
     */
    NOT_NULL,
    /**
     * 非空判断(只对字符串类型字段,其他类型字段依然为非NULL判断)
     */
    NOT_EMPTY,
    /**
     * 默认的,一般只用于注解里
     * <p>1. 在全局里代表 NOT_NULL</p>
     * <p>2. 在注解里代表 跟随全局</p>
     */
    DEFAULT,
    /**
     * 不加入 SQL
     */
    NEVER
}

```


### 编写 Mapper 包下的 UserDao接口

```java
public interface UserDao extends BaseMapper<UserDO> {
}
```

### 批量插入、更新

```java
@Repository
public class UserBatchDao extends ServiceImpl<UserDao, UserDO> {
}
```

### 简单查询实现

```java
@Mapper
public interface UserDao extends BaseMapper<UserDO> {

    default UserDO selectByUsername(String username) {
        if (!StringUtils.hasLength(username)) {
            return null;
        }
        LambdaQueryWrapper<UserDO> lambdaQueryWrapper = new LambdaQueryWrapper<>();
        lambdaQueryWrapper.eq(UserDO::getUsername, username);
        return this.selectOne(lambdaQueryWrapper);
    }

    default List<UserDO> selectByNickname(String nickname) {
        if (!StringUtils.hasLength(nickname)) {
            return Collections.emptyList();
        }
        LambdaQueryWrapper<UserDO> lambdaQueryWrapper = new LambdaQueryWrapper<>();
        lambdaQueryWrapper.eq(UserDO::getNickname, nickname);
        return this.selectList(lambdaQueryWrapper);
    }
}
```

QueryWrapper

| 函数名     | 说明              |
|---------|-----------------|
| eq      | 等于              |
| ne      | 不等于             |
| gt      | 大于              |
| lt      | 小于              |
| between | 两个值之间           |
| like    | 模糊查询 %variable% |
| isNull  | 字段为NULL         |

### 内置分页查询
分页插件配置

```java
@Configuration
public class MybatisPlusConfig {
    /**
     * 新增分页拦截器，并设置数据库类型为mysql
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }
}
```

分页查询
```java
public interface UserDao extends BaseMapper<UserDO> {

    default Page<UserDO> selectPageByAge(Integer age, Integer pageNum, Integer pageSize) {
        Page<UserDO> page = Page.of(pageNum, pageSize);
        LambdaQueryWrapper<UserDO> lambdaQueryWrapper = new LambdaQueryWrapper<>();
        lambdaQueryWrapper.eq(UserDO::getAge, age);

        return this.selectPage(page, lambdaQueryWrapper);
    }
}
```