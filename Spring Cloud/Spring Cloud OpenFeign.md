## Spring Cloud OpenFeign.md


### 引入pom文件

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

### Nacos配置

#### 引入nacos依赖

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

### 启用Feign客户端

在启动类上添加`@EnableFeignClients`注解来启用Feign的客户端功能


### 添加userService接口

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