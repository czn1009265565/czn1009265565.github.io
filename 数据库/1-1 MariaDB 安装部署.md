# MariaDB 安装部署

MariaDB 是一个开源的关系型数据库管理系统（RDBMS），是 MySQL 的一个分支。
它由 MySQL 的原始开发者创建，旨在保持与 MySQL 的高度兼容性，同时提供更好的性能、更多的功能和完全的开源承诺。

## Windows

1. 下载地址 `https://downloads.mariadb.org/`
2. 版本选择  
   - 最新稳定版: `MariaDB 10.11.x`
   - 长期支持版: `MariaDB 10.6.x`
3. 安装步骤
```mermaid
graph TD
    A[下载安装程序] --> B[运行安装向导]
    B --> C[接受许可证]
    C --> D[选择组件]
    D --> E[配置安装路径]
    E --> F[设置root密码]
    F --> G[配置服务]
    G --> H[完成安装]
```

## Ubuntu

1. 更新系统包索引
```shell
sudo apt update
sudo apt upgrade -y
```
2. 安装 MariaDB
```shell
# 安装 MariaDB 服务器
sudo apt install mariadb-server -y

# 安装 MariaDB 客户端（可选）
sudo apt install mariadb-client -y
```
3. 启动和启用 MariaDB 服务
```shell
# 启动服务
sudo systemctl start mariadb

# 设置开机自启
sudo systemctl enable mariadb

# 检查服务状态
sudo systemctl status mariadb
```
4. 运行安全配置脚本（重要）
```shell
sudo mysql_secure_installation
```
按提示完成以下安全设置

- 设置 root 密码
- 移除匿名用户
- 禁止 root 远程登录
- 移除测试数据库
- 重新加载权限表
5. 基本配置编辑 `sudo vim /etc/mysql/mariadb.conf.d/50-server.cnf`
```
[mysqld]
# 绑定地址（允许远程连接时改为 0.0.0.0）
bind-address = 127.0.0.1

# 字符集设置
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# 其他性能配置（根据服务器配置调整）
innodb_buffer_pool_size = 256M
max_connections = 100
```

## 用户管理

注意点: 数据库用户名的完整标识是 'username'@'host' 的组合，不同主机表示不同用户

### 创建用户

```mysql
-- 创建用户(允许远程连接)
CREATE USER 'username'@'%' IDENTIFIED BY 'password';

-- 创建用户(仅允许本地连接)
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';

-- 创建用户（允许特定 IP 连接）
CREATE USER 'username'@'192.168.1.100' IDENTIFIED BY 'password';
```

### 修改用户密码

```mysql
-- 修改用户密码
ALTER USER 'username'@'%' IDENTIFIED BY 'new_password';
```

### 修改用户授权

```mysql
-- 授予所有数据库的所有权限
GRANT ALL PRIVILEGES ON *.* TO 'username'@'%';

-- 授予特定数据库的所有权限
GRANT ALL PRIVILEGES ON `dbname`.* TO 'username'@'%';

-- 授予特定数据库的查询、插入、更新权限
GRANT SELECT, INSERT, UPDATE ON `dbname`.* TO 'username'@'%';

-- 授予特定表的权限
GRANT SELECT, INSERT ON `dbname`.`tablename` TO 'username'@'%';

-- 刷新权限
FLUSH PRIVILEGES;
```

### 删除用户

```mysql
DROP USER 'username'@'%';
DROP USER 'username'@'localhost';
```