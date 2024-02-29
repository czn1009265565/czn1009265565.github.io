# Docker安装部署

## 安装部署

### 系统要求
Docker 支持 64 位版本 CentOS 7/8，并且要求内核版本不低于 3.10。 CentOS 7 满足最低内核的要求，但由于内核版本比较低，部分功能（如 overlay2 存储层驱动）无法使用，并且部分功能可能不太稳定.

### 卸载旧版本
旧版本的 Docker 称为 docker 或者 docker-engine，使用以下命令卸载旧版本：
```shell
sudo yum remove docker \
                docker-client \
                docker-client-latest \
                docker-common \
                docker-latest \
                docker-latest-logrotate \
                docker-logrotate \
                docker-selinux \
                docker-engine-selinux \
                docker-engine
```
### yum安装

安装依赖包
```shell
sudo yum install -y yum-utils
```


鉴于国内网络问题，强烈建议使用国内源，官方源请在注释中查看。
执行下面的命令添加 yum 软件源：
```shell
sudo yum-config-manager \
    --add-repo \
    https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

sudo sed -i 's/download.docker.com/mirrors.aliyun.com\/docker-ce/g' /etc/yum.repos.d/docker-ce.repo

# 官方源
# sudo yum-config-manager \
#     --add-repo \
#     https://download.docker.com/linux/centos/docker-ce.repo
```

安装Docker
```shell
sudo yum install docker-ce docker-ce-cli containerd.io
```

### CentOS8额外设置
由于 CentOS8 防火墙使用了 `nftables`，但 Docker 尚未支持 `nftables`， 我们可以使用如下设置使用 `iptables`：
更改 `/etc/firewalld/firewalld.conf`
```shell
# FirewallBackend=nftables
FirewallBackend=iptables
```
或者执行如下命令：
```shell
firewall-cmd --permanent --zone=trusted --add-interface=docker0

firewall-cmd --reload
```

### 启动Docker
```shell
sudo systemctl enable docker
sudo systemctl start docker
```

### 验证Docker是否安装成功
```shell
docker run --rm hello-world
```


## 镜像配置
由于镜像服务可能出现宕机，建议同时配置多个镜像，这里同时配置网易、百度、阿里云镜像加速服务。

### 查看是否配置过镜像地址

```shell
systemctl cat docker | grep '\-\-registry\-mirror'
```
如果以上命令没有任何输出，那么就可以在 /etc/docker/daemon.json 中写入如下内容（如果文件不存在请新建该文件）：

```shell
vim /etc/docker/daemon.json

{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://4z8dhcx.mirror.aliyuncs.com"
  ]
}
```

重启服务
```shell
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 代理配置

### dockerd网络代理
"docker pull" 命令是由 dockerd 守护进程执行。而 dockerd 守护进程是由 systemd 管理。因此，如果需要在执行 "docker pull" 命令时使用 HTTP/HTTPS 代理，需要通过 systemd 配置。

1. 为 dockerd 创建配置文件夹

```shell
sudo mkdir -p /etc/systemd/system/docker.service.d
```

2. 为 dockerd 创建 HTTP/HTTPS 网络代理的配置文件，文件路径是 `/etc/systemd/system/docker.service.d/http-proxy.conf`。并在该文件中添加相关环境变量。

```shell
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

3. 刷新配置并重启服务

```shell
sudo systemctl daemon-reload
sudo systemctl restart docker
```