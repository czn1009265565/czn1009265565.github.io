## MySQL 安装部署

### MySQL安装
#### 更新yum源

```shell
sudo rpm -Uvh https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
```

#### yum方式安装

```shell
sudo yum -y install mysql-community-server --enablerepo=mysql80-community --nogpgcheck
```

查看MySQL版本

```shell
mysql -V
```

### MySQL配置

#### 启动MySQL服务
```shell
systemctl start mysqld
```
#### 设置MySQL服务开机自启动

```shell
systemctl enable mysqld
```

#### 获取初始密码
查看/var/log/mysqld.log文件，获取并记录root用户的初始密码

```shell
grep 'temporary password' /var/log/mysqld.log
```
#### 安全配置 
```shell
mysql_secure_installation
```

1. 重置root密码
2. 删除匿名用户
3. 禁止root远程登陆
4. 删除test库以及对test库的访问权限
5. 重新加载授权表

#### 创建远程连接用户
```
mysql> create user 'projectName'@'%' identified by 'password'; #创建数据库用户projectName,并授予远程连接权限。
mysql> grant all privileges on *.* to 'projectName'@'%'; #为projectName用户授权数据库所有权限。
mysql> flush privileges; #刷新权限。
```
#### 删除远程用户 

```
mysql> drop user 'projectName';
```