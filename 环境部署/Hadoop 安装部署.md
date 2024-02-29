# Hadoop 安装部署
本文介绍hadoop-3.2.0的伪分布式部署

## 前置环境

1. 安装JDK
2. 静态IP配置 (ZeroTier无需配置)
3. 设置hostname `vim /etc/hosts` 追加`172.30.255.100 hadoop100`
4. 免密登录

```shell
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

## 伪分布式部署
### 解压缩安装包

```shell
tar -zxvf hadoop-3.2.0.tar.gz
mv hadoop-3.2.0 /usr/local/hadoop
```

### 配置环境变量

```shell
vim /etc/profile

export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

source /etc/profile
```
### 核心配置文件

配置`hadoop-env.sh`,文件路径:`/usr/local/hadoop/etc/hadoop/hadoop-env.sh`

```shell
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export HADOOP_LOG_DIR=/data/hadoop_repo/logs/hadoop
```

配置`core-site.xml`,文件路径:`/usr/local/hadoop/etc/hadoop/core-site.xml`

```xml
<configuration>
	<property>
		<name>fs.defaultFS</name>
		<value>hdfs://hadoop100:9000</value>
	</property>
	<property>
		<name>hadoop.tmp.dir</name>
		<value>/data/hadoop_repo</value>
	</property>
</configuration>
```

配置`hdfs-site.xml`,文件路径:`/usr/local/hadoop/etc/hadoop/hdfs-site.xml`

```xml
<configuration>
	<property>
        <!-- 设置 hdfs 副本数 -->
		<name>dfs.replication</name>
		<value>1</value>
	</property>
</configuration>
```

配置`mapred-site.xml`,文件路径:`/usr/local/hadoop/etc/hadoop/mapred-site.xml`

```xml
<configuration>
	<property>
        <!-- 设置 mapreduce 使用的资源调度框架 -->
		<name>mapreduce.framework.name</name>
		<value>yarn</value>
	</property>
</configuration>
```
配置`yarn-site.xml`,文件路径:`/usr/local/hadoop/etc/hadoop/yarn-site.xml`

```xml
<configuration>
    <!-- 设置 yarn 上支持运行的服务和环境变量白名单 --> 
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
	<property>
		<name>yarn.nodemanager.env-whitelist</name>
		<value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CL
			ASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
	</property>
</configuration>
```

### 格式化namenode

```shell
# 仅第一次启动需要格式化
hdfs namenode -format
```

看到`/data/hadoop_repo/dfs/name has been successfully formatted. `则代表格式化成功

### 启动hadoop集群
`start-all.sh` 启动失败, 修改sbin目录下的脚本配置

```shell
vim start-dfs.sh
# 在文件开头新增配置项
HDFS_DATANODE_USER=root
HDFS_DATANODE_SECURE_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root

vim stop-dfs.sh
# 在文件开头新增配置项
HDFS_DATANODE_USER=root
HDFS_DATANODE_SECURE_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root

vim start-yarn.sh
# 在文件开头新增配置项
YARN_RESOURCEMANAGER_USER=root
HADOOP_SECURE_DN_USER=yarn
YARN_NODEMANAGER_USER=root

vim stop-yarn.sh
# 在文件开头新增配置项
YARN_RESOURCEMANAGER_USER=root
HADOOP_SECURE_DN_USER=yarn
YARN_NODEMANAGER_USER=root
```

### 验证

```shell
jps

6248 DataNode
6491 SecondaryNameNode
6109 NameNode
6749 ResourceManager
7261 Jps
6895 NodeManager

hdfs webui 界面: http://172.30.255.100:9870
yarn webui 界面: http://172.30.255.100:8088
```
### 停止集群

```shell
stop-all.sh
```
