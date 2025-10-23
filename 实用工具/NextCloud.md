# NextCloud

Nextcloud 是一款开源的、自托管的云存储和协作平台，功能类似于 Google Drive 或 Dropbox，但优点是可以完全控制自己的数据。

核心功能: 文件同步、在线文档编辑、日历、联系人、视频会议等

## 安装部署

```shell
mkdir nextcloud && cd nextcloud
vim docker-compose.yml
```

```ymal
version: '3'

services:
  nextcloud:
    image: nextcloud:latest
    container_name: nextcloud
    ports:
      - "80:80"
    volumes:
      - nextcloud_data:/var/www/html
      - ./apps:/var/www/html/custom_apps
      - ./config:/var/www/html/config
      - ./data:/var/www/html/data
    environment:
      - MYSQL_HOST=db
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_PASSWORD=nextcloud_password
    depends_on:
      - db

  db:
    image: mariadb:10.6
    container_name: nextcloud_db
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW --innodb-file-per-table=1
    volumes:
      - db_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_PASSWORD=nextcloud_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

volumes:
  nextcloud_data:
  db_data:
```

启动服务

```shell
sudo docker compose up -d
```

## 安装后配置

访问 `http://your-server-ip` 或 `http://your-domain.com`，按提示:

1. 创建管理员账户
2. 配置数据库连接
3. 完成初始设置