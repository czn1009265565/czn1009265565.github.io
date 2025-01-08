## Flask

### 安装依赖

```shell
# 虚拟环境
pip install virtualenv
# Flask
pip install Flask
# 数据库ORM框架
pip install flask-sqlalchemy
pip install pymysql
# 用户身份验证
pip install Flask-Login
# 表单
pip install flask_wtf
# 加解密
pip install Werkzeug
# 部署
pip install gunicorn
```


### 应用示例

```python
from flask import Flask

# 初始化
app = Flask(__name__)


# 路由和视图
@app.route('/')
def index():
    return '<h1>Hello World!<h1>'
```

#### Linux 和 macOS 用户执行下述命令启动 Web 服务器
```python
export FLASK_APP=hello.py
flask run
```

#### Windows 用户 用户执行下述命令启动 Web 服务器
```python
set FLASK_APP=hello.py
flask run
```

#### Debug模式启动
```python
if "__main__" == __name__:
    app.run()
```

#### 命令行选项

```python
flask run -h 0.0.0.0 -p 8080
```

### 动态路由

```python
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!<h1>'.format(name)
```

### 请求对象

```python
from flask import request

@app.route('/user/create', methods=['POST'])
def create():
    user = request.get_json()
    username = user.get('username')
    return 'success'
```

请求对象

| 属性或方法      | 说明                |
|------------|-------------------|
| form       | 字典，存储表单字段         |
| args       | 字典，URL查询参数        |
| cookies    | 字典，存储所有的cookie    |
| headers    | 字典，存储所有的请求头       |
| files      | 字典，存储所有上传的文件      |
| get_data() | 返回请求主体            |
| get_json() | 返回请求主体解析后的JSON字典  |
| method     | HTTP请求方法，GET或POST |

### 响应对象

```python
from flask import make_response

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('sessionId', '10001')
    return response
```
| 属性或方法           | 说明           |
|-----------------|--------------|
| status_code     | HTTP 数字状态码   |
| set_cookie()    | 添加一个cookie   |
| delete_cookie() | 删除一个cookie   |
| set_data()      | 使用字符串或字节设置响应 |
| get_data()      | 获取响应主体       |
| content_type    | 响应主体的媒体类型    |
| content_length  | 响应主体的长度      |


### 模板
#### 变量
user.html
```html
<h1>Hello {{name}}!</h1>
```

模板渲染

```python
from flask import render_template

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

####  控制结构

```html
<h1>
{% if name %}
    Hello, {{ name }}!
{% else %}
    Hello, Stranger!
{% endif %}
</h1>

<ul>
    {% for comment in comment_list %}
    <li>{{ comment }}</li>
    {% endfor %}
<ul>
```

```python
@app.route('/user/<name>')
def user(name):
    comment_list = ["a", "b", "c"]
    return render_template('user.html', name=name, comment_list=comment_list)
```

#### 模板继承
定义基模板 base.html


渲染模板

```python
@app.route('/')
def index():
    return render_template("derive.html")
```

### 数据库
SQLAlchemy 是一个强大的关系型数据库框架，支持多种数据库后台。SQLAlchemy 提供了高层 ORM，也提供了使用数据库原生 SQL 的低层功能。


配置数据库
```python
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

模型定义
```python
from werkzeug.security import check_password_hash

from .. import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)

    def verify_password(self, password):
        """密码验证"""
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
```

最常用的SQLAlchemy列类型

| 类型名          | Python类型          |
|--------------|-------------------|
| Integer      | int               |
| SmallInteger | int               |
| BigInteger   | int或long          |
| Float        | float             |
| Numeric      | decimal.Decimal   |
| String       | str               |
| Text         | str               |
| Boolean      | bool              |
| Date         | datetime.date     |
| Time         | datetime.time     |
| DateTime     | datetime.datetime |

创建、删除表
```
flask shell
>>> from hello import db
>>> db.create_all()
>>> db.drop_all()
```

增删改查
```python
flask shell
>>> from hello import db,User

# 新增
db.session.add(User(id="10001", username="Tom", age=18))
# 批量新增
db.session.add_all([
    User(id="10002", username="Kim", age=19),
    User(id="10003", username="Bob", age=20)
])
db.session.commit()

# 删除
user = User.query.get(10001)
db.session.delete(user)
db.session.commit()

# 更新需要先查询后修改
user = User.query.get(10002)
user.age = 21
db.session.add(user)
db.session.commit()
    
# 查询所有用户数据
User.query.all()
# 查询有多少个用户
User.query.count()
# 查询第1个用户
User.query.first()
# 根据主键ID查询
User.query.get(10001)
# 过滤查询
User.query.filter_by(username="Kim").all()
```


### 日志记录

```python
import logging
from flask import Flask
 
app = Flask(__name__)

# 配置日志记录器，日志级别为DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 配置日志处理器
handler = logging.FileHandler('flasky.log')
handler.setLevel(logging.DEBUG)

# 配置日志格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 添加日志处理器到日志记录器
logger.addHandler(handler)

@app.route("/user/<int:id>")
def user_detail(id):
    user = User.query.get(id)
    # 日志打印
    logger.info("user: %s", user)
    return render_template('user.html', user=user)
```


### 项目结构
不同于多数其他的 Web 框架，Flask 并不强制要求大型项目使用特定的组织方式，应用结构的组织方式完全由开发者决定。

```
|-flasky
  |-app/
    |-static/
    |-templates/
    |-po/
      |-__init__.py
      |-models.py
      |-forms.py
    |-web/
      |-__init__.py
      |-views.py
    |-api/
      |-__init__.py
      |-views.py
    |-__init__.py
  |-venv/
  |-requirements.txt
  |-config.py
  |-flasky.py
```

#### 配置文件 config.py

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'admin'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://username:password@localhost/dbname'
    DEBUG = True
```

#### 应用包构造文件 /app/__init__.py 

```python
import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

# 配置日志记录器，日志级别为INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('flasky.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 初始化服务
app = Flask(__name__)

# 初始化数据库连接
app.config.from_object(Config)
db = SQLAlchemy(app)

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'web.login'
login_manager.init_app(app)

# 注册蓝图
from .api import api
from .web import web

app.register_blueprint(web)
app.register_blueprint(api, url_prefix='/api')
```

#### /app/web/__init__.py
随着Flask项目越来越复杂，把所有视图函数放在一个应用文件中会很不方便我们管理，所以需要对程序进行模块化的处理。Flask内置了一个模块化处理的类——Blueprint蓝图。

Blueprint 是一种组织一组相关视图及其他代码的方式。与把视图及其他代码直接注册到app的方式不同，蓝图方式是先把它们注册到蓝图，然后在工厂函数中把蓝图注册到app。

```python
from flask import Blueprint

web = Blueprint('web', __name__)

from . import views
```

#### /app/api/__init__.py

```python
from flask import Blueprint

api = Blueprint('api', __name__)

from . import views
```

#### 应用主脚本 flasky.py

```python
from app import app


if "__main__" == __name__:
    app.run()
```

### 用户认证
用户登录应用后，他们的验证状态要记录在用户会话中，这样浏览不同的页面时才能记住这个状态。
Flask-Login 是个非常有用的小型扩展，专门用于管理用户身份验证系统中的验证状态，且不依赖特定的身份验证机制。
#### 登录流程:
1. 登录：用户提供登录凭证（如用户名和密码）提交给服务器
2. 建立会话：服务器验证用户提供的凭证，如果通过验证，则建立会话（ Session ），并返回给用户一个会话号（ Session id ）
3. 验证：用户在后续的交互中提供会话号，服务器将根据会话号（ Session id ）确定用户是否有效
4. 登出：当用户不再与服务器交互时，注销与服务器建立的会话

#### 初始化Flask-Login

```python
# 初始化服务
app = Flask(__name__)

# 初始化数据库连接
app.config.from_object(Config)
db = SQLAlchemy(app)

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'web.login'
login_manager.init_app(app)
```
其中 `LoginManager` 对象的 `login_view` 属性用于设置登录页面的视图函数

#### User模型 /app/po/models.py

要想使用 Flask-Login 扩展，应用的 User 模型必须实现几个属性和方法,或者直接继承 `UserMixin` 类，其中包含默认实现.
```python
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from .. import db
from .. import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)

    def verify_password(self, password):
        """密码验证"""
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
```
`user_loader` 的作用是根据 `Session` 信息加载登录用户，它根据用户 `ID`，返回一个用户实例

#### 登录表单 /app/po/forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
```

#### 登录视图 /app/web/views.py

```python
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import login_user
from flask_login import current_user
from flask_login import login_required

from ..po.models import User
from ..po.forms import LoginForm
from . import web


@web.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    msg = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            msg = "用户名或密码密码有误"
        else:
            if user.verify_password(password):
                # 创建用户 Session
                login_user(user)
                return redirect(url_for('web.index'))
            else:
                msg = "用户名或密码密码有误"
    return render_template('login.html', form=form, msg=msg)
```

#### 模板页面
login.html


index.html  


#### 保护视图

```python
@web.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.username)
```

### 部署
在应用启动过程中，Flask 会创建一个 Python 的 logging.Logger 类实例，并将其附属到应用实例上，通过 `app.logger` 访问。


`Flask` 自带的 `Web` 开发服务器不适合在这种情况下使用，因为它不是为生产环境设计的服务器。
有两个 `Web` 服务器适合在生产环境中使用，而且支持 `Flask` 应用，它们是 `Gunicorn` 和 `uWSGI`。

boot.sh
```shell
#!/bin/sh
source venv/bin/activate
flask deploy
exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - flasky:app
```

Dockerfile 容器映像构建脚本
```shell
FROM python:3.6-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG docker

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# 运行时配置
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
```

docker-compose.yml
```yml
version: '3'
services:
  flasky:
    build: .
    ports:
      - "8000:5000"
    env_file: .env
    restart: always
    links:
      - mysql:dbserver
    depends_on:
      - mysql
  mysql:
    image: "mysql/mysql-server:5.7"
    env_file: .env-mysql
    restart: always
```

.env
```
FLASK_APP=flasky.py
FLASK_CONFIG=docker
SECRET_KEY=3128b4588e7f4305b5501025c13ceca5
MAIL_USERNAME=<your-gmail-username>
MAIL_PASSWORD=<your-gmail-password>
DATABASE_URL=mysql+pymysql://flasky:<database-password>@dbserver/flasky
```

.env-mysql
```
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_DATABASE=flasky
MYSQL_USER=flasky
MYSQL_PASSWORD=<database-password>
```