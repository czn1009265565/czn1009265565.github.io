# Airflow
Airflow是一个可编程，调度和监控的工作流平台，基于有向无环图(DAG)，airflow可以定义一组有依赖的任务，按照依赖依次执行。
airflow提供了丰富的命令行工具用于系统管控，而其web管理界面同样也可以方便的管控调度任务，并且对任务运行状态进行实时监控，方便了系统的运维和管理。

## 安装部署

### 虚拟环境
安装依赖  
```shell
pip install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple
```

创建虚拟环境  
```shell
virtualenv airflow
```

激活虚拟环境  
- Linux: `source airflow/bin/activate`
- Windows: `airflow\Scripts\activate`

### 安装基础包

```shell
export AIRFLOW_HOME = ~/airflow
pip install apache-airflow
```

### 扩展包

| 包名           | 	安装命令                                     | 	说明                                                       |
|--------------|-------------------------------------------|-----------------------------------------------------------|
| all          | 	pip install apache-airflow[all]          | 	所有Airflow功能                                              |
| all_dbs      | 	pip install apache-airflow[all_dbs]      | 	所有集成的数据库                                                 |
| async        | 	pip install apache-airflow[async]	       | Gunicorn的异步worker classes                                 |
| devel        | 	pip install apache-airflow[devel]	       | 最小开发工具要求                                                  |
| devel_hadoop | 	pip install apache-airflow[devel_hadoop] | 	Airflow + Hadoop stack 的依赖                               |
| celery       | 	pip install apache-airflow[celery]	      | CeleryExecutor                                            |
| crypto	      | pip install apache-airflow[crypto]        | 	加密元数据db中的连接密码                                            |
| druid        | 	pip install apache-airflow[druid]	       | Druid.io 相关的 operators 和 hooks                            |
| gcp_api      | 	pip install apache-airflow[gcp_api]      | 	Google 云平台 hooks 和operators（使用google-api-python-client ） |
| jdbc	        | pip install apache-airflow[jdbc]	         | JDBC hooks 和 operators                                    |
| hdfs         | 	pip install apache-airflow[hdfs]	        | HDFS hooks 和 operators                                    |
| hive         | 	pip install apache-airflow[hive]	        | 所有Hive相关的 operators                                       |
| kerberos     | 	pip install apache-airflow[kerberos]     | 	Kerberos集成Kerberized Hadoop                              |
| ldap	        | pip install apache-airflow[ldap]	         | 用户的LDAP身份验证                                               |
| mssql        | 	pip install apache-airflow[mssql]	       | Microsoft SQL Server operators 和 hook，作为Airflow后端支持       |
| mysql        | 	pip install apache-airflow[mysql]        | 	MySQL operators 和 hook，支持作为Airflow后端。                    |
| password     | 	pip install apache-airflow[password]	    | 用户密码验证                                                    |
| postgres     | 	pip install apache-airflow[postgres]	    | Postgres operators 和 hook，作为Airflow后端支持                   |
| qds	         | pip install apache-airflow[qds]	          | 启用QDS（Qubole数据服务）支持                                       |
| rabbitmq	    | pip install apache-airflow[rabbitmq]	     | rabbitmq作为Celery后端支持                                      |
| s3           | 	pip install apache-airflow[s3]	          | S3KeySensor ， S3PrefixSensor                              |
| samba	       | pip install apache-airflow[samba]         | 	Hive2SambaOperator                                       |
| slack	       | pip install apache-airflow[slack]         | 	SlackAPIPostOperator                                     |
| vertica      | 	pip install apache-airflow[vertica]      | 	做为Airflow后端的 Vertica hook 支持                             |
| cloudant     | 	pip install apache-airflow[cloudant]	    | Cloudant hook                                             |
| redis	       | pip install apache-airflow[redis]	        | Redis hooks 和 sensors                                     |

### 初始化数据库
在运行任务之前，Airflow需要初始化数据库。默认数据库为SQLite，可自行修改。

```shell
airflow initdb
```

### 配置数据库
由于Airflow是使用优秀的SqlAlchemy库与其元数据进行交互而构建的，因此您可以使用任何SqlAlchemy所支持的数据库作为后端数据库。
推荐使用MySQL或Postgres。
