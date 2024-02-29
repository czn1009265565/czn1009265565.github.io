## 简介

XXL-JOB是一个分布式任务调度平台，其核心设计目标是开发迅速、学习简单、轻量级、易扩展

主要有两个概念 调度中心、执行器 同时部署才能生效。

## 调度中心

1. [Github项目地址](https://github.com/xuxueli/xxl-job)
2. 执行sql语句
3. 修改 xxl-job-admin `application.properties`配置文件
4. 编译启动 xxl-job-admin，访问`http://localhost:8080/xxl-job-admin` 账号:admin 密码:123456

## 执行器

### 引入pom依赖(版本自行修改)
```xml
<!-- 任务调度xxl-job -->
<dependency>
  <groupId>com.xuxueli</groupId>
  <artifactId>xxl-job-core</artifactId>
  <version>2.2.0</version>
</dependency>
```
### application.yml
```yaml
server:
   port: 8888

spring:
   application:
      name: xxl-job-sample

# xxl-job配置
xxl:
   job:
      admin:
         # 调度中心部署跟地址 [选填]：如调度中心集群部署存在多个地址则用逗号分隔。执行器将会使用该地址进行"执行器心跳注册"和"任务结果回调"；为空则关闭自动注册；
         addresses: http://127.0.0.1:8080/xxl-job-admin
      executor:
         # 执行器注册 [选填]：优先使用该配置作为注册地址，为空时使用内嵌服务 ”IP:PORT“ 作为注册地址。从而更灵活的支持容器类型执行器动态IP和动态映射端口问题。
         address:
         # 执行器AppName [选填]：执行器心跳注册分组依据；为空则关闭自动注册
         appname: xxl-job-sample
         # 执行器IP [选填]：默认为空表示自动获取IP，多网卡时可手动设置指定IP，该IP不会绑定Host仅作为通讯实用；地址信息用于 "执行器注册" 和 "调度中心请求并触发任务"；
         ip:
         # 执行器端口号 [选填]：小于等于0则自动获取；默认端口为9999，单机部署多个执行器时，注意要配置不同执行器端口；
         port: 9999
         # 执行器运行日志文件存储磁盘路径 [选填] ：需要对该路径拥有读写权限；为空则使用默认路径；
         logpath: ./log/sample
         # 执行器日志文件保存天数 [选填] ： 过期日志自动清理, 限制值大于等于3时生效; 否则, 如-1, 关闭自动清理功能；
         logretentiondays: 15
      # 执行器通讯TOKEN [选填]：非空时启用；
      accessToken:
```
   
### XxlJobConfig
```java
@Slf4j
@Configuration
public class XxlJobConfig {

    @Value("${xxl.job.admin.addresses}")
    private String adminAddresses;

    @Value("${xxl.job.accessToken}")
    private String accessToken;

    @Value("${xxl.job.executor.appname}")
    private String appname;

    @Value("${xxl.job.executor.address}")
    private String address;

    @Value("${xxl.job.executor.ip}")
    private String ip;

    @Value("${xxl.job.executor.port}")
    private int port;

    @Value("${xxl.job.executor.logpath}")
    private String logPath;

    @Value("${xxl.job.executor.logretentiondays}")
    private int logRetentionDays;

    @Bean
    public XxlJobSpringExecutor xxlJobExecutor() {
        log.info(">>>>>>>>>>> xxl-job config init.");
        XxlJobSpringExecutor xxlJobSpringExecutor = new XxlJobSpringExecutor();
        xxlJobSpringExecutor.setAdminAddresses(adminAddresses);
        xxlJobSpringExecutor.setAppname(appname);
        xxlJobSpringExecutor.setAddress(address);
        xxlJobSpringExecutor.setIp(ip);
        xxlJobSpringExecutor.setPort(port);
        xxlJobSpringExecutor.setAccessToken(accessToken);
        xxlJobSpringExecutor.setLogPath(logPath);
        xxlJobSpringExecutor.setLogRetentionDays(logRetentionDays);

        return xxlJobSpringExecutor;
    }
}
```
### Task

```java
@Slf4j
@Component
public class XxlJobTask {

    /**
     * 1、简单任务示例（Bean模式）
     */
    @XxlJob("demoJobHandler")
    public ReturnT<String> demoJobHandler(String param) throws Exception {
        log.info("Hello World!");
        return ReturnT.SUCCESS;
    }
}
```

## 使用流程

1. 创建新执行器，在调度中心->执行器管理->新增，AppName要与执行器配置文件里面配置的名称一致，选择自动注册即可
2. 创建新任务，在调度中心->任务管理->新增，选择我们刚刚创建的新执行器，重点关注JobHandler这个配置，名称要跟相应的任务方法上@XxlJob注解里面的名称一致
3. 创建完成后，在操作那里进行执行一次，查看对应的日志输出，可知配置成功