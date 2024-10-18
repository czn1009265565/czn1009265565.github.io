## Spring Boot 整合 Logback

### Configuration
主要划分为以下三个核心配置

1. appender: 负责写日志的组件,主要用于配置输出格式，日志回滚策略，日志最大历史
2. logger: 用来设置某一个包或者具体的某一个类的日志打印级别以及指定appender
3. root: 根logger，也是一种logger，且只有一个level属性

### 案例
如下为一个传统的logback.xml示例

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
        <logger name="com.company.projectName" additivity="false">
            <appender-ref ref="STDOUT"/>
        </logger>
        <root level="INFO">
            <appender-ref ref="STDOUT"/>
        </root>
    </springProfile>

    <!-- 生产环境. 日志级别为INFO且写日志文件-->
    <springProfile name="prod">
        <logger name="com.company.projectName" additivity="false">
            <appender-ref ref="STDOUT"/>
            <appender-ref ref="FILE_ERROR" />
            <appender-ref ref="FILE_INFO" />
        </logger>

        <root level="INFO">
            <appender-ref ref="STDOUT"/>
            <appender-ref ref="FILE_ERROR" />
            <appender-ref ref="FILE_INFO" />
        </root>
    </springProfile>

</configuration>
```

1. 日志文件存储路径修改 `<property name="LOG_HOME" value="app/logs/"/>`
2. 修改logger日志监听的包路径，删除logger则表示监听所有包路径
