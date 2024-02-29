# Nginx最佳实践
## 什么是Nginx
一个高性能的http和反向代理web服务器

1. 反向代理
2. 集群负载均衡
3. 静态资源代理

## 正向代理与反向代理

### 正向代理

正向代理 是一个位于客户端和原始服务器(origin server)之间的服务器，为了从原始服务器取得内容，
客户端向代理发送一个请求并指定目标(原始服务器)，然后代理向原始服务器转交请求并将获得的内容返回给客户端。

### 反向代理

反向代理（Reverse Proxy）方式是指以代理服务器来接受Internet上的连接请求，
然后将请求转发给内部网络上的服务器；并将从服务器上得到的结果返回给Internet上请求连接的客户端，
此时代理服务器对外就表现为一个服务器。

## Conf配置解析

1. main全局配置
2. event配置工作模式以及连接数
3. http http模块相关配置
4. http.server 虚拟主机配置可以有多个
5. http.server.location 路由配置，表达式
6. http.server.upstream 集群、内网服务器

```
# 设置启动worker进程的用户
user nginx;
# 启动几个worker进程，一般与CPU数相同，如果部署了另外的服务则可以适当减少
worker_processes auto;
error_log /var/log/nginx/error.log;
# nginx进程pid
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    # 每个worker允许连接的客户端最大连接数
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }
}
```

## 静态资源
root和alias都是用来指定请求资源的真实路径

```
location /static/ {
    root /data/w3;
}
```
实际访问 `http://domain.com/static/fac.ico`对应服务器资源地址:`/data/w3/static/fac.ico`

```
location /static/ {
    alias /data/w3/;
}
```
实际访问`http://domain.com/static/fac.ico`对应服务器资源地址:`/data/w3/fac.ico`.

1. alias 只能作用在location中，而root可以存在server、http和location中。
2. alias 后面必须要用 “/” 结束，否则会找不到文件，而 root 则对 ”/” 可有可无。

### 跨域访问

跨域测试
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>this is the csrf file</title>
    <script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
</head>
<script type="text/javascript">
    $(document).ready(function(){
        console.log("here")
        $.ajax({
            url:"http://localhost:80/static/fac.ico",
            type:"GET",
            success:function(data){
                alert("success!!跨域成功！");
            },
            error:function(){
                alert("fail!!!跨域失败！");
            }
        });
    })
</script>
<body>
</body>
</html>
```

设置允许跨域访问
```
location /static/ {
    # 允许跨域请求的域，*代表所有
    add_header 'Access-Control-Allow-Origin' *;
    # 允许带上cookie请求
    add_header 'Access-Control-Allow-Credentials' 'true';
    # 允许请求的方法，比如 GET/POST/PUT/DELETE
    add_header Access-Control-Allow-Methods' *;
    # 允许请求的header
    add_header 'Access-Control-AlLow-Headers' *;

    root /data/w3;
}
```

注意点:浏览器会自动缓存，需要Ctrl+F5强制刷新页面

### 防盗链

```
location /static/ {
    root /data/w3;
    valid_referers *.imooc.com;
    if ($invalid_referer) {
        return 403;
    }
}
```

Postman设置请求头`Referer:http://www.imooc.com`访问成功

## 负载均衡

```
http {
    # mynet是自定义的命名 在server结构中引用即可
    upstream mynet {    
        # server servername:port  servername可以写主机名或者IP
        server 192.168.1.30:80 max_fails=3 fail_timeout=60s weight=5;
        server 192.168.1.31:80 max_fails=3 fail_timeout=60s weight=5;  
    }

    server {
        listen       80;
        server_name  localhost; 
        location / {
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://mynet;
    }
}
```
### max_fails 

表示尝试出错最大次数，超过后则会标记故障，不会再去请求

### fail_timeout

表示故障等待超时时间，server被标记为故障时，经过fail_timeout等待时间之后会被重新标记为正常状态

### weight

负载均衡权重策略

## HTTPS

### 证书下载
因为我这里申请的是阿里云免费DV SSL 证书，因此以下步骤也基于此。读者也可自行选择其他平台，不过步骤也大同小异，反正最终的目的仅仅是为了得到证书文件以及私钥。
1. 购买阿里云免费DV SSL证书（走个形式）
2. 绑定子域名
3. 验证DNS，提交审核
4. 审核通过后可完成下载

解压后文件如下：
```
*.key
*.pem
```

### 安装配置
这里需要说明一点，因为实际生产环境是使用docker 部署，因此仅需进行文件挂载即可。但和直接在centos上运行的nginx路径、配置等等都是相同的。

1. /etc/nginx目录树(新建cert文件夹,此处省略key、pem文件名)

```
├── cert
│   ├── *.key
│   └── *.pem
├── nginx.conf
├── ...
```

2. nginx.conf 模板

```
server {
    listen 443;#监听的端口
    server_name localhost;#你的域名
    ssl on;
    root html;#网站目录
    index index.html index.htm;#默认访问文件优先顺序
    ssl_certificate   /etc/nginx/cert/*.pem;
    ssl_certificate_key  /etc/nginx/cert/*.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    location / {
        root html;
        index index.html index.htm;
    }
}
```

3. 实际nginx.conf 配置(记得替换域名和证书私钥名称)

```
server {
    server_name localhost;
    listen 80;
    return 301 https://your.domain.com$request_uri;
}

server {
    listen 443;#监听的端口
    server_name your.domain.com;#你的域名
    ssl on;

    ssl_certificate   /etc/nginx/cert/*.pem;
    ssl_certificate_key  /etc/nginx/cert/*.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_redirect     off;
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

        proxy_pass http://192.168.31.40:8080;
    }
}
```

4. 完成
