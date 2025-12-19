# Chroma

Chroma 是一个开源的向量数据库，专门为 AI 应用设计，特别适合存储和检索嵌入向量（embeddings）

## 安装部署
这里以Chroma为例

```shell
python -m venv chroma
source chroma/bin/activate  # Linux/macOS
# 或 chroma\Scripts\activate  # Windows

# 安装Chroma
pip install chromadb

# 启动服务
chroma run --host 0.0.0.0 --port 8000
```

访问 `http://localhost:8000/api/v2/heartbeat` 查看返回值

## 基本操作

### 创建数据库实例

```python
import chromadb
chroma_client = chromadb.Client()

# 默认内存存储
collection = chroma_client.create_collection(name="document_collection")

# 持久化模式
client = chromadb.PersistentClient(path="./chroma_db")
```
客户端服务器模式
```shell
# 启动服务器
chroma run --path /path/to/db
```

```python
import chromadb
# 客户端连接
client = chromadb.HttpClient(host="localhost", port=8000)
```

在创建 `collection` 时可以指定自己的 `embedding` 方法。若不指定，默认使用 `all-minilm-l6-v2` 模型

### 添加文档
```python
documents = [
    "Chroma 是一个向量数据库",
    "它专门为 AI 应用设计",
    "支持高效的相似性搜索"
]
metadatas = [{"source": "intro"}, {"source": "purpose"}, {"source": "feature"}]
ids = ["doc1", "doc2", "doc3"]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
```

添加文档需要包含以下要素:  
- ids（必填），标识符列表，每个文档/向量的唯一ID
- documents（必填），文本内容，会自动转换为向量
- metadatas（可选），元数据字典，用于过滤和查询
- embeddings（可选），预计算的向量嵌入
- uris（可选），外部资源URI，用于存储文件路径或URL
- data（可选），二进制数据，存储原始字节

### 相似性搜索

```python
# 查询相似文档
results = collection.query(
    query_texts=["什么是 Chroma 数据库"],
    where={"source": "intro"},
    n_results=2
)
```
参数说明:  
- query_embeddings，直接使用向量进行查询
- query_texts，使用文本进行查询（会自动转换为向量）
- n_results，返回结果的数量
- where，基于元数据的过滤条件
- where_document，基于文档内容的过滤条件
- include，控制返回的内容

### 文档更新

```python
# 更新单个文档
collection.update(
    ids="doc1",
    documents="更新后的内容",
    metadatas={"category": "更新", "version": 2}
)

# 批量更新多个文档
collection.update(
    ids=["doc1", "doc2", "doc3"],
    documents=["新内容1", "新内容2", "新内容3"],
    metadatas=[
        {"status": "updated", "time": "2024-01-01"},
        {"status": "updated", "time": "2024-01-01"},
        {"status": "updated", "time": "2024-01-01"}
    ]
)
```

### 文档删除

```python
# 删除单个文档
collection.delete(ids="doc1")

# 批量删除多个文档
collection.delete(ids=["doc1", "doc2", "doc3"])

# 删除所有文档（危险操作）
all_docs = collection.get()
if all_docs["ids"]:
    collection.delete(ids=all_docs["ids"])

# 删除特定类别的文档
collection.delete(where={"category": "临时"})

# 删除过期的文档
collection.delete(where={
    "expiry_date": {"$lt": "2024-01-01"}  # 删除2024年之前的文档
})

# 复杂条件删除
collection.delete(where={
    "$and": [
        {"status": "inactive"},
        {"category": "测试"},
        {"create_time": {"$lt": "2023-01-01"}}
    ]
})
```