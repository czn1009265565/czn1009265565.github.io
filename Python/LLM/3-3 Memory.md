# Memory

## 短时记忆
短时记忆通常存储在内存中，用于维护当前对话的上下文

- ConversationBufferMemory：存储完整的对话历史
- ConversationBufferWindowMemory：仅保留最近 N 轮对话，避免内存溢出
- ConversationSummaryMemory：对对话内容进行摘要，压缩存储

### ConversationBufferMemory

功能：存储完整的对话历史（原始形式）。
适用场景：需要完整上下文的小规模对话。
实现方案：

```python
from langchain.memory import  ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("你好，我是人类！")
memory.chat_memory.add_ai_message("你好，我是AI，有什么可以帮助你的吗？")

history = memory.load_memory_variables({})
print(history)
```

### ConversationBufferWindowMemory

功能：仅保留最近 K 轮对话，避免内存溢出。
适用场景：长对话中只需近期上下文。
实现方案：

```python
from langchain.memory import ConversationBufferWindowMemory

# 只保留最近2轮对话
memory = ConversationBufferWindowMemory(k=2)

# 模拟多轮对话
memory.save_context({"input": "第一句话"}, {"output": "第一句回复"})
memory.save_context({"input": "第二句话"}, {"output": "第二句回复"})
memory.save_context({"input": "第三句话"}, {"output": "第三句回复"})

history = memory.load_memory_variables({})
print(history)  # 输出：{'history': 'Human: 第二句话\nAI: 第二句回复\nHuman: 第三句话\nAI: 第三句回复'}
```

### ConversationSummaryMemory

功能：对历史对话生成摘要，节省空间。
适用场景：超长对话的摘要存储。
实现方案：

```python
from langchain.memory import ConversationSummaryMemory

# 使用LLM生成摘要
memory = ConversationSummaryMemory(llm=llm)

memory.save_context({"input": "Langchain是什么？"}, {"output": "一个用于开发LLM应用的框架。"})
memory.save_context({"input": "它有哪些功能？"}, {"output": "支持链式调用、记忆管理、工具集成等。"})

history = memory.load_memory_variables({})
print(history)
```

## 记忆实体
通过提取对话中的关键实体（如人名、地点、任务），构建结构化记忆

### ConversationEntityMemory

功能: 提取对话中的实体（如人名、地点）并单独存储。
适用场景: 需要跟踪具体实体的对话
实现方案:

```python

```


## 知识图谱
将外部知识图谱与对话记忆结合，实现语义化记忆

### ConversationKGMemory

功能: 将对话内容转换为三元组（主体-关系-客体），构建知识图谱并持久化。
优势:  
- 支持复杂关系推理（如“A 是 B 的同事”）
- 便于跨对话查询关联知识

```python
from langchain.memory import ConversationKGMemory

# 初始化知识图谱记忆
memory = ConversationKGMemory(
    llm=llm,
    k=5  # 保留最近 5 个三元组
)

# 模拟对话
conversation = [
    "用户：Tom是Microsoft的员工",
    "用户：Kim也是Microsoft的员工",
    "用户：Bob是Microsoft的老板"
]

# 注入对话历史
for msg in conversation:
    memory.save_context(
        {"input": msg.split("：")[1]},
        {"output": "助手回复已处理"}
    )

# 查看知识图谱的三元组
print("知识图谱三元组：", memory.kg.get_triples())
```

## 长时记忆实现方式

长时记忆依赖外部存储，实现持久化与大规模数据管理

- 数据库存储: 使用 SQLite、PostgreSQL 等关系型数据库，或 MongoDB 等 NoSQL 数据库存储历史对话
- 向量数据库: 结合 Embedding 模型，将对话内容向量化后存入 Chroma、Pinecone 等，支持语义检索
- 文件系统存储: 以 JSON、CSV 等格式保存对话记录，适用于离线分析或冷数据存储

### VectorStoreRetrieverMemory
功能: 将对话历史转换为向量并存入向量数据库，根据当前查询语义检索最相关的历史片段。
优势:  
- 支持大规模对话存储
- 通过语义相似度检索，避免依赖固定窗口大小。
- 适用场景：长对话、多轮任务导向型对话（如客服、知识问答）

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Chroma

# 1. 初始化 Embedding 模型和向量数据库
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(embedding_function=embedding, persist_directory="./chroma_db")

# 2. 创建检索器 (保留最相似的 1 条历史记录)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# 3. 初始化 VectorStoreRetrieverMemory
memory = VectorStoreRetrieverMemory(retriever=retriever)

# 4. 存储对话
memory.save_context({"input": "Python的优点"}, {"output": "简洁易学、生态丰富。"})
memory.save_context({"input": "臭豆腐"}, {"output": "绍兴特色美食"})

# 5. 语义检索
result = memory.load_memory_variables({"prompt": "食物"})
print(result)
```