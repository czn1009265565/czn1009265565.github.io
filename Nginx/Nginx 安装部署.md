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


## Ubuntu

### 1. 更新软件包列表
```shell
sudo apt update
```

### 2. 安装 Nginx

```shell
sudo apt install -y nginx
```

### 启动并设置开机自启

```shell
sudo systemctl start nginx
sudo systemctl enable nginx
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