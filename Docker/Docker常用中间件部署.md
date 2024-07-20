# Docker常用中间件部署
本文用于记录Docker 简洁 部署中间件 应用，用户快速实现代码集成，并不能用于生产环境开发使用

## MySQL：

```shell
docker run --name=mysql \
  -p 33060:3306 \
  -v /root/mysql/conf:/etc/mysql/conf.d \
  -v /root/mysql/logs:/logs \
  -v /root/mysql/data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD='password' \
  -d mysql:5.7 mysqld
```

## redis

```shell
# 数据卷
docker volume create redis
docker run --name myredis -d -p 6379:6379 -v redis:/data redis redis-server --appendonly yes
# 挂载本地目录
docker run --name myredis -d -p 6379:6379 -v /home/redis/data:/data redis redis-server --appendonly yes
```

## RabbitMQ

```shell
docker run -d --name rabbitmq \
  -v /home/rabbitmq/data:/var/lib/rabbitmq \
  -v /home/rabbitmq/log:/var/log/rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3.7.15-management
```
默认用户名和密码是: `guest/guest`

## Kafka
1.镜像下载

```shell
docker pull wurstmeister/kafka
docker pull wurstmeister/zookeeper
```
2.启动

```shell
docker run -d --name zookeeper -p 2181:2181 -t wurstmeister/zookeeper

docker run --name kafka -p 9092:9092 \
-e KAFKA_BROKER_ID=0 -e KAFKA_ZOOKEEPER_CONNECT=192.168.100.129:2181 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.100.129:9092 \
-e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
-d wurstmeister/kafka
```
3.Kafka Tool 连接使用

## Nginx
Nginx反向代理示例

```yaml
services:
  nginx:
    image: nginx
    container_name: nginx
    volumes:
      - /home/app/nginx/nginx.conf:/etc/nginx/nginx.conf
      - /home/app/nginx/nginx.key:/etc/nginx/cert/nginx.key
      - /home/app/nginx/nginx.crt:/etc/nginx/cert/nginx.crt
    ports:
      - 80:80
      - 443:443
    networks:
      - nginx
    restart: always
networks:
  nginx:
```

nginx.conf

```
#user  nobody;
worker_processes  1;

#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}


http {
    server {
        server_name localhost;
        listen 80;
        return 301 https://172.30.1.101$request_uri;
    }

    server {
        listen 443;#监听的端口
        server_name localhost;#你的域名
        ssl on;

        ssl_certificate   /etc/nginx/cert/nginx.crt;
        ssl_certificate_key  /etc/nginx/cert/nginx.key;
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;

        location / {
            proxy_redirect     off;
            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

            proxy_pass https://192.168.1.100;
        }
    }
}
```
