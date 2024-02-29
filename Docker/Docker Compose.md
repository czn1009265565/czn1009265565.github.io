# Docker Compose

## 介绍
在日常工作中，经常会碰到需要多个容器相互配合来实现功能。例如要实现一个 Web 项目，除了 Web 服务容器本身，往往还需要再加上后端的数据库服务容器，甚至还包括负载均衡容器等。
Compose 恰好满足了这样的需求。它允许用户通过一个单独的 `docker-compose.yml` 模板文件（YAML 格式）来定义一组相关联的应用容器为一个项目（project）。

## 安装与卸载

### 二进制包

```shell
# 安装
sudo curl -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 卸载
rm /usr/local/bin/docker-compose
```

### pip安装
通过pip的方式安装较为简单快捷，但是前提是需要安装Python3环境

```shell
# 安装
pip3 install docker-compose

# 卸载
pip3 uninstall docker-compose
```

## 命令

```shell
docker-compose
-f, --file FILE 指定使用的 Compose 模板文件,默认为 docker-compose.yml,可以多次指定.
-p, --project-name NAME 指定项目名称,默认将使用所在目录名称作为项目名

# 根据Dockerfile文件构建镜像
docker-compose build

# 后台方式启动项目
docker-compoes up -d

# 停止项目
docker-compose down
```

## 模板文件

这里以ELK官方Docker Compose文件为例介绍

### 文件目录

```
├── docker-compose.yml
├── elasticsearch
│   ├── config
│   │   └── elasticsearch.yml
│   └── Dockerfile
├── kibana
│   ├── config
│   │   └── kibana.yml
│   └── Dockerfile
└── logstash
    ├── config
    │   └── logstash.yml
    ├── Dockerfile
    └── pipeline
        └── logstash.conf
```

### 配置文件

`.env`配置

```
ELASTIC_VERSION=8.8.1

ELASTIC_PASSWORD='password'
LOGSTASH_INTERNAL_PASSWORD='password'
KIBANA_SYSTEM_PASSWORD='password'
```

### Dockerfile
elasticsearch Dockerfile

```
ARG ELASTIC_VERSION

FROM docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION}
```

logstash Dockerfile

```
ARG ELASTIC_VERSION

FROM docker.elastic.co/logstash/logstash:${ELASTIC_VERSION}
```

kibana Dockerfile

```
ARG ELASTIC_VERSION

FROM docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}
```

### Docker Compose文件
```yaml
version: '3.7'

services:
  elasticsearch:
    # 根据Dockerfile构建镜像
    build:
      # 指令指定 Dockerfile 所在文件夹的路径
      context: elasticsearch/
      args:
        # 使用 arg 指令指定构建镜像时的变量
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    # 指定容器名称    
    container_name: elasticsearch
    # 数据卷所挂载路径设置。可以设置为宿主机路径(HOST:CONTAINER)或者数据卷名称(VOLUME:CONTAINER)，并且可以设置访问模式 （HOST:CONTAINER:ro）。
    volumes:
      - ./elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
      - elasticsearch:/usr/share/elasticsearch/data
    # 端口映射 格式: 宿主端口：容器端口 (HOST:CONTAINER)  
    ports:
      - 9200:9200
      - 9300:9300
    # 设置环境变量,支持数组和字典。 例如在elasticsearch.yml配置文件中可用${}获取
    environment:
      node.name: elasticsearch
      ES_JAVA_OPTS: -Xms512m -Xmx512m
      ELASTIC_PASSWORD: ${ELASTIC_PASSWORD}
      discovery.type: single-node
    # 配置容器连接的网络  在同一网络下可根据container_name相互访问
    networks:
      - elk
    # 启动策略: unless-stopped 确保容器在运行docker-compose down命令之前一直运行
    restart: unless-stopped
    # 日志配置
    logging:
      driver: json-file
      options:
        labels: "elasticsearch"

  logstash:
    build:
      context: logstash/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    container_name: logstash
    volumes:
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - 5044:5044
      - 50000:50000/tcp
      - 50000:50000/udp
      - 9600:9600
    environment:
      LS_JAVA_OPTS: -Xms256m -Xmx256m
      LOGSTASH_INTERNAL_PASSWORD: ${LOGSTASH_INTERNAL_PASSWORD}
    networks:
      - elk
    # 解决容器的依赖、启动先后的问题  
    depends_on:
      - elasticsearch
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        labels: "logstash"

  kibana:
    build:
      context: kibana/
      args:
        ELASTIC_VERSION: ${ELASTIC_VERSION}
    container_name: kibana
    volumes:
      - ./kibana/config/kibana.yml:/usr/share/kibana/config/kibana.yml
    ports:
      - 5601:5601
    environment:
      KIBANA_SYSTEM_PASSWORD: ${KIBANA_SYSTEM_PASSWORD}
    networks:
      - elk
    depends_on:
      - elasticsearch
    restart: unless-stoppe
    logging:
      driver: json-file
      options:
        labels: "kibana"

networks:
  elk:
    driver: bridge

volumes:
  elasticsearch:
```

