## MinIO安装部署
MinIO 基于 Apache License v2.0 开源协议的对象存储服务，兼容亚马逊 S3（ Simple Storage Service 简单存储服务）云存储服务接口，
非常适合于存储大容量非结构化的数据，例如图片、视频、静态页面等，一个对象文件可以是任意大小，文件大小最大支持 5T。

### 下载
这里采用二进制文件的安装方式

```shell
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/
```

### 配置 systemctl 启动
```shell
vim /usr/lib/systemd/system/minio.service
```

```shell
[Unit]
Description=MinIO
Documentation=https://min.io/docs/minio/linux/index.html
Wants=network-online.target
After=network-online.target
AssertFileIsExecutable=/usr/local/bin/minio

[Service]
WorkingDirectory=/usr/local

User=minio-user
Group=minio-user
ProtectProc=invisible

EnvironmentFile=-/etc/default/minio
ExecStartPre=/bin/bash -c "if [ -z \"${MINIO_VOLUMES}\" ]; then echo \"Variable MINIO_VOLUMES not set in /etc/default/minio\"; exit 1; fi"
ExecStart=/usr/local/bin/minio server $MINIO_OPTS $MINIO_VOLUMES

Restart=always

LimitNOFILE=65536

TasksMax=infinity

TimeoutStopSec=infinity
SendSIGKILL=no

[Install]
WantedBy=multi-user.target
```

若配置文件内容所述的用户信息，则需要创建相应的用户和用户组，并赋予权限

```shell
groupadd -r minio-user
useradd -M -r -g minio-user minio-user
chown minio-user:minio-user /home/data1 /home/data2 /home/data3 /home/data4
```

### 新增配置文件

```shell
vim /etc/default/minio
```

```shell
MINIO_ROOT_USER=myminioadmin
MINIO_ROOT_PASSWORD=myminioadmin

MINIO_VOLUMES="/home/data{1...4}"

MINIO_OPTS="--console-address :9001"
```
若磁盘文件夹名不连续，请自行到官方文档查阅处理方法

### 启动服务
**启动服务**
```shell
sudo systemctl start minio.service
```

**确认服务状态**
```shell
sudo systemctl status minio.service
journalctl -f -u minio.service
```

**设置开机自启**
```shell
sudo systemctl enable minio.service
```
