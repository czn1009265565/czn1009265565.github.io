## Spring Cloud Gateway

### 背景

在微服务架构系统中,往往由多个微服务组成,而这些服务可能部署在不同机房、不同地区、不同域名下

这种客户端直接请求服务的方式存在以下问题:

1. 当服务数量众多时，客户端需要维护大量的服务地址
2. 身份认证的难度大，每个微服务需要独立认证

### Gateway

Gateway是在Spring生态系统之上构建的API网关服务，基于Spring 5，Spring Boot 2和 Project Reactor等技术。Gateway旨在提供一种简单而有效的方式来对API进行路由，以及提供一些强大的过滤器功能， 例如：熔断、限流、重试等。


### 核心概念

- Route（路由）：路由是构建网关的基本模块，它由ID，目标URI，一系列的断言和过滤器组成，如果断言为true则匹配该路由

- Predicate（断言）：指的是Java 8 的 Function Predicate。 输入类型是Spring框架中的ServerWebExchange。 这使开发人员可以匹配HTTP请求中的所有内容，例如请求头或请求参数。如果请求与断言相匹配，则进行路由

- Filter（过滤器）：指的是Spring框架中GatewayFilter的实例，使用过滤器，可以在请求被路由前后对请求进行修改

## 快速集成

### pom 文件新增依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

### Route Predicate 的使用

#### 路由配置

```yml
server:
  port: 9201
service-url:
  user-service: http://localhost:8201

spring:
  cloud:
    gateway:
      routes:
        - id: user-service #路由的ID
          uri: ${service-url.user-service}/user
          predicates: # 断言，路径相匹配的进行路由
            - Path=/user/**
```

接下来都省略前缀

#### Cookie Route Predicate
带有指定Cookie的请求会匹配该路由

```yml
- id: cookie_route
  uri: ${service-url.user-service}/user
  predicates: 
    - Cookie=username,\w+
```

#### After Route Predicate
指定时间之后的请求回匹配该路由

```yml
- id: after_route
  uri: ${service-url.user-service}
  predicates:
    - After=2022-09-24T16:30:00+08:00[Asia/Shanghai]
```

#### Before Route Predicate
在指定时间之前的请求会匹配该路由

```yml
- id: before_route
  uri: ${service-url.user-service}
  predicates:
    - Before=2022-09-24T16:30:00+08:00[Asia/Shanghai]
```

#### Host Route Predicate
带有指定Host的请求会匹配该路由

```yml
- id: host_route
  uri: ${service-url.user-service}
  predicates:
    - Host=**.github.com
```

### Hystrix GatewayFilter
Hystrix 过滤器允许你将断路器功能添加到网关路由中，使你的服务免受级联故障的影响，并提供服务降级处理。

#### 引入相关依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```

#### 新增服务降级处理类

```java
@RestController
public class FallbackController {

    @GetMapping("/fallback")
    public String fallback() {
        return "500";
    }
}
```

#### 配置降级处理

```yml
spring:
  cloud:
    gateway:
      routes:
        - id: hystrix_route
          uri: ${service-url.user-service}/user
          predicates:
            - Method=GET
          filters:
            - name: Hystrix
              args:
                name: fallbackcmd
                fallbackUri: forward:/fallback
```


### 动态路由

结合注册中心，默认以服务名为路径创建动态路由

```yml
server:
  port: 9201
spring:
  application:
    name: spring-cloud-gateway
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true #开启从注册中心动态创建路由的功能
          lower-case-service-id: true #使用小写服务名，默认是大写
```


