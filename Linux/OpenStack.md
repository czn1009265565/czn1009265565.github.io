# OpenStack

## DevStack

[参考官网DevStack安装文档](https://docs.openstack.org/devstack/latest/)

本文部署采用 `Ubuntu 22.04`

### 新增Stack用户 

```shell
sudo useradd -s /bin/bash -d /opt/stack -m stack
sudo chmod +x /opt/stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
sudo -u stack -i
```

### 下载DevStack

```shell
git clone https://opendev.org/openstack/devstack
cd devstack
```

### 创建本地配置文件
```shell
vim local.conf

[[local|localrc]]
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
```

### 开始安装

```shell
./stack.sh
```
这个过程等待15-30分钟即可。