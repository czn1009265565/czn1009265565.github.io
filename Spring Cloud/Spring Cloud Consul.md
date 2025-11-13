# Spring Cloud Consul
Consul 是 HashiCorp 公司推出的一款开源工具，提供了服务发现、健康检查、键值存储（用于配置）、多数据中心等功能

## 整体架构

在微服务架构中，Consul 通常扮演以下角色：

1. 服务注册中心：各个微服务在启动时向 Consul 注册自己的网络地址（IP和端口）。
2. 服务发现：服务消费者通过 Consul 查找它要调用的服务的具体地址列表。
3. 健康检查：Consul 会定期检查注册服务的健康状态（如HTTP、TCP、脚本检查），并自动将不健康的实例从服务列表中剔除。
4. 分布式配置中心：利用 Consul 的 Key/Value 存储功能，集中管理所有微服务的配置信息。


## 安装运行 Consul

1. 下载 Consul  
从 HashiCorp 官网 `https://developer.hashicorp.com/consul/install` 下载对应操作系统的二进制文件，或使用包管理器（如 Homebrew: brew install consul）。

2. 以开发模式启动 Consul  
打开终端，执行以下命令。-dev 参数表示以开发模式运行，它会自动创建一个单节点的集群。
```shell
consul agent -dev -client=0.0.0.0 -ui
```
- `-client=0.0.0.0`: 允许其他机器访问本机的 Consul（默认只允许 localhost）。
- `-ui`: 启用内置的 Web UI 界面。

3. 验证  
   - 访问 http://localhost:8500 应该能看到 Consul 的 Web 管理界面。
   - 在界面的 “Nodes” 部分，你应该能看到一个名为 “consul” 的节点，表示 Server 已成功运行。

## Spring Boot 集成 Consul

### 服务提供者

#### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<!-- Actuator for health checks -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<!-- Spring Cloud Consul Discovery -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-consul-discovery</artifactId>
</dependency>
```

重要： 确保管理了 Spring Cloud 的版本。在 `<dependencyManagement>` 中指定，
这里选择的Spring Boot版本是`2.7.6`，因此对应的Spring Cloud版本是`2021.0.5`

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-dependencies</artifactId>
    <version>2021.0.5</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

#### 配置文件

```yaml
server:
  port: 8081 # 服务端口

spring:
  application:
    name: service-provider # 服务名称
  cloud:
    consul:
      host: localhost     # Consul Server 地址
      port: 8500          # Consul Server 端口
      discovery:
        service-name: ${spring.application.name} # 注册到Consul的服务名
        # 其他可选配置
        # instance-id: ${spring.application.name}:${server.port} # 实例ID，默认是 应用名:端口:随机值
        # health-check-path: /actuator/health # 健康检查端点
        # health-check-interval: 10s # 健康检查间隔

# 开放Actuator端点，供Consul进行健康检查
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: always
```

#### 编写Controller

```java
@RestController
public class ProviderController {

    @Value("${server.port}")
    private String port;

    @GetMapping("/hello")
    public String hello(@RequestParam(value="name") String name) {
        return "Hello, " + name + ". I'm from port: " + port;
    }
}
```

#### 启动应用

启动后，查看 Consul UI (http://localhost:8500)。在 “Services” 选项卡下，你应该能看到一个名为 service-provider 的服务，并且有一个健康的实例。


### 服务消费者

#### 引入依赖
这里新增一个openfeign，用户服务间接口调用
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-consul-discovery</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

#### 配置文件

```yaml
server:
  port: 8082

spring:
  application:
    name: service-consumer
  cloud:
    consul:
      host: localhost
      port: 8500
      discovery:
        service-name: ${spring.application.name}
```

#### 启用服务发现

```java
@EnableFeignClients    // 启用Feign的客户端功能
@EnableDiscoveryClient // 显式启用服务发现客户端
@SpringBootApplication
public class SpringBootConsumerApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpringBootConsumerApplication.class, args);
    }
}
```

#### 创建Feign客户端

```java
@FeignClient(value = "service-provider")
public interface ProviderFeign {
    @GetMapping(value = "/hello")
    String hello(@RequestParam(value = "name") String name);
}
```

#### 编写Controller

```java
@RestController
public class ConsumerController {

    @Resource
    private ProviderFeign providerFeign;

    @GetMapping("/hello")
    public String hello(@RequestParam String name) {
        return providerFeign.hello(name);
    }
}
```

#### 接口测试

1. 确保 Consul Server 正在运行。
2. 启动 service-provider 应用 (端口 8081)。
3. 启动 service-consumer 应用 (端口 8082)。
4. 访问 `http://localhost:8082/hello?name=Consul` 接口返回"Hello, Consul. I'm from port: 8081"