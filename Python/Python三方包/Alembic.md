# Alembic

Alembic 是 SQLAlchemy 作者编写的数据库迁移工具，用于管理数据库 schema 的版本控制

## 安装和初始化

### 安装 Alembic
```shell
pip install alembic
```

### 项目初始化

```shell
alembic init alembic
```

目录结构
```
project/
├── alembic/
│   ├── versions/          # 迁移脚本目录
│   ├── env.py            # 运行环境配置
│   └── script.py.mako    # 迁移脚本模板
└── alembic.ini          # 主配置文件
```

## 配置数据库连接

### 修改 `alembic.ini`

```
# 修改数据库连接
sqlalchemy.url = driver://user:pass@localhost/dbname
# sqlalchemy.url = mysql+pymysql://user:pass@localhost/dbname
```

### 配置 `env.py`

这里结合SQLModel

```python
# 引入SQLModel 类
from sqlmodel import SQLModel
# 引入 自定义的元数据基类
from user.model.user_model import User
from chat.model.chat_model import Chat

# 设置元数据
target_metadata = SQLModel.metadata
```

自定义元数据基类
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

由于Alembic 默认的生成模版（Script Template）只包含了原生的 sqlalchemy 和 alembic 引用，因此需要我们修改`script.py.mako`文件，
在顶部的 import 区域，新增 `import sqlmodel`

### 执行迁移流程
每当你修改了 SQLModel 定义的模型（如增加字段），按以下两步操作

1. 生成脚本: Alembic 会对比当前数据库与模型定义的差异，自动写好变更逻辑
```shell
alembic revision --autogenerate -m "初始化表结构"
```
2. 应用变更: 将脚本逻辑同步到数据库
```shell
alembic upgrade head
```

## 常用操作命令

```shell
# 查看当前状态
alembic current

# 查看历史
alembic history

# 升级到最新版本
alembic upgrade head

# 升级到特定版本
alembic upgrade 1234567890
alembic upgrade +2  # 升级2个版本

# 回滚到上一个版本
alembic downgrade -1

# 回滚到特定版本
alembic downgrade 1234567890
alembic downgrade base  # 回滚到最初

# 检查是否需要迁移
alembic check
```
