# Pydantic

Pydantic 是一个用于数据验证和设置管理的 Python 库，主要利用 Python 类型注解

## 基础用法

### 安装
```shell
pip install pydantic
```

### 基本模型定义
```python
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    created_at: datetime = None
    tags: List[str] = []
```
`Optional` 是 `Pydantic` 中用于定义可选字段的重要工具，表示字段值可以是特定类型或 `None`

### 创建实例和验证

```python
user_data = {
    "id": 1,
    "name": "Tom",
    "email": "tom@example.com",
    "age": 25,
    "tags": ["python", "developer"],
    "created_at": datetime.now()
}

user = User(**user_data)
print(user)

# 错误数据
try:
    invalid_user = User(id="not_number", name="Bob")
except ValidationError as e:
    print(e.json())
```

### 递归模型

```python
from pydantic import BaseModel
from typing import List, ForwardRef

# 处理相互递归引用
UserRef = ForwardRef('User')

class User(BaseModel):
    name: str
    friends: List[UserRef] = []

# 解析前向引用
User.model_rebuild()

user1 = User(name='Tom')
user2 = User(name='Bob')
user1.friends.append(user2)
user2.friends.append(user1)
print(user1)
print(user2)
```

### 数据序列化

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    tags: List[str] = []
    metadata: Dict[str, str] = {}

# 创建实例
user = User(
    id=1,
    name="Tom",
    email="1@1.com",
    created_at=datetime.now(),
    tags=["vip", "active"],
    metadata={"role": "admin"}
)

# 序列化为字典
print(user.model_dump())

# 序列化为 JSON
print(user.model_dump_json())

# 带缩进的 JSON
print(user.model_dump_json(indent=2))
```

## 字段类型

### 基本类型
```python
from pydantic import BaseModel
from typing import Dict, List, Set, Tuple, Union
from decimal import Decimal
from pathlib import Path

class DataTypes(BaseModel):
    # 基本类型
    integer: int
    floating: float
    string: str
    boolean: bool
    
    # 复杂类型
    list_data: List[int]
    dict_data: Dict[str, int]
    set_data: Set[str]
    tuple_data: Tuple[int, str, float]
    
    # 特殊类型
    decimal_num: Decimal
    file_path: Path
    
    # 联合类型
    union_field: Union[int, str, None]
```
`Union` 是 `Pydantic` 中用于定义"联合类型"的工具，表示字段可以是多种类型中的任意一种, 在Python3.10中简化语法 `union_field: int | str | None`

### 高级字段类型

```python
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr
from typing import Literal
from datetime import datetime

class AdvancedTypes(BaseModel):
    # 邮箱验证
    email: EmailStr
    # URL验证
    url: HttpUrl
    # 敏感数据（不打印明文）
    password: SecretStr

    # 字面量类型
    status: Literal["active", "inactive", "pending"]

    # 使用 Field 进行更精细控制
    from pydantic import Field

    age: int = Field(gt=0, le=150, description="年龄必须在0-150之间")
    name: str = Field(min_length=1, max_length=50)
    create_time: datetime = Field(alias="createTime", default=datetime.now())

advanceDict = {
    "email": "1@1.com",
    "url": "http://www.baidu.com",
    "password": "password",
    "status": "active",
    "age": 20,
    "name": "Tom",
    "createTime": datetime(2025, 1, 1, 0, 0, 0)
}
types = AdvancedTypes(**advanceDict)
print(types)
```

## 验证器

在 `Pydantic V2` 中，验证器分为字段验证器和模型验证器，分别对应 `V1` 的 `@validator` 和 `@root_validator`

### 字段验证器

```python
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class User(BaseModel):
    username: str
    password: str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名必须为字母数字')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('密码不匹配')
        return v
```

适用于单字段验证场景

### 模型验证器
`@model_validator` 的 `mode` 参数有两个选项: 'before' 和 'after'

- before: 在字段验证之前执行，适用于数据预处理、转换
- after: 在字段验证之后执行，适用于业务逻辑验证、跨字段检查

```python
from typing import Any

from pydantic import BaseModel, model_validator


class User(BaseModel):
    username: str
    password: str
    confirm_password: str

    @model_validator(mode='before')
    @classmethod
    def preprocess_user_data(cls, data: Any) -> Any:
        """前置处理器：数据清洗、格式标准化"""
        if isinstance(data, dict):
            # 用户名标准化：去除空格，转为小写
            if 'username' in data and isinstance(data['username'], str):
                original_username = data['username']
                data['username'] = original_username.strip().lower()
            # 密码去除首尾空格
            if 'password' in data and isinstance(data['password'], str):
                data['password'] = data['password'].strip()

            if 'confirm_password' in data and isinstance(data['confirm_password'], str):
                data['confirm_password'] = data['confirm_password'].strip()
        return data

    @model_validator(mode='after')
    def validate_user_business_rules(self) -> 'User':
        """后置验证器：业务逻辑验证和衍生字段计算"""
        if self.password != self.confirm_password:
            raise ValueError('密码不匹配')
        return self


if __name__ == "__main__":
    user = User(username=" Tom ", password="123456", confirm_password=" 123456")
    print(user)
```

适用于跨字段逻辑、复杂业务规则


## 环境变量配置

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',           # 环境变量文件
        env_file_encoding='utf-8', # 文件编码
        case_sensitive=False,      # 环境变量不区分大小写
        extra='ignore',            # 忽略额外字段
    )

    # 字段定义
    database_url: str = Field(alias='DATABASE_URL')
    api_key: str = Field(alias='API_KEY', min_length=10)
    debug: bool = False
    port: int = 8000

if __name__ == "__main__":
    # 使用示例
    settings = AppSettings()
    print(settings)
```
