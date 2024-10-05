# Redis 安装部署

### 更新YUM源

```shell
sudo yum install epel-release
```

### 安装Redis
```shell
sudo yum install redis -y
```

### 启动Redis

```shell
sudo systemctl start redis.service
sudo systemctl enable redis
```

### 查看状态

```shell
sudo systemctl status redis.service
```

### 绑定IP

```shell
sudo vim /etc/redis.conf

# 新增绑定内网IP
bind 127.0.0.1 192.168.1.101

# 重启服务
sudo systemctl restart redis
```