# LangChain
LangChain 是一个用于开发大语言模型（LLM）应用程序的框架，
核心思想是通过“链”（Chain）的方式将LLM与外部数据源、工具等连接起来，让LLM能够完成更复杂、更实用的任务，而不仅仅是简单的对话。
它通过模块化设计，简化了LLM应用的开发流程，使开发者能够更高效地集成、调用和管理语言模型。

## 解决的问题
在没有 LangChain 之前，开发LLM应用面临的主要问题: 

1. “记忆力”短: LLM本身无法记住长篇对话或文档内容
2. 信息孤立: LLM的知识局限于其训练数据，无法获取实时、私有或特定的外部信息
3. 能力单一: LLM只能进行文本生成和对话，无法执行具体动作（如计算、查询数据库、调用API）
4. 开发复杂: 要将LLM与各种组件组合起来，需要大量定制化代码，流程繁琐且难以复用

LangChain 正是为了解决这些问题而生的，使得LLM能够:

1. 访问并处理私人或特定领域的文档
2. 拥有长期记忆，进行多轮复杂对话
3. 调用外部工具和API，执行具体任务
4. 以标准化、可复用的方式构建复杂应用

## 环境搭建

```shell
pip install --upgrade langchain==0.0.279 
pip install --upgrade openai==0.27.8 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

校验是否安装成功,查看是否打印对应版本
```shell
pip show langchain
pip show openai
```

## First Example

OpenAI 官方SDK
```python
import os
import openai

os.environ["OPENAI_KEY"] = "sk-"
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"

openai.api_key = os.getenv("OPENAI_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

messages = [
    {"role": "user", "content": "介绍下你自己"}
]

res = openai.ChatCompletion.create(
    model="Qwen3-Coder-480B",
    messages=messages,
    stream=False,
)

print(res['choices'][0]['message']['content'])
```

LangChain调用
```python
import os
from langchain.chat_models import ChatOpenAI


os.environ["OPENAI_KEY"] = "sk-"
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_KEY")
llm = ChatOpenAI(
   model="Qwen3-Coder-480B",
   openai_api_key=api_key,
   openai_api_base=api_base
)
predict = llm.predict("介绍下你自己")
print(predict)
```

## 核心功能
LangChain 采用模块化设计，其主要组件可以类比为建房子的不同部分

### 1. Model I/O
Model I/O 是 LangChain 中最基础也是最核心的模块，它定义了与任何大型语言模型（LLM）进行交互的标准流程。
这个流程可以概括为: 输入（Prompt）→ 模型（LLM）→ 输出解析（Output Parser）

1. Prompts (提示词模板): 将用户输入和固定指令模板化，实现提示词的复用和管理，而不仅仅是简单的字符串拼接
2. LLMs (大语言模型): 提供一个统一的接口来调用各种语言模型，无论是 OpenAI、Anthropic 的开源模型，还是本地部署的模型
3. Output Parsers (输出解析器): 将语言模型返回的非结构化文本（字符串）转换成结构化、可编程的数据（如 JSON 对象、Pydantic 模型对象），便于程序后续处理


### 2. 检索（Retrieval）
这是让LLM“拥有”外部知识的关键，通常用于构建问答系统或基于文档的聊天机器人

1. 文档加载器（Document Loaders）: 从各种来源（PDF、Word、网页、数据库）加载文档
2. 文本分割器（Text Splitters）: 将长文档拆分成模型上下文窗口能容纳的小块
3. 向量存储（Vectorstores）: 将文档转换为向量（Embeddings）并存储，以便进行语义搜索
4. 检索器（Retrievers）: 根据用户问题，从向量存储中快速检索出最相关的文档片段

### 3. 链（Chains）
链是LangChain的灵魂，它将多个组件（如 Prompt、LLM、Output Parser、工具等）按特定顺序组合起来，完成一个复杂任务

1. 简单链: 将一个提示词模板、一个模型和一个输出解析器连接起来
2. 顺序链（SequentialChain）: 将多个链按顺序执行，前一个链的输出作为后一个链的输入
3. 检索问答链（RetrievalQA）: 一个非常经典的链，它结合了检索和问答: 先检索相关文档，再将文档和问题一起发给LLM生成答案
4. 摘要链（load_summarize_chain）：用于生成文档摘要

### 4. 智能体（Agents）
智能体是LangChain最强大的功能之一。它让LLM扮演“大脑”的角色，能够自主决定调用哪些工具来完成任务

1. 核心思想: LLM根据用户目标进行推理，决定行动步骤，调用工具，并根据工具返回的结果决定下一步动作
2. 工具（Tools）: 代理可以调用的函数，如: 搜索引擎、计算器、数据库查询、API调用等
3. 适用场景: 需要动态决策的复杂任务，例如“查一下今天北京的天气，并推荐一件适合穿的衣服”


### 5. 内存（Memory）
用于在多次交互中持久化状态（对话历史），让LLM拥有“记忆”。

1. 简单内存: 只记住上一次的对话。
2. 缓冲区内存: 记住最近N轮对话。
3. 向量存储内存: 将历史对话存入向量数据库，实现长期、可检索的记忆。


## 适用场景

1. 智能问答系统  
   - 结合RAG技术，为企业知识库、客服机器人提供精准答案
   - 示例: 内部文档检索、技术支持助手
2. 自动化流程工具  
   - 链式调用实现多步骤任务，如数据分析报告生成、邮件自动回复
   - 示例: 从数据库提取数据→生成摘要→发送邮件
3. 内容生成与优化  
   - 利用提示模板批量生成营销文案、代码注释、多语言翻译
   - 示例: 电商产品描述生成、技术文档翻译
4. 代理决策系统  
   - 通过工具集成实现复杂决策，如投资分析、日程管理
   - 示例: LLM调用财经API分析股票趋势，生成建议
5. 教育与研究
   - 快速构建实验性LLM应用，验证模型效果或新算法
   - 示例: 学术论文摘要工具、交互式学习助手