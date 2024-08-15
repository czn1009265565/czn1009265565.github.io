# Flume
Apache Flume 是一个分布式、可靠、高可用的日志收集、聚合和传输系统。它常用于将大量日志数据从不同的源(如Web服务器、应用程序、传感器等)收集到中心化的存储或数据处理系统中。

## Flume安装部署
下载地址：http://archive.apache.org/dist/flume/

### 前置准备

JDK安装部署

### 解压安装

```shell
tar -zxf apache-flume-1.10.1-bin.tar.gz -C /opt/module/
mv /opt/module/apache-flume-1.10.1-bin /opt/module/flume
```

**日志存储路径**  
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="ERROR">
  <Properties>
    <!-- 配置对应的日志存储路径 -->
    <Property name="LOG_DIR">/opt/module/flume/log</Property>
  </Properties>
  <Appenders>
    <Console name="Console" target="SYSTEM_ERR">
      <PatternLayout pattern="%d (%t) [%p - %l] %m%n" />
    </Console>
    <RollingFile name="LogFile" fileName="${LOG_DIR}/flume.log" filePattern="${LOG_DIR}/archive/flume.log.%d{yyyyMMdd}-%i">
      <PatternLayout pattern="%d{dd MMM yyyy HH:mm:ss,SSS} %-5p [%t] (%C.%M:%L) %equals{%x}{[]}{} - %m%n" />
      <Policies>
        <!-- Roll every night at midnight or when the file reaches 100MB -->
        <SizeBasedTriggeringPolicy size="100 MB"/>
        <CronTriggeringPolicy schedule="0 0 0 * * ?"/>
      </Policies>
      <DefaultRolloverStrategy min="1" max="20">
        <Delete basePath="${LOG_DIR}/archive">
          <!-- Nested conditions: the inner condition is only evaluated on files for which the outer conditions are true. -->
          <IfFileName glob="flume.log.*">
            <!-- Only allow 1 GB of files to accumulate -->
            <IfAccumulatedFileSize exceeds="1 GB"/>
          </IfFileName>
        </Delete>
      </DefaultRolloverStrategy>
    </RollingFile>
  </Appenders>

  <Loggers>
    <Logger name="org.apache.flume.lifecycle" level="info"/>
    <Logger name="org.jboss" level="WARN"/>
    <Logger name="org.apache.avro.ipc.netty.NettyTransceiver" level="WARN"/>
    <Logger name="org.apache.hadoop" level="INFO"/>
<Logger name="org.apache.hadoop.hive" level="ERROR"/>
    <Root level="INFO">
      <AppenderRef ref="LogFile" />
	  <!-- 新增控制台输出 -->
      <AppenderRef ref="Console" />
    </Root>
  </Loggers>
</Configuration>
```

**验证**  
```shell
/opt/module/flume/bin/flume-ng version
```


## 基本概念
![flume](imgs/flume.png)

- Agent(代理): Flume 中的基本工作单元，用于数据的采集、传输和处理。
- Source(数据源): 代理中的组件，负责接收和发送数据到 Flume。
- Channel(通道): 用于临时存储数据的缓冲区，用于在 Source 和 Sink 之间传输数据。
- Sink(数据目的地): 代理中的组件，负责将数据传送到指定的目的地，如 HDFS、Kafka es等。


## 日志采集

### 创建Flume配置文件

```shell
mkdir /opt/module/flume/job
vim /opt/module/flume/job/file_to_kafka.conf
```

**配置文件内容如下**  
```properties
#定义组件
a1.sources = r1
a1.channels = c1

#配置source
a1.sources.r1.type = TAILDIR
a1.sources.r1.filegroups = f1
a1.sources.r1.filegroups.f1 = /opt/module/applog/log/app.*
a1.sources.r1.positionFile = /opt/module/flume/taildir_position.json

#配置channel
a1.channels.c1.type = org.apache.flume.channel.kafka.KafkaChannel
a1.channels.c1.kafka.bootstrap.servers = hadoop101:9092,hadoop102:9092
a1.channels.c1.kafka.topic = topic_log
a1.channels.c1.parseAsFlumeEvent = false

#组装 
a1.sources.r1.channels = c1
```

**启动采集任务**  
```shell
/opt/module/flume/bin/flume-ng agent -n a1 -c /opt/module/flume/conf/ -f /opt/module/flume/job/file_to_kafka.conf
```