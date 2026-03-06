# Agent

## 概述
在 LangChain 中，Agent 是一个能够自主思考、调用工具来完成任务的智能体。
它不像普通的 Chain 那样固定执行流程，而是根据用户输入动态决定要执行什么动作（如调用哪个工具、是否需要多次调用等）

### 核心组件

- LLM（大语言模型）：负责推理和决策
- Tools（工具集）：Agent 可以调用的外部功能（如计算器、搜索引擎、API 等）
- Agent Executor：运行 Agent 的引擎，负责调度工具调用和解析 LLM 输出


### 工作原理

1. 接收用户输入（如：“计算 3 的 5 次方是多少？”）
2. LLM 思考: 决定是否需要调用工具、调用哪个工具
3. 执行工具: 获取工具返回结果
4. 再次思考: 结合结果判断是否需要进一步动作
5. 返回最终答案

## 类型

- ZERO_SHOT_REACT_DESCRIPTION: 零样本学习，根据工具描述直接决策，适用于文本补全模型
- CHAT_ZERO_SHOT_REACT_DESCRIPTION: 零样本学习，根据工具描述直接决策，适用于对话模型
- CONVERSATIONAL_REACT_DESCRIPTION: 支持历史上下文，适用于文本补全模型
- CHAT_CONVERSATIONAL_REACT_DESCRIPTION: 支持历史上下文，适用于对话模型
- STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION: 支持结构化输入，适合复杂任务，适用于对话模型

零样本学习: 模型在未见过特定任务示例的情况下，仅通过任务描述和通用知识来执行任务

ReAct框架: 一种将推理(通过思考分析状况、制定方案) 与行动(调用外部工具获取信息或执行操作) 结合的Agent设计范式，灵感来源于人类解决复杂任务时的思考过程
运行流程:
1. Thought（推理）: 分析当前问题、历史记录和可用工具，制定下一步计划方案。
2. Action（行动）: 根据推理结果选择工具并生成调用参数
3. Observation（观察）: 获取工具返回的结果，作为下一步推理的输入
4. 循环: 重复上述过程，直到任务完成或达到终止条件


## 简单示例

### 数学计算 Agent
```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType

# 初始化模型
api_key = ""
api_base = ""
llm = ChatOpenAI(
    model="Qwen3-Coder-Flash",
    openai_api_key=api_key,
    openai_api_base=api_base,
    temperature=0
)

# 1. 初始化 LLM 和工具
tools = load_tools(["llm-math"], llm=llm)  # 加载数学计算工具

# 2. 创建 Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 使用零样本React Agent
    verbose=True  # 显示详细执行过程
)

# 3. 运行测试
question = "请计算 15 的 3 次方是多少？然后给结果加上 28。"
result = agent.run(question)
print(f"\n最终答案: {result}")
```

### 支持记忆

```python
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

tools = load_tools(["llm-math"], llm=llm)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,#处理解析错误
    memory=memory #记忆组件
)

result1 = agent_chain.run('2的平方')
print(result1)
result2 = agent_chain.run('我们刚才聊了什么？')
print(result2)
```