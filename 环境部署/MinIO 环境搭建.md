# MinIO 环境搭建

## Windows
1. 下载 `https://dl.min.io/server/minio/release/windows-amd64/minio.exe`

2. 启动服务 `minio.exe server D:\software\minio\data --console-address :9090`

3. 浏览器访问 `http://127.0.0.1:9090` 账号密码 minioadmin/minioadmin

## Single-Node Single-Drive

1. 拉取镜像

```shell
# quay.io
docker pull quay.io/minio/minio
```

2. 创建配置文件

```shell
vim /etc/default/minio

MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_VOLUMES="/home/app/minio"
MINIO_OPTS="--console-address :9090"
```

3. 启动容器

```shell
docker run -dt                                  \
  -p 9000:9000 -p 9090:9090                     \
  -v PATH:/mnt/data                             \
  -v /etc/default/minio:/etc/config.env         \
  -e "MINIO_CONFIG_ENV_FILE=/etc/config.env"    \
  --name "minio_single"                         \
  --restart=always                              \
  quay.io/minio/minio server --console-address ":9090"

# 查看容器启动状态
docker logs minio_single
```

4. 访问MinIO `http://localhost:9090`