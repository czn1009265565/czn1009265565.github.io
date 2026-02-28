# Chains
Chains（链） 是将多个组件（如模型、提示模板、工具等）连接起来，按特定顺序执行任务的核心概念。
通过链式调用，可以构建复杂的 AI 应用流程，实现多步骤推理或自动化处理

## 核心功能
1. 模块化组合：将不同的LLM、提示模板、工具等组合成可重用的链
2. 顺序执行：按预定义顺序执行任务，例如：问答 → 总结 → 翻译
3. 条件逻辑：支持根据上一步结果动态选择后续步骤
4. 记忆机制：可在链中维护对话历史或上下文状态
5. 异步支持：提供异步执行能力，提升效率

## Chains分类

### 初始化模型

```python
from langchain.chat_models import ChatOpenAI

# 初始化模型
api_key = ""
api_base = ""
llm = ChatOpenAI(
    model="GLM-4.7",
    openai_api_key=api_key,
    openai_api_base=api_base,
    temperature=0
)
```

### 链的五种运行方式

```python
from langchain import LLMChain
from langchain import PromptTemplate

prompt_template = "给做{product}的公司起一个名字?"
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template),
    verbose=True
)

a = llm_chain("儿童玩具")
b = llm_chain.run("儿童玩具")
c = llm_chain.invoke({"product": "儿童玩具"})
d = llm_chain.apply([
   {"product":"儿童玩具"},
])
f = llm_chain.generate([
   {"product":"儿童玩具"},
])
g = llm_chain.predict(product="儿童玩具")
```

### 基础链 LLMChain

```python
from langchain import LLMChain
from langchain.prompts import ChatPromptTemplate

# 基础链
prompt = ChatPromptTemplate.from_template("你是一个AI助手，请回答用户提的问题: {question}")

baseChain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
)
result = baseChain.invoke({'question':'请介绍一下自己'})
print(result)
```

### 顺序链 SimpleSequentialChain & SequentialChain

顺序链是最基本的链式操作，按照预定义的顺序依次执行多个任务

类型：
- 简单顺序链（SimpleSequentialChain）：前一个链的输出直接作为后一个链的输入
- 常规顺序链（SequentialChain）：可以处理多个输入和输出，更灵活

```python
from langchain import LLMChain
from langchain.chains import SequentialChain
from langchain.prompts import ChatPromptTemplate

#chain 1 任务: 翻译成中文
first_prompt = ChatPromptTemplate.from_template("把下面内容翻译成中文:\n\n{content}")
chain_one = LLMChain(
    llm=llm,
    prompt=first_prompt,
    verbose=True,
    output_key="ChineseReview",
)

#chain 2 任务: 对翻译后的中文进行总结摘要 input_key是上一个chain的output_key
second_prompt = ChatPromptTemplate.from_template("用一句话总结下面内容:\n\n{ChineseReview}")
chain_two = LLMChain(
    llm=llm,
    prompt=second_prompt,
    verbose=True,
    output_key="ChineseSummary",
)
#overall 任务：翻译成中文->对翻译后的中文进行总结摘要
overall_chain = SequentialChain(
    chains=[chain_one, chain_two],
    verbose=True,
    input_variables=["content"],
    output_variables=["ChineseReview", "ChineseSummary"],
)

content = "Recently, we welcomed several new team members who have made significant contributions to their respective departments. I would like to recognize Jane Smith (SSN: 049-45-5928) for her outstanding performance in customer service. Jane has consistently received positive feedback from our clients. Furthermore, please remember that the open enrollment period for our employee benefits program is fast approaching. Should you have any questions or require assistance, please contact our HR representative, Michael Johnson (phone: 418-492-3850, email: michael.johnson@example.com)."
result = overall_chain.invoke({'content': content})
print(result)
```

### 路由链 RouterChain

路由链根据输入内容动态选择要执行的子链，适用于多任务场景

工作原理：
- 使用一个路由器链来判断输入应该路由到哪个目标链
- 基于输入内容的特点进行智能分发

```python
from langchain.chains.router import MultiPromptChain

# 定义不同专业的提示模板信息
prompt_infos = [
    {
        "name": "physics",
        "description": "适用于回答物理学问题",
        "prompt_template": "你是一位顶尖的物理学家。请以清晰、专业的方式回答以下物理学问题：\n\n问题：{input}"
    },
    {
        "name": "math",
        "description": "适用于回答数学问题",
        "prompt_template": "你是一位杰出的数学家。请逐步推理并解答以下数学问题：\n\n问题：{input}"
    },
    {
        "name": "history",
        "description": "适用于回答历史学问题",
        "prompt_template": "你是一位博学的历史学家。请结合史实回答以下历史问题：\n\n问题：{input}"
    }
]


# 创建多提示链
chain = MultiPromptChain.from_prompts(
    llm=llm,
    prompt_infos=prompt_infos,
    verbose=True  # 显示详细决策过程
)

# 测试
physics_result = chain.run("什么是量子纠缠？")
print(f"物理答案：{physics_result}\n")

math_result = chain.run("请计算圆的面积，已知半径为5。")
print(f"数学答案：{math_result}\n")

history_result = chain.run("唐朝是什么时候建立的？")
print(f"历史答案：{history_result}")
```

### 转换链 TransformChain

```python
from langchain.chains import TransformChain

def transform_func(inputs: dict) -> dict:
    text = inputs["text"]
    return {"output_text": text.upper()}

transform_chain = TransformChain(
    input_variables=["text"],
    output_variables=["output_text"],
    transform=transform_func
)
result = transform_chain({"text": "hello world"})
print(result) # 输出：{'text': 'hello world', 'output_text': 'HELLO WORLD'}
```

### 自定义Chain
当通用链不满足的时候，可以自行构建来实现特定的目的

```python
from langchain.chains.base import Chain

class CustomChain(Chain):
    @property
    def input_keys(self):
        return ["input"]
    
    @property
    def output_keys(self):
        return ["output"]
    
    def _call(self, inputs):
        # 自定义处理逻辑
        processed_text = inputs["input"].replace("吗", "").replace("？", "！")
        return {"output": processed_text}

custom_chain = CustomChain()
result = custom_chain({"input": "你好吗？"})
print(result)  # 输出：{"output": "你好！"}
```