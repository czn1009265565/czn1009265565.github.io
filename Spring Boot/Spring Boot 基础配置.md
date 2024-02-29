## Spring Boot 基础配置

### 端口配置

```
server:
  port: 8080
```

### 环境配置

开发、部署、测试过程中 往往对应多个配置文件

新建`application.yml`,`application-dev.yml`,`application-test.yml`,`application-prod.yml`
```
spring:
  profiles:
    include: dev
```

### 属性配置

```
wechat:
  appId: xxx
  appSecret: xxx
  openAppId: xxx
  openAppSecret: xxx
```

单属性导入
```
@Data
@Component
public class WechatAccountConfig {
    @Value("${wechat.appId}")
    private String appId;

    @Value("${wechat.appSecret}")
    private  String appSecret;
}
```

多属性导入
```
@Data
@Component
@ConfigurationProperties(prefix = "wechat")
public class WechatAccountConfig {

    /**
     * 公众平台id
     */
    private String appId;

    /**
     * 公众平台密钥
     */
    private String appSecret;

    /**
     * 开放平台id
     */
    private String openAppId;

    /**
     * 开放平台密钥
     */
    private String openAppSecret;
}
```

### 属性间引用

```
author:
  firstName: zenan
  lastName: chen
  wholeName: ${author.lastName}${author.firstName}
```


### SQL启动脚本

启动运行建表语句、通用数据插入
```
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/database
    username: root
    password: Admin123.
    driver-class-name: com.mysql.jdbc.Driver
  sql:
    init:
      schema-locations: classpath:sql/schema.sql
      data-locations: classpath:sql/data.sql
      mode: always
```