## Spring Cloud Alibaba Nacos

### 安装部署
1. [版本选择](https://github.com/alibaba/nacos/tags) 查看Spring Cloud Alibaba 对应Nacos版本
2. 初始化数据库 执行conf目录下的`nacos-mysql.sql`
3. 数据库配置 `vim ./conf/application.properties`

```properties
spring.datasource.platform=mysql

## Count of DB:
db.num=1

## Connect URL of DB:
db.url.0=jdbc:mysql://127.0.0.1:3306/nacos?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&serverTimezone=UTC
db.user.0=nacos
db.password.0=nacos
```
4. 单机部署 `sh ./bin/startup.sh -m standalone`


### Spring Boot 集成

1. 引入依赖

```xml
<!-- 用于加载bootstrap.yml -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bootstrap</artifactId>
</dependency>

<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```

2. 配置Nacos地址

新建`bootstrap.yml`

```yaml
spring:
  application:
    name: example
  cloud:
    nacos:
      discovery:
        enabled: true
        server-addr: 127.0.0.1:8848
        # server-addr: 127.0.0.1:8848,127.0.0.1:8849,127.0.0.1:8850
        namespace: 3c346842-ec50-4a0b-9e9f-67c941182609
```

3. 通过 Spring Cloud 原生注解 `@EnableDiscoveryClient` 开启服务注册发现功能
4. 启动服务，至此服务注册完成
5. 服务发现

```java
@Slf4j
@Service
public class NacosClientService {
    
    private final DiscoveryClient discoveryClient;

    public NacosClientService(DiscoveryClient discoveryClient) {
        this.discoveryClient = discoveryClient;
    }

    public List<ServiceInstance> getNacosClientInfo(String serviceId) {
        return discoveryClient.getInstances(serviceId);
    }
}
```