## Sqoop 安装部署
Sqoop 是一个常用的数据迁移工具，主要用于在不同存储系统之间实现数据的导入与导出：

1. 导入数据：从 MySQL，Oracle 等关系型数据库中导入数据到 HDFS、Hive、HBase 等分布式文件存储系统中；
2. 导出数据：从 分布式文件系统中导出数据到关系数据库中。

其原理是将执行命令转化成 MapReduce 作业来实现数据的迁移

1. 下载并解压 
    ```
    $ tar -zxvf sqoop-release-1.4.7-rc0.tar.gz
    $ mv sqoop-release-1.4.7-rc0 /usr/local/sqoop
    ```
2. 配置环境变量
    ```markdown
    # vim /etc/profile
    
    export SQOOP_HOME=/usr/local/sqoop
    export PATH=$SQOOP_HOME/bin:$PATH
   
    # source /etc/profile
    ```
3. 修改配置
    
    其中HADOOP_COMMON_HOME、HADOOP_MAPRED_HOME为必选,其余为可选
    ```markdown
    #Set path to where bin/hadoop is available
    export HADOOP_COMMON_HOME=/usr/local/hadoop
    
    #Set path to where hadoop-*-core.jar is available
    export HADOOP_MAPRED_HOME=/usr/local/hadoop
    
    #set the path to where bin/hbase is available
    export HBASE_HOME=/usr/local/hbase
    
    #Set the path to where bin/hive is available
    export HIVE_HOME=/usr/local/hive
    
    #Set the path for where zookeper config dir is
    export ZOOCFGDIR=/usr/local/zookeeper/conf
    ```
7. 拷贝数据库驱动至`/usr/local/sqoop/lib`
8. 验证 `sqoop version`