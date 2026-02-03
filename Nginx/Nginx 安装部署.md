# Nginx 安装部署

## Centos7

### 1. 更新yum源

```shell
yum -y update
```
### 2. 安装Nginx

```shell
yum install epel-release
yum install nginx
```

### 3. 启动并设置开机自启
```shell
systemctl start nginx
systemctl enable nginx
```

### 4. 卸载Nginx
```shell
# 关闭nginx服务
systemctl stop nginx
# 关闭开机自启
systemctl disable nginx
# 卸载nginx软件包
yum remove nginx

# 删除配置文件及目录
rm -rf /etc/nginx
rm -rf /var/log/nginx
rm -rf /usr/share/nginx
rm -rf /var/cache/nginx
```

## Ubuntu

### 1. 更新软件包列表
```shell
sudo apt update
```

### 2. 安装 Nginx

```shell
sudo apt install -y nginx
```

### 3. 启动并设置开机自启

```shell
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 4. 卸载Nginx
```shell
# 关闭nginx服务
sudo systemctl stop nginx
# 关闭开机自启
sudo systemctl disable nginx
# 卸载nginx软件包
sudo apt remove nginx nginx-common

# 删除配置文件及目录
sudo rm -rf /etc/nginx
sudo rm -rf /var/log/nginx
sudo rm -rf /var/www/html
sudo rm -rf /usr/share/nginx
```

## 常用命令

```shell
# 查看状态
systemctl status nginx

# 查看配置文件地址，并检查语法
nginx -t

# 重新加载配置
nginx -s reload
```