# Memory

Memory模块是构建对话式AI系统的核心组件，它负责维护和管理对话历史，使AI能够记住之前的对话内容，从而实现更连贯、更智能的多轮对话交互。

核心作用:

1. 上下文保持：确保AI理解当前对话与之前对话的关联性
2. 状态管理：跟踪对话流程和用户偏好
3. 个性化交互：基于历史对话提供个性化响应
4. 长期记忆：支持跨越多个会话的记忆持久化

## 短时记忆
短时记忆通常存储在内存中，用于维护当前对话的上下文

- ConversationBufferMemory：存储完整的对话历史
- ConversationBufferWindowMemory：仅保留最近 N 轮对话，避免内存溢出
- ConversationSummaryMemory：对对话内容进行摘要，压缩存储

### ConversationBufferMemory


```python
from langchain.memory import  ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("你好，我是人类！")
memory.chat_memory.add_ai_message("你好，我是AI，有什么可以帮助你的吗？")

history = memory.load_memory_variables({})
print(history)
```

优点:
1. 信息完整保留  
   保留全部对话细节，避免因摘要或截断导致的关键信息丢失。
   适合需要精确回溯上下文的场景（如法律咨询、技术调试）。
2. 实现简单  
   无需复杂的摘要模型或动态筛选逻辑，开发成本低。
3. 上下文连贯性  
   模型能基于完整历史生成更一致的回复，尤其适合长程依赖的对话（如故事创作、多轮决策）

缺点:
1. Token 消耗大  
   对话越长，占用 Token 越多，容易触发模型的长度限制（如 GPT-3.5 的 4K Token）
   可能导致高成本（按 Token 计费）或响应速度下降
2. 效率低下
   冗余信息（如寒暄、重复内容）会降低模型处理效率
   超出限制时需强制截断，可能丢失早期重要信息
3. 不适用于超长对话
   当对话轮次较多时，后续交互可能无法有效利用早期上下文

适用场景:

1. 短对话或任务型对话  
   例如客服问答、简单命令控制（如智能家居），对话轮次少，无需复杂记忆管理
2. 对上下文准确性要求高的场景
   如医疗诊断、代码调试，需完整参考历史记录
3. 原型开发或快速验证
   在项目初期可用作基础记忆方案，快速测试对话流程

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

优点:
1. 内存效率高
   仅保留最近的对话记录，避免内存无限增长，适合长期对话或资源受限的场景
2. 减少噪声干扰
   自动丢弃较早的对话历史，避免无关信息干扰当前对话的连贯性
3. 实时性较强
   专注于近期交互，更适合需要紧跟当前话题的对话（如客服、任务导向型对话）

缺点:
1. 上下文丢失风险
   若关键信息出现在窗口之外（如对话早期的重要设定），系统可能无法正确引用，导致回答不一致或错误
2. 不适用于长依赖任务
   对于需要长期记忆的场景（如多轮复杂推理、用户偏好记录），其能力有限
3. 窗口大小难以调优
   窗口过小可能导致信息缺失，过大则引入冗余，需根据具体场景调整

适用场景:
1. 短对话任务
   如简单问答、指令执行、订单查询等无需长期记忆的交互
2. 资源敏感环境
   嵌入式设备或低配置服务器中，需严格控制内存占用时
3. 高实时性需求场景
   如在线客服、语音助手，需快速响应最近几轮对话内容
4. 避免历史干扰的对话
   当早期对话可能与当前话题无关时（如话题已切换），限制窗口可提升准确性

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

优点:
1. 节省上下文窗口  
   将冗长的对话历史压缩为简洁的摘要，显著减少Token消耗（尤其对按Token计费的模型重要）
2. 长期依赖维护  
   避免因上下文长度限制丢失早期关键信息，适合长周期对话（如客服会话、治疗记录）
3. 结构化重点信息  
   提取核心意图、决策或用户偏好，提升AI回复的连贯性和针对性

缺点:
1. 信息损失风险  
   摘要过程可能忽略细节（如数字、特定表述），影响精确性
2. 摘要偏差  
   自动总结可能扭曲原意或强调次要内容，依赖模型摘要能力
3. 实时性延迟  
   需定期触发摘要，可能无法实时反映最新对话变化

适用场景:
1. 长周期交互应用
   如心理健康辅导、教育导师等需长期跟踪用户进度的场景
2. 资源敏感环境
   需控制API成本或模型上下文有限的场景（如低配本地部署）
3. 主题聚焦型对话
   用户需求明确且需持续优化回复的场景（如商品推荐、项目规划）

## 记忆实体
通过提取对话中的关键实体（如人名、地点、任务），构建结构化记忆

### ConversationEntityMemory

功能: 提取对话中的实体（如人名、地点）并单独存储。
适用场景: 需要跟踪具体实体的对话
实现方案:


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