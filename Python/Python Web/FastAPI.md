# FastAPI

## 安装部署

仅安装 FastAPI 的核心包及其最小必要依赖

```shell
pip install fastapi
```

安装 FastAPI 完整功能套件，包括所有可选依赖（如文档支持、数据库驱动、异步工具等）
```shell
pip install "fastapi[all]"
```

额外依赖示例:
- uvicorn（ASGI 服务器）
- httpx（HTTP 客户端）
- jinja2（模板渲染）
- python-multipart（表单数据处理）
- itsdangerous（安全相关）
- pyjwt（JWT 支持


另外还需要一个 ASGI 服务器，生产环境可以使用 Uvicorn 或者 Hypercorn

```shell
pip install "uvicorn[standard]"
```

## 第一个应用

创建基础应用
```python
from fastapi import FastAPI

app = FastAPI()

# 定义根路径
@app.get("/")
def read_root():
    return {"Hello": "World"}


# 带路径参数的路由
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

或执行启动命令
```shell
uvicorn main:app --reload --port 8000
```

## 基本路由和请求方法

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 数据模型
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# GET - 获取数据
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# POST - 创建数据
@app.post("/items/")
async def create_item(item: Item):
    return item

# PUT - 更新数据
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# DELETE - 删除数据
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
```

异步路由 (async def):
- 真正的异步执行: 函数内部可以使用 await 调用其他异步操作
- 非阻塞: 遇到 I/O 操作时（如数据库查询、API 调用），会释放控制权给事件循环
- 适用场景: 包含异步 I/O 操作的路由

同步路由 (def):
- 在线程池中运行: FastAPI 会自动将同步函数放入线程池执行，避免阻塞主事件循环
- 阻塞操作: 如果函数内部有耗时操作（如复杂计算、同步 I/O），会阻塞当前工作线程
- 适用场景: 纯计算任务或无异步版本的库

## 请求参数类型

### 路径参数
```python
@app.get("/users/{user_id}")
async def read_user(user_id: int):  # 类型自动转换和验证
    return {"user_id": user_id}
```

### 查询参数
```python
@app.get("/items/")
async def read_items(
    skip: int = 0,           # 可选参数，默认值
    limit: int = 10,         # 可选参数，默认值
    q: str | None = None     # 可选字符串参数
):
    return {"skip": skip, "limit": limit, "q": q}
```

### 请求体

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    age: int | None = None

@app.post("/users/")
async def create_user(user: User):  # 自动验证请求体
    return user
```

## 响应模型和状态码

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class UserIn(BaseModel):  # 输入模型
    username: str
    password: str
    email: str

class UserOut(BaseModel):  # 输出模型（不包含密码）
    username: str
    email: str

@app.post(
    "/users/", 
    response_model=UserOut,  # 指定响应模型
    status_code=status.HTTP_201_CREATED  # 自定义状态码
)
async def create_user(user: UserIn):
    # 业务逻辑...
    return user  # 自动过滤密码字段
```

## 异常处理

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}

# 自定义异常处理器
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )
```

## 依赖注入

```python
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi import Header, HTTPException
from sqlmodel import create_engine, Session

app = FastAPI()

# 数据库连接 依赖注入
engine = create_engine("mysql+pymysql://root:password@localhost:3306/dbname")

def get_session():
    with Session(engine) as session:
        yield session

# 权限校验 Header中的x-token参数
def verify_token(x_token: str = Header()):
    if x_token != "super-secret-token":
        raise HTTPException(status_code=403, detail="No Permission")
    return x_token


SessionDep = Annotated[Session, Depends(get_session)]
CurrentToken = Annotated[str, Depends(verify_token)]

@app.get("/test1")
def read_items(db: SessionDep, token: CurrentToken):
    return {"status": "success"}

@app.get("/test2")
def read_items(db: Session = Depends(get_session), token: str = Depends(verify_token)):
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```
其中test1与test2写法等价，因为 FastAPI 在底层“接管”了对 Annotated 的解析

## 自动 API 文档

启动服务后访问:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


## 项目结构

```
my_fastapi_project/
├── main.py              # 应用入口
├── routers/             # 路由模块
│   ├── __init__.py
│   ├── items.py
│   └── users.py
├── models.py           # Pydantic 模型
├── dependencies.py     # 依赖项
└── requirements.txt    # 依赖列表
```

模块化示例

```python
# routers/items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def read_items():
    return [{"name": "Item 1"}, {"name": "Item 2"}]

# main.py
from fastapi import FastAPI
from routers import items, users

app = FastAPI()
app.include_router(items.router)
app.include_router(users.router)
```


## 生产部署

### Gunicorn + Uvicorn

```shell
# 安装
pip install gunicorn

# 运行（多进程）
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Docker

```Dockfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
