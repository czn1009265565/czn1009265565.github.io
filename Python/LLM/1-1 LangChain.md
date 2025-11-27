# LangChain
Langchain是一个用于构建大语言模型（LLM）应用程序的开源框架。
它通过模块化设计，简化了LLM应用的开发流程，使开发者能够更高效地集成、调用和管理语言模型。

## 环境搭建

```shell
pip install "langchain>=1.1.0" langchain-openai langchain-community
```

## 核心功能

1. 模块化组件  
   - 模型封装：支持多种LLM（如OpenAI GPT、Qwen3模型等），提供统一的接口调用
   - 提示模板管理：可预设提示词模板，动态填充内容，提升交互效率
   - 链式调用：将多个LLM调用或工具组合成工作流（例如：问答→总结→翻译）
   - 记忆机制：支持会话历史记录，实现多轮对话的上下文保持
2. 数据集成与处理  
   - 文档加载器：支持从文本、PDF、网页等来源加载数据
   - 文本分割与向量化：结合嵌入模型（如OpenAI Embeddings）将文本转换为向量，便于检索
   - 检索增强生成：通过向量数据库（如FAISS、Chroma）检索外部知识，增强LLM回答的准确性
3. 代理与工具集成  
   - 智能代理：允许LLM根据需求调用外部工具（如计算器、API、数据库查询）
   - 自定义工具：开发者可扩展工具库，实现特定领域的功能（如股票查询、天气检索）
4. 部署与监控  
   - 异步支持：优化高并发场景下的性能
   - 日志与追踪：记录LLM调用链路，便于调试和效果分析

## 适用场景

1. 智能问答系统  
   - 结合RAG技术，为企业知识库、客服机器人提供精准答案
   - 示例：内部文档检索、技术支持助手
2. 自动化流程工具  
   - 链式调用实现多步骤任务，如数据分析报告生成、邮件自动回复
   - 示例：从数据库提取数据→生成摘要→发送邮件
3. 内容生成与优化  
   - 利用提示模板批量生成营销文案、代码注释、多语言翻译
   - 示例：电商产品描述生成、技术文档翻译
4. 代理决策系统  
   - 通过工具集成实现复杂决策，如投资分析、日程管理
   - 示例：LLM调用财经API分析股票趋势，生成建议
5. 教育与研究
   - 快速构建实验性LLM应用，验证模型效果或新算法
   - 示例：学术论文摘要工具、交互式学习助手

## 核心概念

### Model I/O

Model I/O 是 LangChain 中最基础也是最核心的模块，它定义了与任何大型语言模型（LLM）进行交互的标准流程。
这个流程可以概括为：输入（Prompt）→ 模型（LLM）→ 输出解析（Output Parser）。

1. Prompts (提示模板)  
   核心思想：将用户输入和固定指令模板化，实现提示词的复用和管理，而不仅仅是简单的字符串拼接

2. LLMs (大语言模型)  
   核心思想：提供一个统一的接口来调用各种语言模型，无论是 OpenAI、Anthropic 的开源模型，还是本地部署的模型。
3. Output Parsers (输出解析器)  
   核心思想：将语言模型返回的非结构化文本（字符串）转换成结构化、可编程的数据（如 JSON 对象、Pydantic 模型对象）

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
api_key="sk-",
base_url="https://api.deepseek.com/v1",
model="deepseek-chat"
)

# 使用 ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("回答这个问题: {question}")
chain = prompt | llm
response = chain.invoke({"question": "什么是机器学习？"})
print(response.content)
```

### LCEL(LangChain Expression Language)基础
核心思想： 提供一种声明式的、链式的语法，将多个组件（如 Prompt、LLM、Output Parser、工具等）像搭积木一样组合成一个复杂的“链”

核心操作符： 管道操作符 |。它表示“将前一个组件的输出传递给后一个组件作为输入”

```python
# 使用 LCEL 写法
chain = prompt | chat_model | parser

# 调用链
result = chain.invoke({"product": "特斯拉电动汽车"})
```

优势：  
1. 简洁性：代码一目了然
2. 自动功能：无需额外代码，链就支持 stream（流式输出）、batch（批量处理）、async（异步调用）
3. 可组合性：可以轻松地将小链组合成大链，构建复杂的 AI 应用

### 消息系统(HumanMessage, AIMessage, SystemMessage)

核心思想： 聊天模型是基于“消息”历史的上下文来生成回复的。不同的消息角色（人、AI、系统）承载着不同的语义。准确描述聊天对话中的不同角色，这对于现代聊天模型至关重要。

核心类：
- SystemMessage（系统消息）： 为 AI 设定角色、行为和目标的指令。例如：“你是一个有用的助手，且所有回答不得超过50个字。” 这条消息通常不会被用户看到
- HumanMessage（用户消息）： 代表人类用户说的话或提出的问题。例如：“你好，请介绍一下你自己。”
- AIMessage（AI消息）： 代表 AI 助手之前的回复。用于在多轮对话中提供历史上下文
- FunctionMessage / ToolMessage： 与“工具调用”功能相关，代表函数或工具执行后的结果

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import HumanMessage, AIMessage, SystemMessage

# 定义聊天提示模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的电影评论家。"),
    ("human", "请问电影《奥本海默》怎么样？"),
])

chat_model = ChatOpenAI(
    api_key="sk-",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

# 创建链
chain = template | chat_model

# 调用
response = chain.invoke({})
print(response.content)
```