# Superset

## 安装部署

1. 安装虚拟环境  
   ```shell
   pip install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
2. 创建虚拟环境并激活
   ```shell
   virtualenv superset
   # Linux
   source superset/bin/activate
   # Windows
   superset\Scripts\activate
   ```
3. 安装依赖包  
   ```shell
   pip install apache-superset -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
4. 初始化数据库
   ```shell
   # Linux
   export FLASK_APP=superset
   # Windows
   set FLASK_APP=superset
   superset db upgrade
   ```
   报错:
   ```shell
   # A Default SECRET_KEY was detected, please use superset_config.py to override it.
   # 解决
   # 在superset文件根目录下新建superset_config.py
   SECRET_KEY = 'password'
   ```
5. 创建管理员用户
   ```shell
   superset fab create-admin
   ```
6. 初始化Superset
   ```shell
   superset init
   ```
7. 配置语言，`superset_config.py`配置文件新增 `BABEL_DEFAULT_LOCALE = 'zh'`
8. 启动Superset
   ```shell
   superset run -p 8080 --with-threads --reload --debugger
   ```
9. 部署Superset  
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

## 对接数据源  

1. 安装驱动依赖 [不同数据源对应依赖](https://superset.apache.org/docs/databases/installing-database-drivers) 这里以PG为例 `pip install psycopg2`
2. 服务重启
3. 新增数据库 Settings => Database Connections => + Database 填写数据库连接信息
4. 创建数据集 Datasets => + Dataset 选择数据库下对应表
5. 创建图标 Charts => + Chart 配置数据集、图表类型和对应指标
6. 配置仪表盘 Dashboards => + Dashboard 规划并填充图表
7. 配置仪表盘自动刷新频率