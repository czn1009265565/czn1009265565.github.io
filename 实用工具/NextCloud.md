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
    restart: unless-stopped
    ports:
      - "8000:80"
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
    restart: unless-stopped
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW --innodb-file-per-table=1
    volumes:
      - db_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_PASSWORD=nextcloud_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  onlyoffice:
    image: onlyoffice/documentserver:latest
    container_name: onlyoffice
    restart: unless-stopped
    ports:
      - "8001:80"
    environment:
      - JWT_ENABLED=false
    volumes:
      - ./onlyoffice/logs:/var/log/onlyoffice
      - ./onlyoffice/data:/var/www/onlyoffice/Data
      - ./onlyoffice/lib:/var/lib/onlyoffice
      - ./onlyoffice/db:/var/lib/postgresql

volumes:
  nextcloud_data:
  db_data:
```

启动服务

```shell
sudo docker compose up -d
```

## 初始化配置

访问 `http://your-server-ip` 或 `http://your-domain.com`，按提示:

1. 创建管理员账户
2. 配置数据库连接
3. 完成初始设置

### 安装 OnlyOffice 插件

1. 登录 Nextcloud 管理员账户
2. 点击右上角用户菜单 → "应用"
3. 在左侧分类中找到 "办公与文本" 或直接搜索 "onlyoffice"
4. 找到 "ONLYOFFICE" 应用并点击"下载并启用"

### 配置 OnlyOffice 连接

1. 在 Nextcloud 中点击右上角用户菜单 → "设置"
2. 在左侧菜单中选择 "ONLYOFFICE"
3. 配置文档服务器地址
4. 文档编辑服务地址: `http://your-server-ip:8001`
5. 点击"保存"

### 验证 OnlyOffice

1. 在 Nextcloud 中上传或创建一个文档（.docx、.xlsx、.pptx）
2. 右键点击文档选择"在 ONLYOFFICE 中打开"
3. 应该能在 ONLYOFFICE 界面中编辑文档

