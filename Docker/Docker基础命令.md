# Docker基础命令

## 镜像操作

### 构建镜像
编写Dockerfile文件

```shell
docker build -t image_name:tag .
```

### 获取镜像

```shell
# 完整命令 
docker pull docker.io/library/ubuntu:18.04
# 简写 
docker pull ubuntu:18.04
```
- `docker.io` Docker 镜像仓库地址
- `library/ubuntu` 仓库名。这里的仓库名是两段式名称，即 <用户名>/<软件名>。对于 Docker Hub，如果不给出用户名，则默认为 library，也就是官方镜像。
- `18.04` 标签


### 运行镜像

```shell
docker run -it --rm ubuntu:18.04 bash
```
- `-it`：这是两个参数，一个是 `-i`：交互式操作，一个是 `-t` 终端。我们这里打算进入 `bash` 执行一些命令并查看返回结果，因此我们需要交互式终端。

- `--rm`：这个参数是说容器退出后随之将其删除

- `ubuntu:18.04`：这是指用 ubuntu:18.04 镜像为基础来启动容器。
- `bash`：放在镜像名后的是 命令，这里我们希望有个交互式 Shell，因此用的是 bash。

### 列出镜像

```shell
docker image ls
```

### 删除镜像

```shell
docker image rm image_name
```
其中，`image_name` 可以是 镜像短 ID、镜像长 ID、镜像名 或者 镜像摘要。

### 启动容器

```shell
# 基于镜像启动容器
docker run --name redis -d -p 6379:6379 redis

# 启动已终止容器
docker container start container_name
```

- `--name` 自定义容器名称
- `-d` 以后台的方式运行
- `-p` 设置端口映射 主机端口:容器端口

### 导出镜像

```shell
docker image ls

REPOSITORY                 TAG              IMAGE ID       CREATED        SIZE
ubuntu                     22.04            52882761a72a   2 months ago   77.9MB

docker save 52882761a72a > ubuntu.tar
```

### 导入镜像

```shell
# 导入镜像
docker load < image.tar

docker image ls

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
<none>       <none>    52882761a72a   2 months ago   77.9MB

# 重命名标签
docker tag a9bd596c9448 ubuntu:22.04
```

## 容器操作

### 终止容器

```shell
docker container stop container_name
```

### 进入容器

```shell
docker exec -it container_name bash
```

### 导出容器

```shell
docker container ls

CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS         PORTS     NAMES
ea98b962471f   ubuntu:18.04   "/bin/bash"   4 minutes ago   Up 4 minutes             friendly_solomon

docker export ea98b962471f > ubuntu.tar
```

### 导入容器

```shell
# 从本地文件导入
cat ubuntu.tar | docker import - test/ubuntu:v1.0

# 从URL导入
docker import http://example.com/exampleimage.tgz example/imagerepo
```

### 删除容器

```shell
# 删除容器
docker container rm container_name

# 强制删除运行中的容器
docker container rm -f container_name

# 清理所有处于终止状态的容器
docker container prune
```

## 数据操作
数据卷的概念

- 数据卷 可以在容器之间共享和重用
- 对 数据卷 的修改会立马生效
- 对 数据卷 的更新，不会影响镜像
- 数据卷 默认会一直存在，即使容器被删除

### 创建数据卷

```shell
docker volume create volume_name
```

### 查看数据卷

```shell
docker volume ls
```

### 挂载数据卷

```shell
docker run -d --name nginx -v volume_name:/usr/share/nginx/html nginx:alpine
```
这里创建一个名为 `nginx` 的容器，并加载一个 `数据卷` 到容器的 `/usr/share/nginx/html` 目录。

### 删除数据卷

```shell
docker volume rm volume_name
```

### 挂载主机目录

```shell
docker run -d --name web -v /src/webapp:/usr/share/nginx/html nginx:alpine
```
上面的命令加载主机的 `/src/webapp` 目录到容器的 `/usr/share/nginx/html` 目录。

### 挂载主机文件

```shell
docker run -d --name web -v ./nginx.conf:/etc/nginx/nginx.conf nginx:alpine
```
上面的命令加载主机的当前路径下的 `nginx.conf` 文件覆盖容器中的 `/etc/nginx/nginx.conf` 文件


## 网络操作

### 外部访问

容器外部访问容器则可以通过将容器端口映射至宿主机指定端口，以 `hostPort:containerPort` 的格式

```shell
docker run -d -p 80:80 -p 443:443 nginx:alpine
```

### 容器互联

容器内部互相访问，建议将容器加入自定义的 Docker 网络来连接多个容器

```shell
# 创建bridge网络(适用于单机)
docker network create -d bridge network_name

docker run -it --rm --name busybox1 --network network_name busybox sh
docker run -it --rm --name busybox2 --network network_name busybox sh
```

容器间可以通过容器名相互访问，
在 busybox1 容器执行 `ping busybox2`, 同理在 `busybox2` 容器执行 `ping busybox1`。
