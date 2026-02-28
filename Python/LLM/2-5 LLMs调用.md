# LLMs调用
LangChain 将 LLM 供应商的 API 进行了标准化封装，使得切换不同模型（如 OpenAI、Azure、Anthropic、本地模型等）的代码几乎一致，极大提高了可移植性。

在 LangChain 中，主要有两种类型的模型封装:

- LLMs(OpenAI): 基础文本补全模型。输入一个字符串，输出一个字符串，例如 `Qwen2.5-Coder`
- ChatModels(ChatOpenAI): 对话优化的模型。它们的输入和输出是结构化的 消息（如 HumanMessage, AIMessage, SystemMessage），例如 `Qwen3-Coder-Flash`

现代应用开发中，更推荐使用 ChatModels


### 基础文本补全模型

```python
import os
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "sk-"
os.environ["OPENAI_API_BASE"] = ""

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")

# 初始化支持流式传输的模型
llm = OpenAI(
    model = "Qwen2.5-Coder",
    temperature=0,
    openai_api_key = api_key,
    openai_api_base = api_base,
    max_tokens=512,
)
# 流式输出
for chunk in llm.stream("请介绍一下你自己"):
    print(chunk,end="",flush=False)
```

###  对话优化模型

```python
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = "sk-"
os.environ["OPENAI_API_BASE"] = ""

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")


# 初始化模型
chat_model = ChatOpenAI(
    model="GLM-4.7",
    openai_api_key = api_key,
    openai_api_base = api_base,
    temperature=0
)

messages = [
    SystemMessage(content="你是一个AI助手"),
    HumanMessage(content="请介绍一下你自己")
]

# 支持输入Message列表
response = chat_model.invoke(messages)
# 通过content获取文本
print(response.content)
print("========================分割线========================")

# 字符串自动转换为 HumanMessage
response = chat_model.invoke("请介绍一下你自己")
print(response)

print("========================分割线========================")
# 流式输出
for chunk in chat_model.stream("请介绍一下你自己"):
    print(chunk,end="",flush=False)
```
