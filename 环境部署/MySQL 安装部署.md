# MySQL 安装部署

### 更新yum源
添加MySQL官方的Yum仓库

```shell
# MySQL5.7
sudo rpm -Uvh https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
# MySQL8.0
sudo rpm -Uvh https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
```

### yum方式安装

```shell
# MySQL5.7
sudo yum -y install mysql-community-server --enablerepo=mysql57-community --nogpgcheck
# MySQL8.0
sudo yum -y install mysql-community-server --enablerepo=mysql80-community --nogpgcheck
```

### 启动MySQL服务
```shell
systemctl start mysqld
```

### 设置MySQL服务开机自启动

```shell
systemctl enable mysqld
```

### 获取初始密码
查看/var/log/mysqld.log文件，获取并记录root用户的初始密码

```shell
grep 'temporary password' /var/log/mysqld.log
```
### 安全配置 
```shell
mysql_secure_installation
```

1. 重置root密码
2. 删除匿名用户
3. 禁止root远程登陆
4. 删除test库以及对test库的访问权限
5. 重新加载授权表

### 创建远程连接用户

```shell
# 创建数据库用户,并授予远程连接权限
mysql> create user 'username'@'%' identified by 'password';
# 为用户授权数据库所有权限
mysql> grant all privileges on *.* to 'username'@'%';
# 刷新权限
mysql> flush privileges;
```

### 删除用户

```shell
# 删除用户 
mysql> drop user 'username'; 
```