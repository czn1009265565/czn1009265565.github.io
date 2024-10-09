# SkyWalking

## 简介
Skywalking 时一个开源的分布式追踪系统，用于检测、诊断和优化分布式系统的功能。
它可以帮助开发者和运维人员深入了解分布式系统中各个组件之间的调用关系、性能瓶颈以及异常情况，从而提供系统级的性能优化和故障排查。

![架构](./imgs/SkyWalking.jpg)


## 单机环境搭建

官方下载地址: https://skywalking.apache.org/downloads/

```shell
# 解压
tar -zxvf apache-skywalking-apm-bin.tar.gz
```

### SkyWalking OAP 搭建

修改配置文件(这里主要修改存储配置)  
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

### SkyWalking UI 搭建

修改配置文件  
```shell
vim webapp/application.yml
```

启动 SkyWalking UI 服务
```shell
bin/webappService.sh
```

查看日志详情
```shell
tail -200f logs/skywalking-webapp.log
```

访问UI界面  `http://127.0.0.1:8080`


## SkyWalking Agent 搭建

配置启动脚本
```shell
# SkyWalking Agent 配置
export SW_AGENT_NAME=blog
export SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.0.0.1:11800
export SW_AGENT_SPAN_LIMIT=2000
export JAVA_AGENT=-javaagent:/home/app/skywalking-agent/skywalking-agent.jar

# 启动服务
java $JAVA_AGENT -jar blog.jar
```

## 性能指标