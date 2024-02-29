## DataX 安装部署

DataX 是阿里巴巴集团内被广泛使用的离线数据同步工具/平台，实现包括 MySQL、SQL Server、Oracle、PostgreSQL、HDFS、Hive、HBase、OTS、ODPS 等各种异构数据源之间高效的数据同步功能。

### 前置环境

1. JDK(1.8以上，推荐1.8)
2. Python(2或3都可以)
3. Apache Maven 3.x (Compile DataX)

### 下载安装包

https://github.com/alibaba/DataX

```shell
tar -zxvf datax.tar.gz
mv datax /usr/local/datax

# 自检脚本
python /usr/local/datax/bin/datax.py /usr/local/datax/job/job.json
```


