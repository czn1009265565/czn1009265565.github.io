## Hbase 集群搭建
HBase 的版本必须要与 Hadoop 的版本兼容

||HBase-1.7.x|HBase-2.3.x|HBase-2.4.x|
|---|---|---|---|
|Hadoop-2.10.x|√|√|√|
|Hadoop-3.1.0|x|x|x|
|Hadoop-3.1.1+|x|√|√|
|Hadoop-3.2.x|x|√|√|
|Hadoop-3.3.x|x|√|√|


本文安装Hbase-2.4.10

### 伪分布式安装

1. 解压
	```
	$ tar -zxvf hbase-2.4.10-bin.tar.gz
	$ mv hbase-2.4.10-bin /usr/local/hbase
	```
2. 添加环境变量
	```
	$ vim /etc/profile

	export HBASE_HOME=/usr/local/hbase
	export PATH=$HBASE_HOME/bin:$PATH

	$ source /etc/profile
	```
3. 配置文件 `conf/hbase-env.sh`,指定 JDK 的安装路径
	
	```
	export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
	```
4. 配置文件 `conf/hbase-site.xml`，增加如下配置 (hadoop001 为主机名)
	```
	<configuration>
	 <!--指定 HBase 以分布式模式运行-->   
	 <property>
	    <name>hbase.cluster.distributed</name>
	    <value>true</value>
	 </property>
	 <!--指定 HBase 数据存储路径为 HDFS 上的 hbase 目录,hbase 目录不需要预先创建，程序会自动创建-->   
	 <property>
	    <name>hbase.rootdir</name>
	    <value>hdfs://hadoop001:8020/hbase</value>
	  </property>
	    <!--指定 zookeeper 数据的存储位置-->   
	  <property>
	    <name>hbase.zookeeper.property.dataDir</name>
	    <value>/home/zookeeper/dataDir</value>
	  </property>
	</configuration>
	```
4. 配置文件 `conf/regionservers`，指定 region servers 的地址，修改后其内容如下
	```
	hadoop001
	```
5. 启动
	```
	# bin/start-hbase.sh
	```
6. 验证
	
	jps 命令查看进程。其中 HMaster，HRegionServer 是 HBase 的进程,HQuorumPeer 是 HBase 内置的 Zookeeper 的进程