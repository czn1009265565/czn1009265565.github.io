## Hive 安装部署
本文介绍apache-hive-3.1.2的安装部署

### 前置环境

1. Hadoop 安装部署

### 下载安装包

下载地址: `https://dist.apache.org/repos/dist/release/hive/`

```shell
tar -zxvf apache-hive-3.1.2-bin.tar.gz
mv apache-hive-3.1.2-bin /usr/local/hive
```

### 添加环境变量
```shell
vim /etc/profile

export HIVE_HOME=/usr/local/hive
export PATH=$PATH:$HIVE_HOME/bin

source /etc/profile
```
### Hive环境配置

```shell
cd /usr/local/hive/conf/
cp hive-env.sh.template hive-env.sh
vim hive-env.sh

export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export HIVE_HOME=/usr/local/hive
export HADOOP_HOME=/usr/local/hadoop
```

### 配置元数据数据库 (这里采用MySQL)

```shell
cp hive-default.xml.template hive-site.xml
vim hive-site.xml
```

修改对应的属性
```xml
<property>
	<name>javax.jdo.option.ConnectionURL</name>
	<value>jdbc:mysql://127.0.0.1:3306/hive?serverTimezone=Asia/Shanghai</value>
</property>
<property>
	<name>javax.jdo.option.ConnectionDriverName</name>
	<value>com.mysql.cj.jdbc.Driver</value>
</property>
<property>
	<name>javax.jdo.option.ConnectionUserName</name>
	<value>root</value>
</property>
<property>
	<name>javax.jdo.option.ConnectionPassword</name>
	<value>root</value>
</property>
<property>
	<name>hive.querylog.location</name>
	<value>/data/hive_repo/querylog</value>
</property>
<property>
	<name>hive.exec.local.scratchdir</name>
	<value>/data/hive_repo/scratchdir</value>
</property>
<property>
	<name>hive.downloaded.resources.dir</name>
	<value>/data/hive_repo/resources</value>
</property>
```

### 添加MySQL驱动

添加MySQL的驱动程序到hive/lib下 `mysql-connector-java-8.0.26.jar`

### 配置 Hadoop `core-site.xml`
   
```xml
<!-- 配置hadoop的代理用户，主要是用于让hiveserver2客户端访问及操作hadoop文件具备权限 -->
<property>
    <name>hadoop.proxyuser.root.hosts</name>
    <value>*</value>
</property>

<!-- 配置hadoop的代理用户组，主要是用于让hiveserver2客户端访问及操作hadoop文件具备权限 -->
<property>
    <name>hadoop.proxyuser.root.groups</name>
    <value>*</value>
</property>
```

### 初始化元数据 

`schematool -dbType mysql -initSchema`

发现报错，删除如下配置即可

```xml
<property>
    <name>hive.txn.xlock.iow</name>
    <value>true</value>
    <description>
      Ensures commands with OVERWRITE (such as INSERT OVERWRITE) acquire Exclusive locks for&#8;transactional tables.  This ensures that inserts (w/o overwrite) running concurrently
      are not hidden by the INSERT OVERWRITE.
    </description>
  </property>
```

### 启动Hive

```shell
# 执行hive 客户端
hive

# 启动 hiveserver2
nohup hiveserver2 &

# 使用beeline
beeline -u jdbc:hive2://hadoop001:10000 -n root
```