# Spring Boot Actuator

在Spring Boot中，我们可以使用Actuator来监控应用，Actuator提供了一系列的RESTful API让我们可以更为细致的了解各种信息。

## Spring Boot 集成
### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Actuator配置

开放所有端点
```yaml
management:
  endpoints:
    enabled-by-default: true #默认是true
    web:
      exposure:
        include: "*"  #开启全部监控端点
      base-path: /actuator #自定义访问路径
  endpoint:
    health:
      show-details: always #health端点显示具体信息
```

开放自定义端点
```yaml
management:
  endpoints:
    web:
      exposure:
        include: 
          - info
          - health
      base-path: /actuator
```

这里由于不同版本的`spring-boot-starter-actuator`配置项也大不相同,
可以查看源码包中`spring-configuration-metadata.json`中的配置项及描述

### 接口列表

|HTTP 方法|路径|描述|
|---|---|---|
|GET|/configprops|描述配置属性(包含默认值)如何注入Bean|
|GET|/beans|描述应用程序上下文里全部的Bean，以及它们的关系|
|GET|/threaddump|获取线程活动的快照|
|GET|/env|获取全部环境属性|
|GET|/env/{name}|根据名称获取特定的环境属性值|
|GET|/health|报告应用程序的健康指标，这些值由HealthIndicator的实现类提供|
|GET|/info|获取应用程序的定制信息，这些信息由info打头的属性提供|
|GET|/mappings|描述全部的URI路径，以及它们和控制器(包含Actuator端点)的映射关系|
|GET|/metrics|报告各种应用程序度量信息，比如内存用量和HTTP请求计数|
|GET|/metrics/{name}|报告指定名称的应用程序度量值|


## Spring Boot 数据可视化
`Spring Boot Actuator` 提供了各种端点，而 `Spring Boot Admin` 能够将 `Actuator` 中的信息进行界面化的展示，并提供实时报警功能。

在微服务环境中，使用 `Spring Boot Admin`，通常包括服务端和客户端，服务端只运行 `Spring Boot Admin Server`，收集各个客户端的数据，并以可视化界面显示出来。
客户端运行 `Spring Boot Admin Client`，或者通过服务发现与注册获取应用的信息。

### 引入依赖

```xml
<dependency>
    <groupId>de.codecentric</groupId>
    <artifactId>spring-boot-admin-starter-server</artifactId>
    <version>${server.version}</version>
</dependency>
```

### application 配置

```yaml
server:
  port: 8888
```

### 开启 Admin Server

```java
@EnableAdminServer
@SpringBootApplication
public class SpringBootAdminServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringBootAdminServerApplication.class, args);
    }
}
```

启动Admin Server服务，访问 `http://localhost:8888` 查看监控页面详情

### 配置客户端

```xml
<dependency>
    <groupId>de.codecentric</groupId>
    <artifactId>spring-boot-admin-starter-client</artifactId>
    <version>${server.version}</version>
</dependency>
```

连接Admin Server
```yaml
spring:
  application:
    name: spring-boot-admin-client
  boot:
    admin:
      client:
        url: 'http://localhost:8888'
        instance:
          # 注册到Admin Server的微服务名称
          name: ${spring.application.name}
```