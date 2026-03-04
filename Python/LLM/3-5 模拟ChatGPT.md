# 模拟ChatGPT

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

# 初始化模型
api_key = ""
api_base = ""
llm = ChatOpenAI(
    model="Qwen3-Coder-Flash",
    openai_api_key=api_key,
    openai_api_base=api_base,
    temperature=0
)

template = """AI助手是由OpenAI训练的大型语言模型。

AI助手旨在能够处理各种任务，从回答简单问题到提供广泛话题的深入解释和讨论。作为一个语言模型，AI助手能够根据接收到的输入生成类似人类的文本，使其能够进行自然的对话并提供与当前话题相关且连贯的回答。

AI助手不断学习和改进，其能力不断发展。它能够处理和理解大量文本，并利用这些知识对各种问题提供准确和丰富的回答。此外，AI助手能够根据接收到的输入生成自己的文本，使其能够参与讨论并就各种话题提供解释和描述。

总的来说，AI助手是一个强大的工具，可以帮助处理各种任务，并就广泛话题提供有价值的见解和信息。无论您需要针对特定问题的帮助，还是只是想就某个特定话题进行交流，AI助手都在这里为您提供帮助。

{history}
Human: {human_input}
AI助手:"""

prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)


chatgpt_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

output = chatgpt_chain.predict(
    human_input="我要求你扮演Linux终端。我会输入命令，你将回复终端应显示的内容。我希望你只在一个唯一的代码块内回复终端输出，不添加其他内容。除非我指示你这样做，否则请不要输入命令。当我需要用英文告诉你一些信息时，我会用花括号{像这样}。我的第一个命令是pwd"

)
print(output)
```