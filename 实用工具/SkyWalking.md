# SkyWalking

## 简介
Skywalking 时一个开源的分布式追踪系统，用于检测、诊断和优化分布式系统的功能。
它可以帮助开发者和运维人员深入了解分布式系统中各个组件之间的调用关系、性能瓶颈以及异常情况，从而提供系统级的性能优化和故障排查。

![架构](./imgs/SkyWalking.jpg)

- Agent: 负责收集日志数据，并且传递给中间的OAP服务器
- OAP: 后台服务，负责接收 Agent 发送的 Tracing 和Metric的数据信息，然后进行分析(Analysis Core) ，存储到外部存储器( Storage )，最终提供查询( Query )功能
- UI: web控制台，支持查看链路，查看各种指标，性能等
- Storage: 负责数据的存储，支持多种存储类型。


## 单机环境搭建

官方下载地址: https://skywalking.apache.org/downloads/

```shell
# 解压
tar -zxvf apache-skywalking-apm-bin.tar.gz
```

### SkyWalking OAP

修改配置文件，这里主要修改存储配置，采用Elasticsearch

```shell
vim config/application.yml
```

启动 SkyWalking OAP 服务
```shell
# Linux
bin/oapService.sh
# Windows
bin/oapService.bat
```

查看日志详情
```shell
tail -200f logs/skywalking-oap-server.log
```

### SkyWalking UI

修改配置文件，可以修改对应的端口占用

```shell
vim webapp/application.yml
```

启动 SkyWalking UI 服务
```shell
# Linux
bin/webappService.sh
# Windows
bin/webappService.bat
```

查看日志详情
```shell
tail -200f logs/skywalking-webapp.log
```

访问UI界面  `http://127.0.0.1:8080`


## SkyWalking Agent 应用
参数配置

- `-javaagent:<skywalking-agent-path>`: 指定`skywalking`中的agent中的`skywalking-agent.jar`路径
- `-Dskywalking.agent.service_name`: 指定客户端服务名称，一般是 `spring.application.name`
- `-Dskywalking.collector.backend_service`: 指定OAP服务地址，本地地址则为`127.0.0.1:11800`

```shell
# 启动服务
java -javaagent:<skywalking-agent-path> -Dskywalking.collector.backend_service=127.0.0.1:11800 -Dskywalking.agent.service_name=<application-name> -jar app.jar
```

### 日志收集

#### 引入依赖

```xml
<dependency>
    <groupId>org.apache.skywalking</groupId>
    <artifactId>apm-toolkit-logback-1.x</artifactId>
    <version>9.3.0</version>
</dependency>
```

#### 日志配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!--定义日志文件的存储路径-->
    <property name="LOG_HOME" value="app/logs/"/>

    <!-- 控制台 appender -->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%class:%line] %-5level - %msg%n</pattern>
        </encoder>
    </appender>

    <!--skywalking grpc 日志收集-->
    <appender name="GRPC" class="org.apache.skywalking.apm.toolkit.log.logback.v1.x.log.GRPCLogClientAppender">
        <encoder class="ch.qos.logback.core.encoder.LayoutWrappingEncoder">
            <layout class="org.apache.skywalking.apm.toolkit.log.logback.v1.x.mdc.TraceIdMDCPatternLogbackLayout">
                <pattern>%d{yyyy-MM-dd HH:mm:ss.sss} [%X{sw_ctx}] [%thread] %-5level %logger{36} -%msg%n</pattern>
            </layout>
        </encoder>
    </appender>

    <!--按天生成日志-->
    <!-- 出错日志 appender -->
    <appender name="FILE_ERROR" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <File>${LOG_HOME}/error.log</File>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 按天回滚 daily -->
            <fileNamePattern>${LOG_HOME}/error-%d{yyyy-MM-dd}.log
            </fileNamePattern>
            <!-- 日志最大的历史 30天 -->
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%class:%line] %-5level - %msg%n</pattern>
        </encoder>
        <filter class="ch.qos.logback.classic.filter.LevelFilter"><!-- 只打印错误日志 -->
            <level>ERROR</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>
    <!-- info日志 appender -->
    <appender name="FILE_INFO" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <File>${LOG_HOME}/info.log</File>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!-- 按天回滚 daily -->
            <fileNamePattern>${LOG_HOME}/info-%d{yyyy-MM-dd}.log
            </fileNamePattern>
            <!-- 日志最大的历史 30天 -->
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%class:%line] %-5level - %msg%n</pattern>
        </encoder>
        <filter class="ch.qos.logback.classic.filter.LevelFilter"><!-- 只打印INFO级别日志 -->
            <level>INFO</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!-- 测试环境+开发环境，日志级别为INFO且不写日志文件 -->
    <springProfile name="test,dev">
        <root level="INFO">
            <appender-ref ref="STDOUT"/>
            <appender-ref ref="GRPC"/>
        </root>
    </springProfile>

    <!-- 生产环境. 日志级别为INFO且写日志文件-->
    <springProfile name="prod">
        <root level="INFO">
            <appender-ref ref="STDOUT"/>
            <appender-ref ref="FILE_ERROR" />
            <appender-ref ref="FILE_INFO" />
            <appender-ref ref="GRPC"/>
        </root>
    </springProfile>

</configuration>
```

启动服务即可看到日志成功输出至SkyWalking平台