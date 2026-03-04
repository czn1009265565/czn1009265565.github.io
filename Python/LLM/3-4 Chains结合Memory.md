# Chains结合Memory

## 短时记忆

特点:
- 记忆短暂: 超出容量限制后早期对话被丢弃
- 适用场景: 临时性任务（如查询订单状态、短时多轮问答）

```python
from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory

# 初始化短时记忆
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)

# 模拟对话
dialogue = [
    "今天的天气真好。",
    "是的，适合去公园散步。",
    "公园里有什么花开了吗？",  # 此时记忆应包含前两句
    "我明天要开会，没时间去了。"  # 记忆滚动更新，可能移出最早内容
]

for text in dialogue:
    response = chain.run(input=text)
    print(f"用户: {text}\n助手: {response}\n")
```

## 长时记忆

特点:
- 记忆持久: 信息长期保存在向量数据库中
- 语义检索: 即使提问方式不同（如“买了什么” vs “购买记录”），也能匹配相关记忆

```python
from langchain import ConversationChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Chroma

# 1. 初始化向量数据库
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(embedding_function=embedding, persist_directory="./chroma_db")

# 2. 预设历史记忆
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
memory = VectorStoreRetrieverMemory(retriever=retriever)

initial_memories = [
    "用户喜欢科幻电影和披萨",
    "用户上个月购买了无人机",
    "用户的生日是5月20日"
]
for text in initial_memories:
    memory.save_context({"input": text}, {"output": "助手回复已处理"})

# 3. 创建对话链
chain = ConversationChain(llm=llm, memory=memory, verbose=True)

# 4. 测试记忆检索
questions = [
    "推荐一部电影给我吧",      # 应触发“喜欢科幻电影”的记忆
    "我最近买了什么电子产品？"  # 应检索到“购买了无人机”
]
for q in questions:
    print(f"用户: {q}")
    print(f"助手: {chain.run(q)}\n")
```