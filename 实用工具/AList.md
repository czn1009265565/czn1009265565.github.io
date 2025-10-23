# AList

创建 `docker-compose.yml` 文件:

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