## Nginx 安装部署

### 更新yum源

```shell
yum -y update
```
### 安装Nginx

```shell
yum install epel-release
yum install nginx
```
### 启动服务
```shell
systemctl start nginx
```

### 设置开启自启

```shell
systemctl enable nginx
```

### 查看服务状态

```shell
systemctl status nginx
```
### 查看配置文件地址

```shell
nginx -t
```
### 重新加载配置

```shell
nginx -s reload 
```

### Nginx配置示例

```
http {
    upstream mynet {    
        #mynet是自定义的命名 在server结构中引用即可
        #max_fails 表示尝试出错最大次数 即可认为该服务器 在fail_timeout时间内不可用
        # server servername:port   servername可以写主机名 或者点分式IP
        server 192.168.1.30:80 max_fails=1 fail_timeout=300s;
        server 192.168.1.31:80 max_fails=1 fail_timeout=300s;  
    }

    server {
        listen       80;
        server_name  localhost; 
        location / {
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme; #https,http
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://mynet;
    }
}  
```