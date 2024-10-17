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