# Superset
Apache Superset是一个现代的数据探索和可视化平台。它功能强大且十分易用，可对接各种数据源，包括很多现代的大数据分析引擎，
拥有丰富的图表展示形式，并且支持自定义仪表盘。

## 安装部署

### 前置准备
1. 安装Miniconda
   ```shell
   # 创建虚拟环境
   conda create --name superset python=3.10
   ```
2. 依赖安装
   ```shell
   yum install -y gcc gcc-c++ libffi-devel python-devel python-pip python-wheel python-setuptools openssl-devel cyrus-sasl-devel openldap-devel
   ```
3. 升级pip  
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
   mysql> create user superset@'%' identified WITH mysql_native_password BY 'password';
   mysql> grant all privileges on *.* to superset@'%' with grant option;
   mysql> flush privileges;
   ```

3. 修改配置文件
   ```shell
   # 这里使用miniconda作为python环境管理
   vim ./miniconda3/envs/superset/lib/python3.10/site-packages/superset/config.py
   
   # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATA_DIR, "superset.db")
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@hostname:port/superset'
   
   # 生成 SECRET_KEY
   openssl rand -base64 42
   # 配置 SECRET_KEY
   SECRET_KEY = 'QDj/23oRQc9uzIKxomTZ85BHbtusTZ9OX0OAfIHRS8yMPIu0IdgS1GiC'
   ```

4. 安装mysql驱动
   ```shell
   # 这里选择兼容性更好的pymysql
   pip install pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
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
   superset run -p 8888 --with-threads --reload --debugger
   ```
4. 部署Superset  
   `gunicorn` 是一个 `Python Web Server`，类似 `Tomcat`  
   ```shell
   # 安装gunicorn
   pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
   # 启动服务
   gunicorn --workers 5 --timeout 120 --bind 192.168.1.101:8888  "superset.app:create_app()" --daemon
   ```
   - --workers：指定进程个数
   - --timeout：worker 进程超时时间，超时会自动重启
   - --bind：绑定本机地址，即为 Superset 访问地址
   - --daemon：后台运行
5. 关闭服务  
   ```shell
   # ‌寻找master PID
   pstree -ap|grep gunicorn
   
   kill -9 <Master PID>
   ```