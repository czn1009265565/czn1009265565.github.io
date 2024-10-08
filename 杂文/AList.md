# AList

docker-compose.yml

```yaml
services:
  alist:
    image: 'xhofe/alist-aria2:latest'
    container_name: alist
    volumes:
      - '/home/app/alist/meta:/opt/alist/data'
      - '/home/app/alist/data:/root/data'
    ports:
      - '5244:5244'
    environment:
      - PUID=0
      - PGID=0
      - UMASK=022
    restart: always
```

默认账号admin

#### 获取密码

```shell
# 低于v3.25.0版本
docker exec -it alist ./alist admin

# 高于v3.25.0版本
# 随机生成一个密码
docker exec -it alist ./alist admin random
# 手动设置一个密码,`NEW_PASSWORD`是指你需要设置的密码
docker exec -it alist ./alist admin set NEW_PASSWORD
```

官方文档: `https://alist.nn.ci/zh/guide/`

## 阿里云盘挂载

1. 驱动选择 `阿里云盘Open`
2. 由于国内无法连接，因此需要修改Oauth令牌链为如下任意链接

- https://api-cf.nn.ci/alist/ali_open/token
- https://api.xhofe.top/alist/ali_open/token

3. 设置刷新令牌 访问 `https://alist.nn.ci/tool/aliyundrive/request` 并登录获取Token

## 百度网盘挂载

[获取token](https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=iYCeC9g08h5vuP9UqvPHKKSVrKFXGa1v&redirect_uri=https://alist.nn.ci/tool/baidu/callback&scope=basic,netdisk&qrcode=1)

填写刷新令牌、客户端ID、客户端密钥

## PotPlayer配置WebDAV
1. 设置专辑名称
2. 选择FTP/WebDAV/HTTP搜索

- 协议: WebDAV
- 主机/路径: 172.30.255.101/dav/
- 端口: 5244
- 用户名: admin
- 密码: password

## 种子文件下载

曲线救国

1. 上传种子文件
2. 复制连接
3. 离线下载输入链接

## 百度网盘文件下载

1. 复制
2. 选择目标文件夹至阿里网盘
3. 阿里网盘PC实现文件下载
