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

### 初始化数据库
在运行任务之前，Airflow需要初始化数据库。默认数据库为SQLite，可自行修改。

```shell
airflow initdb
```
### 启动Web服务

```shell
airflow webserver -p 8080 -D
```

### 启动调度任务

```shell
airflow scheduler -D
```

### 配置数据库
由于Airflow是使用优秀的SqlAlchemy库与其元数据进行交互而构建的，因此您可以使用任何SqlAlchemy所支持的数据库作为后端数据库。
推荐使用MySQL或Postgres。

这里以MySQL为例
1. 创建数据库`CREATE DATABASE airflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
2. 修改airflow配置文件 `sql_alchemy_conn = mysql+mysqlconnector://root:password@localhost:3306/airflow_db`
3. 杀死并重启服务 `airflow webserver -p 8080 -D`

## 调度脚本

```shell
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    # 用户
    'owner': 'airflow',
    # 是否开启任务依赖
    'depends_on_past': True, 
    # 邮箱
    'email': ['1@1.com'],
    # 启动时间 (UTC时间)
    'start_date':datetime(2022,11,28),
    # 重试次数
    'retries': 1,
    # 重试时间间隔
    'retry_delay': timedelta(minutes=5),
}
# 声明任务图
dag = DAG('dag_id', default_args=default_args, schedule_interval=timedelta(days=1))
 
# 创建单个任务
t1 = BashOperator(
    # 任务id
    task_id='dwd',
    # 任务命令
    bash_command='ssh hadoop102 "/opt/module/spark-yarn/bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn /opt/module/spark-yarn/examples/jars/spark-examples_2.12-3.1.3.jar 10 "',
    # 重试次数
    retries=3,
    # 把任务添加进图中
    dag=dag)

t2 = BashOperator(
    task_id='dws',
    bash_command='ssh hadoop102 "/opt/module/spark-yarn/bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn /opt/module/spark-yarn/examples/jars/spark-examples_2.12-3.1.3.jar 10 "',
    retries=3,
    dag=dag)

t3 = BashOperator(
    task_id='ads',
    bash_command='ssh hadoop102 "/opt/module/spark-yarn/bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn /opt/module/spark-yarn/examples/jars/spark-examples_2.12-3.1.3.jar 10 "',
    retries=3,
    dag=dag)

# 设置任务依赖(不能出现环形链路)
t2.set_upstream(t1)
t3.set_upstream(t2)
```

airflow.cfg配置调度任务目录，放置调度脚本  
```
dags_folder=/home/app/airflow/dags
```