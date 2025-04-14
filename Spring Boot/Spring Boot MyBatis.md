## Spring Boot MyBatis

### 依赖配置

这里我们需要引入`mybatis-spring-boot-starter`和数据库连接驱动(这里采用MySQL)
[Spring Boot与MyBatis对应版本查看](http://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/)

```xml
<dependencies>
    <!-- MySQL Driver -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>${mysql.version}</version>
    </dependency>

    <!-- MyBatis -->
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>${mybatis.version}</version>
    </dependency>
</dependencies>
```

### application配置

```yaml
spring:
  # MySQL
  datasource:
    url: jdbc:mysql://localhost:3306/dbname
    username: username
    password: password
    driver-class-name: com.mysql.jdbc.Driver
#  PostgreSQL    
#  datasource:
#    url: jdbc:postgresql://127.0.0.1:5432/dbname
#    username: postgres
#    password: postgres
#    driver-class-name: org.postgresql.Driver
    

mybatis:
  configuration:
    # 控制台日志配置,打出执行的sql语句
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  # 配置XML Mapper 扫描路径  
  mapper-locations: classpath:mapper/*.xml
```

### 配置文件
在启动类上新增`@MapperScan`注解

```java
@MapperScan("com.example.mybatis.dao")
@SpringBootApplication
public class MybatisAnnotationApplication {

    public static void main(String[] args) {
        SpringApplication.run(MybatisAnnotationApplication.class, args);
    }
}
```

### 定义实体类
```java
@Data
public class User {
    private Long id;

    private String username;

    private Integer age;

    private String email;

    private LocalDateTime createTime;

    private LocalDateTime updateTime;
}
```

### 定义Dao层

```java
public interface UserMapper {

    int insert(@Param("user") User user);

    User selectById(Long id);
}
```


### SQL映射

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mybatis.dao.UserMapper">
    <sql id="baseColumn">
        id, username, age, email, create_time, update_time
    </sql>

    <resultMap id="userResultMap" type="com.example.mybatis.entity.User">
        <id column="id" property="id" jdbcType="BIGINT"/>
        <result column="username" property="username" jdbcType="VARCHAR"/>
        <result column="age" property="age" jdbcType="INTEGER"/>
        <result column="email" property="email" jdbcType="VARCHAR"/>
        <result column="create_time" property="createTime" jdbcType="TIMESTAMP"/>
        <result column="update_time" property="updateTime" jdbcType="TIMESTAMP"/>
    </resultMap>

    <insert id="insert">
        insert into user(<include refid="baseColumn" />)
        values(#{user.id}, #{user.username}, #{user.age}, #{user.email}, #{user.createTime}, #{user.updateTime})
    </insert>

    <select id="selectById" resultMap="userResultMap">
        select <include refid="baseColumn" /> from user where id = #{id};
    </select>
</mapper>
```

更多的关于MyBatis动态SQL [查看文档](https://mybatis.org/mybatis-3/dynamic-sql.html)

### 转义符

| 符号   | 原符号    | 替换符号        |
|------|--------|-------------|
| 小于	  | `<`	   | `&lt;`      |
| 小于等于 | 	`<=`	 | `&lt;=`     |
| 大于   | 	`>`	  | `&gt;`      |
| 大于等于 | 	`>=`	 | `&gt;=`     |
| 不等于	 | `<>`   | 	`&lt;&gt;` |
| 与	   | `&`	   | `&amp;`     |
| 单引号	 | `’`	   | `&apos;`    |
| 双引号	 | `"`    | `&quot;`    |

## 分页插件

### 引入依赖 

[最新版本查看](https://github.com/pagehelper/pagehelper-spring-boot)

```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.3.1</version>
</dependency>
```

### 最佳实践
PageVO
```java
@Data
public class PageVO<T> {
    private Integer pageNum;
    private Integer pageSize;
    private Long total;
    private Integer pages;
    private List<T> data;

    public static <T> PageVO<T> assemblePage(PageInfo<T> pageInfo) {
        if (Objects.isNull(pageInfo)) return null;
        PageVO<T> pageVO = new PageVO<>();
        pageVO.setPageNum(pageInfo.getPageNum());
        pageVO.setPageSize(pageInfo.getPageSize());
        pageVO.setPages(pageInfo.getPages());
        pageVO.setTotal(pageInfo.getTotal());
        pageVO.setData(pageInfo.getList());
        return pageVO;
    }
}
```

UserService
```java
public interface UserService {
    PageVO<User> list(Integer pageNum, Integer pageSize);
}
```

UserServiceImpl
```java
@Service
public class UserServiceImpl implements UserService {

    @Resource
    private UserMapper userMapper;

    @Override
    public PageVO<User> list(Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<User> userList = userMapper.selectAll();
        PageInfo<User> pageInfo = PageInfo.of(userList);
        return PageVO.assemblePage(pageInfo);
    }
}
```