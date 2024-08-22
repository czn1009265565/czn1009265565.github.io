# DataX

DataX 是阿里巴巴开源的一个异构数据源离线同步工具，致力于实现包括关系型数据库(MySQL、Oracle等)
、HDFS、Hive、ODPS、HBase、FTP等各种异构数据源之间稳定高效的数据同步功能。

项目地址: https://github.com/alibaba/DataX

| 类型           | 数据源                       | Reader(读) | Writer(写) |
|--------------|---------------------------|:---------:|:---------:|
| RDBMS 关系型数据库 | MySQL                     |     √     |     √     |
|              | Oracle                    |     √     |     √     |
|              | OceanBase                 |     √     |     √     |
|              | SQLServer                 |     √     |     √     |
|              | PostgreSQL                |     √     |     √     |
|              | DRDS                      |     √     |     √     |
|              | Kingbase                  |     √     |     √     |
|              | 通用RDBMS(支持所有关系型数据库)       |     √     |     √     |
| 阿里云数仓数据存储    | ODPS                      |     √     |     √     |
|              | ADB                       |           |     √     |
|              | ADS                       |           |     √     |
|              | OSS                       |     √     |     √     |
|              | OCS                       |           |     √     |
|              | Hologres                  |           |     √     |
|              | AnalyticDB For PostgreSQL |           |     √     |
| 阿里云中间件       | datahub                   |     √     |     √     |
|              | SLS                       |     √     |     √     |
| 图数据库         | 阿里云 GDB                   |     √     |     √     |
|              | Neo4j                     |           |     √     |
| NoSQL数据存储    | OTS                       |     √     |     √     |
|              | Hbase0.94                 |     √     |     √     |
|              | Hbase1.1                  |     √     |     √     |
|              | Phoenix4.x                |     √     |     √     |
|              | Phoenix5.x                |     √     |     √     |
|              | MongoDB                   |     √     |     √     |
|              | Cassandra                 |     √     |     √     |
| 数仓数据存储       | StarRocks                 |     √     |     √     |
|              | ApacheDoris               |           |     √     |
|              | ClickHouse                |     √     |     √     |
|              | Databend                  |           |     √     |
|              | Hive                      |     √     |     √     |
|              | kudu                      |           |     √     |
|              | selectdb                  |           |     √     |
| 无结构化数据存储     | TxtFile                   |     √     |     √     |
|              | FTP                       |     √     |     √     |
|              | HDFS                      |     √     |     √     |
|              | Elasticsearch             |           |     √     |
| 时间序列数据库      | OpenTSDB                  |     √     |           |
|              | TSDB                      |     √     |     √     |
|              | TDengine                  |     √     |     √     |


## 安装部署

下载地址: http://datax-opensource.oss-cn-hangzhou.aliyuncs.com/datax.tar.gz

**解压安装**  
```shell
tar -zxvf datax.tar.gz -C /opt/module/
```

**自检**  
```shell
python /opt/module/datax/bin/datax.py /opt/module/datax/job/job.json
```

## DataX使用

DataX的使用十分简单，用户只需根据自己同步数据的数据源和目的地选择相应的Reader和Writer，
并将Reader和Writer的信息配置在一个json文件中，然后执行如下命令提交数据同步任务即可。

```shell
python bin/datax.py path/to/your/job.json
```

## 案例

### MySQL_TO_HDFS

```json
{
  "job": {
    "setting": {
      "speed": {
        "channel": 1
      }
    },
    "content": [
      {
        "reader": {
          "name": "mysqlreader",
          "parameter": {
            "username": "root",
            "password": "root",
            "column": [
              "id",
              "name"
            ],
            "splitPk": "id",
            "connection": [
              {
                "table": [
                  "table_name"
                ],
                "jdbcUrl": [
                  "jdbc:mysql://127.0.0.1:3306/database"
                ]
              }
            ]
          }
        },
        "writer": {
          "name": "hdfswriter",
          "parameter": {
            "defaultFS": "hdfs://hadoop101:port",
            "fileType": "text",
            "path": "/user/hive/warehouse/database.db/table_name",
            "fileName": "table_name",
            "writeMode": "append",
            "fieldDelimiter": "\t",
            "compress": "gzip",
            "column": [
              {
                "name": "id",
                "type": "bigint"
              },
              {
                "name": "name",
                "type": "string"
              }
            ]
          }
        }
      }
    ]
  }
}
```

Reader配置说明:

* **jdbcUrl**: JDBC连接信息
* **username**: 用户名
* **password**: 密码
* **table**: 表名
* **column**: 所配置的表中需要同步的列名集合
* **splitPk**  
    * 描述: MysqlReader进行数据抽取时，如果指定splitPk，表示用户希望使用splitPk代表的字段进行数据分片，DataX因此会启动并发任务进行数据同步，这样可以大大提供数据同步的效能。
      推荐splitPk用户使用表主键，因为表主键通常情况下比较均匀，因此切分出来的分片也不容易出现数据热点。 目前splitPk仅支持整形数据切分，`不支持浮点、字符串、日期等其他类型`。如果用户指定其他非支持类型，MysqlReader将报错！ 如果splitPk不填写，包括不提供splitPk或者splitPk值为空，DataX视作使用单通道同步该表数据。
* **where**: 筛选条件
* **querySql**: 自定义筛选SQL，querySql优先级大于table、column、where选项


Writer配置说明:

* **defaultFS**: Hadoop hdfs文件系统namenode节点地址，格式：hdfs://ip:port
* **fileType**: 目前只支持用户配置为"text"或"orc"
* **path**: 存储到Hadoop hdfs文件系统的路径信息，HdfsWriter会根据并发配置在Path目录下写入多个文件。为与hive表关联，请填写hive表在hdfs上的存储路径。例：Hive上设置的数据仓库的存储路径为：/user/hive/warehouse/ ，已建立数据库：test，表：hello；则对应的存储路径为：/user/hive/warehouse/test.db/hello
* **fileName**: HdfsWriter写入时的文件名，实际执行时会在该文件名后添加随机的后缀作为每个线程写入实际文件名
* **column**: 写入数据的字段，不支持对部分列写入。为与hive中表关联，需要指定表中所有字段名和字段类型
* **writeMode**  
    * 描述：hdfswriter写入前数据清理处理模式  
        * append，写入前不做任何处理，DataX hdfswriter直接使用filename写入，并保证文件名不冲突。
        * nonConflict，如果目录下有fileName前缀的文件，直接报错。
        * truncate，如果目录下有fileName前缀的文件，先删除后写入。
* **fieldDelimiter**: hdfswriter写入时的字段分隔符,**需要用户保证与创建的Hive表的字段分隔符一致，否则无法在Hive表中查到数据**
* **compress**: hdfs文件压缩类型，默认不填写意味着没有压缩。其中：text类型文件支持压缩类型有gzip、bzip2;orc类型文件支持的压缩类型有NONE、SNAPPY（需要用户安装SnappyCodec）。