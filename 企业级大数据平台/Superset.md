# Superset

## PyPI 安装部署

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
   superset db upgrade
   ```
   报错一:
   ```shell
   # Error: Could not locate a Flask application.
   # 解决
   # Linux
   export FLASK_APP=superset
   # Windows
   set FLASK_APP=superset
   ```
   报错二:
   ```shell
   # A Default SECRET_KEY was detected, please use superset_config.py to override it.
   # 解决
   # 在superset文件根目录下新建superset_config.py
   SECRET_KEY = 'password'
   # Linux
   export SUPERSET_CONFIG_PATH=./superset/superset_config.py
   # Windows
   set set SUPERSET_CONFIG_PATH=.\superset\superset_config.py
   ```
5. 创建管理员用户
   ```shell
   export FLASK_APP=superset
   superset fab create-admin
   ```
6. 初始化Superset
   ```shell
   superset init
   ```
7. 启动Superset
   ```shell
   superset run -p 8088 --with-threads --reload --debugger
   ```