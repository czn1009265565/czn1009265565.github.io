# Hadoop分布式部署

## 前置准备

1. JDK安装部署
2. 静态IP配置
3. 设置主机名
   ```shell
   vim /etc/hosts 
   192.168.1.101 hadoop101
   192.168.1.102 hadoop102
   192.168.1.103 hadoop103
   ```
4. 新增hadoop用户，并赋予sudo权限
   ```shell
   useradd hadoop
   passwd hadoop
   
   visudo
   # Scroll down to the end of the file and add the following line
   hadoop  ALL=(ALL) NOPASSWD:ALL
   ```
5. 配置免密登录(hadoop用户)
   ```shell
   # 生成公钥和私钥
   ssh-keygen -t rsa
   
   # hadoop101
   ssh-copy-id hadoop101
   ssh-copy-id hadoop102
   ssh-copy-id hadoop103
   sudo chmod 700 ~/.ssh
   sudo chmod 600 ~/.ssh/authorized_keys
   
   # hadoop102
   ssh-copy-id hadoop101
   ssh-copy-id hadoop102
   ssh-copy-id hadoop103
   sudo chmod 700 ~/.ssh
   sudo chmod 600 ~/.ssh/authorized_keys
   ```

## 部署规划

|      | hadoop101         | hadoop102                   | hadoop103                   |
|------|-------------------|-----------------------------|-----------------------------|
| HDFS | NameNode、DataNode | DataNode                    | SecondaryNameNode、DataNode	 |
| YARN | NodeManager       | ResourceManager、NodeManager | NodeManager                 |

## 安装Hadoop

```shell
sudo mkdir /opt/module/
# 修改/opt/module目录所有者和所属组
sudo chown hadoop:hadoop /opt/module

tar -zxvf hadoop-3.3.4.tar.gz -C /opt/module/
mv /opt/module/hadoop-3.3.4 /opt/module/hadoop

# 添加环境变量
sudo vim /etc/profile.d/hadoop_env.sh

# JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$PATH:$JAVA_HOME/bin
#HADOOP_HOME
export HADOOP_HOME=/opt/module/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin

source /etc/profile.d/hadoop_env.sh
```

## 集群配置

```shell
cd $HADOOP_HOME/etc/hadoop
```

### 核心配置文件
```shell
vim core-site.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
   <!-- 指定NameNode的地址 -->
   <property>
      <name>fs.defaultFS</name>
      <value>hdfs://hadoop101:8020</value>
   </property>
   <!-- 指定hadoop数据的存储目录 -->
   <property>
      <name>hadoop.tmp.dir</name>
      <value>/opt/module/hadoop/data</value>
   </property>

   <!-- 配置HDFS网页登录使用的静态用户为hadoop -->
   <property>
      <name>hadoop.http.staticuser.user</name>
      <value>hadoop</value>
   </property>

   <!-- 配置该atguigu(superUser)允许通过代理访问的主机节点 -->
   <property>
      <name>hadoop.proxyuser.hadoop.hosts</name>
      <value>*</value>
   </property>
   <!-- 配置该atguigu(superUser)允许通过代理用户所属组 -->
   <property>
      <name>hadoop.proxyuser.hadoop.groups</name>
      <value>*</value>
   </property>
   <!-- 配置该hadoop(superUser)允许通过代理的用户-->
   <property>
      <name>hadoop.proxyuser.hadoop.users</name>
      <value>*</value>
   </property>
</configuration>
```

### HDFS配置文件

```shell
vim hdfs-site.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
   <!-- nn web端访问地址-->
   <property>
      <name>dfs.namenode.http-address</name>
      <value>hadoop101:9870</value>
   </property>

   <!-- 2nn web端访问地址-->
   <property>
      <name>dfs.namenode.secondary.http-address</name>
      <value>hadoop103:9868</value>
   </property>

   <!-- 测试环境指定HDFS副本的数量1 -->
   <property>
      <name>dfs.replication</name>
      <value>1</value>
   </property>
</configuration>
```

### YARN配置文件

```shell
vim yarn-site.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
    <!-- 指定MR走shuffle -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>

    <!-- 指定ResourceManager的地址-->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop102</value>
    </property>

    <!-- 环境变量的继承 -->
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>
            JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME
        </value>
    </property>

    <!--yarn单个容器允许分配的最大最小内存 -->
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>512</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>4096</value>
    </property>

    <!-- yarn容器允许管理的物理内存大小 -->
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>4096</value>
    </property>

    <!-- 关闭yarn对物理内存和虚拟内存的限制检查 -->
    <property>
        <name>yarn.nodemanager.pmem-check-enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.nodemanager.vmem-check-enabled</name>
        <value>false</value>
    </property>
</configuration>
```

### MapReduce配置文件
```shell
vim mapred-site.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration>
   <!-- 指定MapReduce程序运行在Yarn上 -->
   <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
   </property>
</configuration>
```

### 配置workers

```shell
vim /opt/module/hadoop/etc/hadoop/workers
```

```shell
hadoop101
hadoop102
hadoop103
```

### 配置历史服务器

```shell
vim mapred-site.xml
```
新增如下配置项
```xml
<!-- 历史服务器端地址 -->
<property>
    <name>mapreduce.jobhistory.address</name>
    <value>hadoop101:10020</value>
</property>

<!-- 历史服务器web端地址 -->
<property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>hadoop101:19888</value>
</property>
```

### 配置日志聚集

```shell
vim yarn-site.xml
```
新增如下配置项
```xml
<!-- 开启日志聚集功能 -->
<property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
</property>

<!-- 设置日志聚集服务器地址 -->
<property>  
    <name>yarn.log.server.url</name>  
    <value>http://hadoop101:19888/jobhistory/logs</value>
</property>

<!-- 设置日志保留时间为7天 -->
<property>
    <name>yarn.log-aggregation.retain-seconds</name>
    <value>604800</value>
</property>
```

### 分发配置

```shell
scp -r /opt/module/hadoop hadoop@hadoop102:/opt/module/hadoop
scp -r /opt/module/hadoop hadoop@hadoop103:/opt/module/hadoop
```

## 群起集群

如果集群是第一次启动，需要在hadoop101节点格式化NameNode

```shell
cd /opt/module/hadoop/
bin/hdfs namenode -format
```

**启动集群**  
```shell
# 在hadoop101启动hdfs
sbin/start-dfs.sh
# 在hadoop102启动yarn
sbin/start-yarn.sh
```

**关闭集群**
```shell
# 在hadoop101关闭hdfs
sbin/stop-dfs.sh
# 在hadoop102关闭yarn
sbin/stop-yarn.sh
```

**查看进程**  
```shell
--------- hadoop101 ----------
3074 Jps
2116 NameNode
2245 DataNode
2590 NodeManager
--------- hadoop102 ----------
3270 NodeManager
2952 DataNode
3148 ResourceManager
3854 Jps
--------- hadoop103 ----------
1889 DataNode
2100 NodeManager
2446 Jps
1967 SecondaryNameNode
```
