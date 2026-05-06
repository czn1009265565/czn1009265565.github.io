# Agent

## 概述
在 LangChain 中，Agent 是一个能够自主思考、调用工具来完成任务的智能体。
它不像普通的 Chain 那样固定执行流程，而是根据用户输入动态决定要执行什么动作（如调用哪个工具、是否需要多次调用等）

## 工作流程

工作流程分为输入解析、思考决策、工具执行、结果迭代四个核心阶段

### 一、初始输入: 用户问题接收与预处理

- 原始输入解析: 接收用户的自然语言问题，提取任务目标、约束条件等关键信息，作为后续处理的基础
- 上下文加载: 调用记忆模块，读取历史对话记录，理解用户的提问背景，避免重复提问

### 二、思考循环: 智能决策与工具选择

- 初步推理: 将用户输入传递给大语言模型（LLM），判断问题类型: 若问题可直接通过知识库回答，则跳过工具调用，直接生成回答；若需要外部数据或计算，则进入工具选择环节。
- 工具匹配: LLM 根据任务需求，从工具库中筛选合适的工具，确定调用参数与执行顺序。例如查询天气时匹配 API 工具，复杂计算时调用计算器工具。
- 执行校验: 通过 AgentExecutor 组件检查工具调用的合理性，判断是否满足停止条件，避免陷入无限循环

### 三、工具调用: 外部交互与结果返回

- 动作执行: 向选中的工具传入参数，触发具体操作，如发送 API 请求、运行代码片段、查询数据库信息。
- 结果观察: 收集工具返回的结构化结果，例如天气数据、计算数值、网页内容，进行格式标准化处理，转换为模型可理解的文本格式。

### 四、结果生成: 迭代优化与最终输出

- 多轮循环: 将工具返回结果重新输入 LLM，判断是否需要继续调用工具补充信息，比如根据天气结果再次调用行程规划工具，直到获取足够信息。
- 回答生成: LLM 整合所有结果，转换为自然语言回答，通过 AgentOutputs 返回给用户。

### 核心组件

- LLM（大语言模型）: 负责推理和决策
- Tools（工具集）: Agent 可以调用的外部功能（如计算器、搜索引擎、API 等）
- Agent Executor: 运行 Agent 的引擎，负责调度工具调用和解析 LLM 输出


### 工作原理

1. 接收用户输入（如: “计算 3 的 5 次方是多少？”）
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