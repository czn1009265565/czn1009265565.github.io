## Spring Cloud Admin 服务监控

Spring Boot Admin（SBA）是一款基于Actuator开发的开源软件，以图形化界面的方式展示Spring Boot应用的配置信息、Beans信息、环境属性、线程信息、JVM状况等

### Spring Boot Admin Server

1. 引入依赖

```xml
<dependency>
    <groupId>de.codecentric</groupId>
    <artifactId>spring-boot-admin-server</artifactId>
    <version>2.5.6</version>
</dependency>

<dependency>
    <groupId>de.codecentric</groupId>
    <artifactId>spring-boot-admin-server-ui</artifactId>
    <version>2.5.6</version>
</dependency>
```

2. 开启监控

```java
@EnableAdminServer
@SpringBootApplication
public class SpringCloudAdminServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringCloudAdminServerApplication.class, args);
    }

}
```

3. 端口配置

```yaml
server:
  port: 8888
```

4. 启动服务,访问`localhost:8888`


### Spring Boot Admin Client
注册到Spring Boot Admin Server存在两种方式

- Spring Boot Admin Client 通过Http 调用注册
- 通过Spring Cloud 注册中心 获取被监控和管理的应用程序

1. 引入依赖

```xml
<dependency>
    <groupId>de.codecentric</groupId>
    <artifactId>spring-boot-admin-starter-client</artifactId>
    <version>2.5.6</version>
</dependency>
```

2. 调用注册方式

```yaml
server:
  port: 8889

spring:
  boot:
    admin:
      client:
        url: http://localhost:8888

management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always
```

3. 注册中心方式

```yaml
server:
  port: 8889

spring:
  application:
    name: admin-client
  cloud:
    nacos:
      discovery:
        enabled: true
        server-addr: 127.0.0.1:8848
        namespace: 96048fb0-9115-428b-a90f-6247f7461d0c
        metadata:
          management:
            context-path: /actuator
            
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always
```

4. 启动服务，查看`localhost:8888`
