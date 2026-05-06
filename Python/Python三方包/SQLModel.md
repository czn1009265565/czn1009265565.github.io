# SQLModel

SQLModel 是由 FastAPI 作者开发的现代 Python ORM 库，完美结合了 Pydantic 的数据验证和 SQLAlchemy 的数据库操作能力

## 环境安装

```shell
pip install sqlmodel

# 按需安装数据库驱动
pip install pymysql      # MySQL
pip install psycopg2-binary  # PostgreSQL
```

## 核心概念

- SQLModel 基类	同时作为 Pydantic 模型和 SQLAlchemy ORM 模型
- Field()	定义数据库字段和验证规则
- Relationship()	处理表间关系（一对多/多对多）
- Session	数据库操作入口，管理事务

## 基础实例

### 数据库连接配置

db.py
```python
from sqlmodel import create_engine, SQLModel, Session

# 创建引擎 连接字符串格式: 数据库类型+驱动://用户名:密码@主机:端口/数据库名
engine = create_engine("mysql+pymysql://root:password@localhost:3306/dbname")

def init_db():
    SQLModel.metadata.create_all(engine)
```

### 模型定义

user_model.py

```python
import hashlib
from datetime import datetime
from sqlmodel import Field, SQLModel, BigInteger

def md5pwd(password: str) -> str:
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.hexdigest()

def default_md5_pwd():
    return md5pwd('password')

def get_timestamp() -> int:
    dt_millis = int(datetime.now().timestamp() * 1000)
    return dt_millis

class BaseUserPO(SQLModel, table=True):
    __tablename__ = "user_profile"

    id: int = Field(nullable=False, sa_type=BigInteger(), primary_key=True)
    name: str = Field(max_length=255, unique=True)
    password: str = Field(default_factory=default_md5_pwd, max_length=255)
    email: str = Field(max_length=255)
    status: int = Field(default=0, nullable=False)
    origin: int = Field(nullable=False, default=0)
    create_time: int = Field(default_factory=get_timestamp, sa_type=BigInteger(), nullable=False)
```

### 初始化数据库

```python
from db import init_db
from user_model import BaseUserPO


if __name__ == "__main__":
    # 初始化数据库
    init_db()
```

## CRUD

### 新增数据

```python
from sqlmodel import Session
from db import engine
from user_model import BaseUserPO

with Session(engine) as session:
    user1 = BaseUserPO(id=1, name='Alice', email='Alice@gmail.com')
    session.add(user1)
    session.commit()

    user2 = BaseUserPO(id=2, name='Bob', email='Bob@gmail.com')
    user3 = BaseUserPO(id=3, name='Charlie', email='Charlie@gmail.com')
    session.add_all([user2, user3])
    session.commit()
```

### 查询数据

```python
with Session(engine) as session:
    # 获取所有记录
    all_users = session.exec(select(BaseUserPO)).all()
    # 按ID查询
    user = session.get(BaseUserPO, 1)
    # 条件查询
    statement = select(BaseUserPO).where(BaseUserPO.status > 0)
    users = session.exec(statement).all()
    # 单字段查询优化
    names = session.exec(select(BaseUserPO.name)).all()
```

### 更新数据

```python
with Session(engine) as session:
    user = session.get(BaseUserPO, 1)
    user.email = '1@gmail.com'
    session.add(user)
    session.commit()
    session.refresh(user)
    print(user)
```

### 删除数据

````python
with Session(engine) as session:
    user = session.get(BaseUserPO, 1)
    session.delete(user)
    session.commit()
````

### 原生SQL

```python
from sqlmodel import Session, text
from db import engine

with Session(engine) as session:
    # 1. 简单查询
    result = session.exec(text("SELECT * FROM users"))
    print("所有用户:", result.all())

    # 2. 带参数查询
    stmt = text("SELECT * FROM users WHERE age > :min_age")
    users = session.exec(stmt, params={"min_age": 25}).all()
    print("25岁以上用户:", users)
```