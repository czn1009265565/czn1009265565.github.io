# Superset
Apache Superset是一个现代的数据探索和可视化平台。它功能强大且十分易用，可对接各种数据源，包括很多现代的大数据分析引擎，
拥有丰富的图表展示形式，并且支持自定义仪表盘。

## 安装部署

### 前置准备

**依赖安装**  
```shell
yum install -y gcc gcc-c++ libffi-devel python-devel python-pip python-wheel python-setuptools openssl-devel cyrus-sasl-devel openldap-devel
```

**升级pip**  
```shell
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 安装依赖包
```shell
pip install apache-superset -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 配置元数据库
1. 新建数据库
   ```shell
   mysql> CREATE DATABASE superset DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
   ```

2. 创建superset用户
   ```shell
   mysql> create user superset@'%' identified WITH mysql_native_password BY 'superset';
   mysql> grant all privileges on *.* to superset@'%' with grant option;
   mysql> flush privileges;
   ```

3. 修改配置文件
   ```shell
   # 这里使用miniconda作为python环境管理
   vim /opt/module/miniconda/envs/superset/lib/python3.8/site-packages/superset/config.py
   
   # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATA_DIR, "superset.db")
   SQLALCHEMY_DATABASE_URI = 'mysql://superset:superset@localhost:3306/superset?charset=utf8'
   ```

4. 安装mysql驱动
   ```shell
   pip install mysqlclient -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

5. 初始化Superset元数据
   ```shell
   export FLASK_APP=superset
   superset db upgrade
   ```

### 初始化Superset

1. 创建管理员用户  
   ```shell
   superset fab create-admin
   ```
2. 初始化数据  
   ```shell
   superset init
   ```
3. 启动Superset
   ```shell
   superset run -p 8080 --with-threads --reload --debugger
   ```
4. 部署Superset  
   `gunicorn` 是一个 `Python Web Server`，类似 `Tomcat`  
   ```shell
   # 安装gunicorn
   pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
   # 启动服务
   gunicorn --workers 5 --timeout 120 --bind localhost:8080  "superset.app:create_app()" --daemon
   ```
   - --workers：指定进程个数
   - --timeout：worker 进程超时时间，超时会自动重启
   - --bind：绑定本机地址，即为 Superset 访问地址
   - --daemon：后台运行