## Spring Boot Actuator 监控

在Spring Boot中，我们可以使用Actuator来监控应用，Actuator提供了一系列的RESTful API让我们可以更为细致的了解各种信息。

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

### 开放自定义端点

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


