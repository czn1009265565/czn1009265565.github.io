# SqlAlchemy

SQLAlchemy 是 Python 最流行的 SQL 工具包/ORM 框架，支持几乎所有主流数据库，既可以用面向对象方式操作数据库，
也保留了原生SQL的灵活性，分为 SQLAlchemy Core（底层SQL抽象层）和 SQLAlchemy ORM（高层对象映射层）两部分，
日常开发以ORM用法为主。

## 环境安装

```shell
# 安装核心库
pip install sqlalchemy

# 安装对应数据库驱动（按需选装）
pip install pymysql          # MySQL 驱动
pip install psycopg2-binary  # PostgreSQL 驱动
```

连接字符串统一格式：数据库类型+驱动://用户名:密码@主机:端口/数据库名

## 核心概念

- Engine（引擎）	SQLAlchemy 与数据库通信的核心，管理连接池，负责底层连接的创建和释放
- Base（基类）	所有 ORM 模型的父类，所有表结构都继承它定义
- Session（会话）	ORM 操作数据库的入口，负责管理事务、执行查询、持久化对象
- Model（模型）	数据库表的Python对象映射，类属性对应表字段

## 基础实例

### 数据库连接配置

db.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 创建引擎 连接字符串格式: 数据库类型+驱动://用户名:密码@主机:端口/数据库名
engine = create_engine("mysql+pymysql://root:password@localhost:3306/dbname", echo=True)

# 2. 创建所有模型的基类
Base = declarative_base()

# 3. 创建会话工厂，生成操作数据库的会话对象
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    # 创建表
    Base.metadata.create_all(engine)
```

### 模型定义

user_model.py

```python
from sqlalchemy import Column, Integer, Text, BigInteger, DateTime, Identity, Boolean, String
from db import Base

class User(Base):
    # 数据库中的表名
    __tablename__ = "users"

    # 字段定义
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
```

### 初始化数据库

```python
from db import Base, engine, session, init_db
from user_model import User


if __name__ == "__main__":
    # 初始化数据库(需要引入对应模型类)
    init_db()
```

## CRUD

### 新增数据

```python
# 单个新增
user1 = User(username="Alice", age=25)
session.add(user1)
# 提交事务
session.commit()

# 批量新增
user2 = User(username="Bob", age=30)
user3 = User(username="Charlie", age=22)
session.add_all([user2, user3])
session.commit()
```

### 查询数据

```python
# 1. 查询所有用户
all_users = session.query(User).all()

# 2. 根据主键查询
user = session.query(User).get(1)

# 3. 条件查询
# 等于查询用filter_by，复杂条件用filter
user = session.query(User).filter_by(username="Alice").first()
# 查年龄大于23的用户
users = session.query(User).filter(User.age > 23).all()
# 多条件AND查询
users = session.query(User).filter(User.age > 20, User.age < 30).all()

# 4. 排序：按年龄降序排列
users = session.query(User).order_by(User.age.desc()).all()

# 5. 分页：第2页，每页2条
users = session.query(User).order_by(User.id).limit(2).offset(2).all()
```

### 更新数据

```python
# 单条更新：先查再改
user = session.query(User).get(1)
user.age = 26
session.commit()

# 批量更新：把所有小于18岁的用户年龄统一改为18
session.query(User).filter(User.age < 18).update({"age": 18})
session.commit()
```

### 删除数据

````python
# 单条删除
user = session.query(User).get(1)
session.delete(user)
session.commit()

# 批量删除
session.query(User).filter(User.age > 60).delete()
session.commit()
````

### 事务

```python
try:
    user = User(username="Alice", age=25)
    session.add(user)
    session.commit()
except Exception:
    session.rollback()
    raise
```

### 原生SQL

```python
from sqlalchemy import text

# 1. 简单查询
result = session.execute(text("SELECT * FROM users"))
print("所有用户:", result.all())

# 2. 带参数查询
stmt = text("SELECT * FROM users WHERE age > :min_age")
users = session.execute(stmt, {"min_age": 25}).fetchall()
print("25岁以上用户:", users)

# 3. 更新操作
session.execute(text("UPDATE users SET age=15 WHERE id=:id"), {"id": 1})
session.commit()  # 写操作需要提交
```