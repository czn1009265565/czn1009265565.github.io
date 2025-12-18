# Prompt模板

`Prompt` 模板是 `LangChain` 中用于管理和格式化提示词的核心组件，它允许你创建可重用的提示词结构，并通过变量插值动态生成具体的提示内容

## PromptTemplate
基础模板

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("你是一个有帮助的AI助手。请回答以下问题：问题：{question} 回答：")
prompt_format = prompt.format(question="什么是机器学习?")
print(prompt_format)
```

## ChatPromptTemplate
对话式提示词的模板类

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# 使用 from_messages
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}助手。"),
    ("human", "你好，我是{user_name}。"),
    ("ai", "你好{user_name}！很高兴为你服务。"),
    ("human", "{user_question}")
])
chat_prompt = chat_prompt_template.format(role="AI", user_name="Tom", user_question="什么是机器学习?")
print(chat_prompt)

# 使用 from_template（单条消息）
simple_prompt_template = ChatPromptTemplate.from_template("请回答：{question}")
simple_prompt = simple_prompt_template.format(question = "什么是机器学习?")
print(simple_prompt)
```

## 组合式提示词模板

```python
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate


# Final Prompt由一系列变量构成
full_template = """{character}
{behavior}
{prohibit}"""
full_prompt = PromptTemplate.from_template(full_template)

# 第一层基本性格设计
character_template = """你是{person}，你有着{personality}."""
character_prompt = PromptTemplate.from_template(character_template)

# 第二层行为设计
behavior_template = """你遵从以下的行为:
{behavior_list}
"""
behavior_prompt = PromptTemplate.from_template(behavior_template)

# 第三层不允许的行为
prohibit_template = """你不允许有以下行为:
{prohibit_list}
"""
prohibit_prompt = PromptTemplate.from_template(prohibit_template)

# 组合三层提示词
input_prompts = [
    ("character", character_prompt),
    ("behavior", behavior_prompt),
    ("prohibit", prohibit_prompt)
]
pipeline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=input_prompts)

prompt = pipeline_prompt.format(person="Tom", personality="乐于助人", behavior_list="积极向上",
                                       prohibit_list="涉毒")
print(prompt)
```

## 文件管理提示词模板

simple_prompt.json

```json
{
    "_type":"prompt",
    "input_variables":["industry","question"],
    "template":"你是一个擅长{industry}的AI助手。请回答以下问题：问题：{question}"
}
```

```python
from langchain.prompts import load_prompt

#加载json格式的prompt模版
prompt = load_prompt("simple.json")
print(prompt.format(industry="物理",question="什么是量子力学?"))
```