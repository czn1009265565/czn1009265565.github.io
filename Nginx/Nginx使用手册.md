# Nginx使用手册

## 功能

- HTTP 服务器：处理 HTTP 请求并向客户端提供内容。
- 反向代理：将来自客户端的请求转发到另一台服务器或一组服务器。
- 负载均衡：将流量分配给多台服务器，以提高性能和可用性。
- 缓存：暂存经常访问的内容，以减少服务器负载和提高页面加载速度。
- Web 应用程序防火墙：保护应用程序免遭恶意流量和攻击。
- SSL/TLS 终结：处理加密的 HTTPS 连接，为网站提供安全性和隐私。

## 编译安装

[下载链接](https://nginx.org/en/download.html)

选择稳定版本(Stable version)即可

```shell
# 默认安装安装路径为/usr/local/nginx
./configure --prefix=/usr/local/nginx
make
sudo make install
```

## 基础命令
不像许多其他软件系统，Nginx 仅有几个命令行参数，完全通过配置文件来配置  

- -c 为 Nginx 指定一个配置文件，来代替缺省的。
- -t 不运行，而仅仅测试配置文件。nginx 将检查配置文件的语法的正确性，并尝试打开配置文件中所引用到的文件。
- -v 显示 nginx 的版本。
- -V 显示 nginx 的版本，编译器版本和配置参数。

1. 启动 `sudo /usr/local/nginx/nginx`
2. 停止  
   ```shell
   ps aux | grep nginx
   kill -9 nginx主进程号
   ```
3. 平滑重启  
   ```shell
   # 先测试配置文件
   nginx -t -c /etc/nginx/nginx.conf
   nginx -s reload
   ```
   
## 指令

配置文件:  
```
#user  nobody;
worker_processes  1;

#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   html;
            index  index.html index.htm;
        }
    }
}
```

- user: 指定Nginx Worker进程运行用户
- worker_processes: 启动几个worker进程，一般与CPU数相同，如果部署了另外的服务则可以适当减少
- worker_connections: 每个worker允许连接的客户端最大连接数
- include: 加载外部配置文件
- client_max_body_size: 限制上传/下载文件大小，例如 100m
- listen: 监听端口
- location: 对Http请求中的URI匹配处理，优先级顺序如下
  1. `location = /uri`: 精确匹配
  2. `location ^~ /uri`: 前缀匹配
  3. `location ~ pattern` 　区分大小写的正则匹配
  4. `location ~* pattern` 　不区分大小写的正则匹配
  5. `location /uri` 　　　　不带任何修饰符，也表示前缀匹配
  6. `location /` 　　　　　通用匹配，任何未匹配到其它location的请求都会匹配到，相当于switch中的default。
- root: 指定web根目录
    ```
    location /static/ {
        root /data/w3;
    }
    ```
访问 `http://domain.com/static/fac.ico` 对应服务器资源地址: `/data/w3/static/fac.ico`

- alias，定义只能作用在location中，且后面必须要用 “/” 结束
    ```
    location /static/ {
        alias /data/w3/;
    }
    ```
访问`http://domain.com/static/fac.ico` 对应服务器资源地址: `/data/w3/fac.ico`
- deny/allow: 控制对特定IP地址的访问
    ```
    location / {
        allow   192.168.1.0/24;
        allow   10.1.1.0/16;
        deny    all;
    }
    ```
在上面的例子中,仅允许网段 10.1.1.0/16 和 192.168.1.0/24 ip访问


## 案例

### 静态代理
#### root
```
location /static/ {
    root /data/w3;
}
```
访问 `http://domain.com/static/fac.ico` 对应服务器资源地址: `/data/w3/static/fac.ico`

#### alias
```
location /static/ {
    alias /data/w3/;
}
```
访问`http://domain.com/static/fac.ico` 对应服务器资源地址: `/data/w3/fac.ico`

### 负载均衡

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

- max_fails: 表示尝试出错最大次数，超过后则会标记故障，不会再去请求
- fail_timeout: 表示故障等待超时时间，server被标记为故障时，经过fail_timeout等待时间之后会被重新标记为正常状态
- weight: 负载均衡权重策略
- proxy_pass: 代理转发，注意点: proxy_pass的url以`/`结尾代表绝对路径，反之则代表相对路径  
  请求示例: http://192.168.1.100/static/favicon.ico
  ```
  location /static/ {
      proxy_pass http://127.0.0.1;
  }
  ```
  代理URL: http://127.0.0.1/static/favicon.ico  
  ```
  location /static/ {
      proxy_pass http://127.0.0.1/;
  }
  ```
  代理URL: http://127.0.0.1/favicon.ico

### Https

#### 生成自签名证书

```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
```
输入任意的国家、省、城市、组织、邮箱即可，自签名证书仅用于测试。

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

        proxy_pass http://192.168.1.100:8080;
    }
}
```

### 跨域
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