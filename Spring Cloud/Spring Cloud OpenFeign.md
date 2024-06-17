# Spring Cloud OpenFeign

Feign是一个声明式的web服务客户端，让编写web服务客户端变得非常容易，只需创建一个接口并在接口上添加注解即可。  
Feign也支持可拔插式的编码器和解码器。Spring Cloud对Feign进行了封装，使其支持了Spring MVC标准注解和HttpMessageConverters。

## Spring Boot 集成 OpenFeign
### 引入依赖
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

### 启用Feign客户端

在启动类上添加`@EnableFeignClients`注解来启用Feign的客户端功能

```java
@SpringBootApplication
@EnableFeignClients
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 声明Feign接口

```java
@FeignClient(value = "user-service")
public interface UserService {
    @PostMapping("/user/create")
    CommonResult create(@RequestBody User user);

    @GetMapping("/user/{id}")
    CommonResult<User> getUser(@PathVariable Long id);

    @GetMapping("/user/getByUsername")
    CommonResult<User> getByUsername(@RequestParam String username);

    @PostMapping("/user/update")
    CommonResult update(@RequestBody User user);

    @PostMapping("/user/delete/{id}")
    CommonResult delete(@PathVariable Long id);
}
```

#### `@FeignClient`属性解析

- name & value: 必填，用于标注客户端名称，也可以用`${propertyKey}`获取配置属性
- contextId: 该类的Bean名称，默认是name属性。由于BeanName在IOC容器中唯一，因此如果一个客户端想要定义多个接口类，就可以指定不同的contextId
- url: URL路径,例如 `http://127.0.0.1:8080`，也可以用`${propertyKey}`获取配置属性
- path: 所有方法级映射使用的路径前缀
- configuration: 用于模拟客户端的自定义配置类。可以包含组成客户端部分的覆盖@Bean定义，默认配置都在FeignClientsConfiguration类中，可以指定FeignClientsConfiguration类中所有的配置
- fallback: 指定失败回调类

#### 示例

1. `@FeignClient(name="user-service", url="http://localhost:8080")` 没有负载均衡能力，只能定向发送
2. `@FeignClient(name="user-service", url="${user-service.url}")` 配置文件中定义 `user-service.url=http://localhost:8080`，没有负载均衡能力
3. `@FeignClient(name="user-service", url="http://localhost:${user-service.port:8080}")` 配置文件中定义 `user-service.port=8080`，没有负载均衡能力
4. `@FeignClient(name="user-service")` 通过服务发现寻址，有负载均衡能力

### Feign拦截器

拦截器是OpenFeign可用的一种强大的工具，它可以被用来在请求和响应前后进行一些额外的处理

```java
public class FirstInterceptor implements RequestInterceptor {
    @Override
    public void apply(RequestTemplate requestTemplate) {
        // 在这里添加额外的处理逻辑，添加请求头
        requestTemplate.header("Token", "value");
    }
}
```

#### 注册拦截器

```java
@Configuration
public class FeignConfiguration {
    @Bean
    public FirstInterceptor firstInterceptor() {
        return new FirstInterceptor();
    }
    
    /** 注册多个拦截器 可以通过Order注解决定执行顺序 **/
    @Bean
    public SecondInterceptor secondInterceptor() {
        return new SecondInterceptor();
    }
}
```

### 集成Nacos服务发现

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```

#### 配置服务注册中心地址

```yml
spring:
  application:
    name: feign-client
  cloud:
    nacos:
      discovery:
        enabled: true
        server-addr: 127.0.0.1:8848
        namespace: 03212e55-6b5c-4743-8127-cf397e18118d
```

在启动类上添加`@EnableDiscoveryClient`注解来启动服务发现

### 服务降级
#### 引入pom依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```

#### 添加服务降级实现类

```java
@Component
public class UserFallbackService implements UserService {
    @Override
    public CommonResult create(User user) {
        return new CommonResult("调用失败，服务被降级",500);
    }

    @Override
    public CommonResult<User> getUser(Long id) {
        return new CommonResult("调用失败，服务被降级",500);
    }

    @Override
    public CommonResult<User> getByUsername(String username) {
        return new CommonResult("调用失败，服务被降级",500);
    }

    @Override
    public CommonResult update(User user) {
        return new CommonResult("调用失败，服务被降级",500);
    }

    @Override
    public CommonResult delete(Long id) {
        return new CommonResult("调用失败，服务被降级",500);
    }
}
```

#### 设置服务降级处理类

```java
@FeignClient(value = "user-service",fallback = UserFallbackService.class)
public interface UserService {
}
```