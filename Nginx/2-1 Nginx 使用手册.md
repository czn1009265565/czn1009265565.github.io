# Nginx 使用手册

高性能的 HTTP/反向代理服务器、负载均衡器、缓存服务器。

主要功能: 

- HTTP 服务器: 处理 HTTP 请求并向客户端提供内容。
- 反向代理: 将来自客户端的请求转发到另一台服务器或一组服务器。
- 负载均衡: 将流量分配给多台服务器，以提高性能和可用性。
- 缓存: 暂存经常访问的内容，以减少服务器负载和提高页面加载速度。
- Web 应用程序防火墙: 保护应用程序免遭恶意流量和攻击。
- SSL/TLS 终结: 处理加密的 HTTPS 连接，为网站提供安全性和隐私。

## 目录结构

```
/etc/nginx/
├── nginx.conf          # 主配置文件
├── conf.d/             # 额外配置文件目录
├── sites-available/    # 可用站点配置
├── sites-enabled/      # 已启用站点配置（符号链接）
├── modules-available/  # 可用模块
├── modules-enabled/    # 已启用模块
└── snippets/           # 配置片段

/var/log/nginx/         # 日志文件目录
/var/www/html/          # 默认网站根目录
/usr/share/nginx/html/  # 另一个常见根目录
```

## 配置文件

主配置
```
# 全局块 - 影响 Nginx 整体运行
user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;

# Events 块 - 连接处理配置
events {
    worker_connections 1024;
    # multi_accept on;
}

# HTTP 块 - 主要配置区域
http {
    # 启用高效文件传输（零拷贝）
    sendfile on;
    # 在sendfile模式下，等待数据包填满再发送，提高网络效率
    tcp_nopush on;
    # 禁用Nagle算法，降低小数据包的延迟
    tcp_nodelay on;
    # 客户端连接保持时间65秒
    keepalive_timeout 65;
    # MIME类型哈希表大小
    types_hash_max_size 2048;

    # 引入MIME类型定义文件
    include /etc/nginx/mime.types;
    # 默认MIME类型（二进制流）
    default_type application/octet-stream;

    # SSL 设置
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # 日志格式
    access_log /var/log/nginx/access.log;

    # 启用Gzip压缩
    gzip on;
    # 根据Accept-Encoding头动态决定是否压缩
    gzip_vary on;
    # 只压缩大于1KB的文件
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    # 包含其他配置
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

## 核心配置指令

### Location 匹配规则

```
# 精确匹配（最高优先级）
location = /exact-path {
    # 只匹配 /exact-path
}

# 前缀匹配（禁止继续搜索正则）
location ^~ /static/ {
    # 匹配以 /static/ 开头的路径
}

# 正则匹配（区分大小写）
location ~ \.php$ {
    # 匹配 .php 结尾的路径
}

# 正则匹配（不区分大小写）
location ~* \.(jpg|jpeg|png)$ {
    # 匹配图片文件
}

# 普通前缀匹配（最低优先级）
location / {
    # 匹配所有路径
}
```

### 反向代理配置

```
server {
    listen       80;
    server_name  localhost;
    location / {
        proxy_pass http://backend_server:8080;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 支持http长连接
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

注意点: proxy_pass的url以`/`结尾代表绝对路径，反之则代表相对路径。
这里以请求 `http://127.0.0.1/static/favicon.ico` 为例
```
# 代理URL http://127.0.0.1:8080/static/favicon.ico
location /static/ {
    proxy_pass http://127.0.0.1:8080;
}

# 代理URL: http://127.0.0.1:8080/favicon.ico
location /static/ {
    proxy_pass http://127.0.0.1:8080/;
}
```

### 负载均衡配置

```
http {
    # backend_server是自定义的命名 在server结构中引用即可
    upstream backend_server {
        # server servername:port  servername可以写主机名或者IP
        server 192.168.1.101:8080 max_fails=3 fail_timeout=60s weight=1;
        server 192.168.1.102:8080 max_fails=3 fail_timeout=60s weight=1;
    }

    server {
        listen       80;
        server_name  localhost;
        location / {
            proxy_pass http://backend_server:8080;
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            
            # 支持http长连接
            proxy_http_version 1.1;
            proxy_set_header Connection "";
        }
    }
}
```

### 静态代理

#### root
```
location /static/ {
    root /data/w3;
}
```
访问 `http://localhost/static/fac.ico` 对应服务器资源地址: `/data/w3/static/fac.ico`

#### alias
```
location /static/ {
    alias /data/w3/;
}
```
访问`http://localhost/static/fac.ico` 对应服务器资源地址: `/data/w3/fac.ico`


### 反向代理与静态文件分离

```
server {
    listen 80;
    server_name localhost;
    
    # 静态文件由 Nginx 直接处理
    location /static/ {
        alias /var/www/static/;
        expires 1d;
        add_header Cache-Control "public";
    }
    
    # 其他请求转发到后端
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 支持http长连接
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```


### Https

#### 生成自签名证书

```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
```
输入任意的国家、省、城市、组织、邮箱即可，自签名证书仅用于测试

#### nginx.conf配置

```
server {
    server_name localhost;
    listen 80;
    return 301 https://$host$request_uri;
}

server {
    listen 443;#监听的端口
    server_name localhost;#你的域名
    ssl on;

    ssl_certificate   /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key  /etc/nginx/ssl/nginx.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_redirect     off;
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

        proxy_pass http://localhost:8080;
    }
}
```