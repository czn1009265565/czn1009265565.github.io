# Agent Tool

Tools 是 Agent 可以调用的函数或工具，用于执行特定任务（如搜索、计算、文件操作等）。Agent 通过选择并调用合适的 Tool 来解决问题

## 常用内置工具

### 搜索查询类
- DuckDuckGoSearchRun	使用 DuckDuckGo 进行网络搜索
- WikipediaQueryRun	查询维基百科内容
- GoogleSearchRun	使用 Google 搜索（需 API 密钥）
- BingSearchRun 使用 Bing 搜索（需 API 密钥）

### 代码与计算类

- PythonREPLTool	执行 Python 代码
- Calculator	数学计算器
- HumanInputRun	请求人工输入（调试用）

### 数据与数据库类

- SQLDatabaseToolkit	数据库查询工具包
- JsonGetValueTool	从 JSON 中提取值
- JsonListKeysTool	列出 JSON 的键

### API 与网络类

- RequestsGetTool	发送 HTTP GET 请求
- RequestsPostTool	发送 HTTP POST 请求
- OpenAPIToolkit	OpenAPI 规范工具包

### 文件操作类
- FileReadTool	读取文件内容
- FileWriteTool	写入文件内容
- DirectoryListingTool	列出目录文件
- FileSearchTool	在文件中搜索文本

### 使用示例

```python
from langchain import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun, PythonREPLTool, ReadFileTool, WriteFileTool, RequestsGetTool
    
common_tools = [
    DuckDuckGoSearchRun(),
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    PythonREPLTool(),
    ReadFileTool(),
    WriteFileTool(),
]

# 查看工具信息
for tool in common_tools:
    print(f"🛠️ {tool.name}: {tool.description}")
```
## 自定义工具

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool, tool

class WeatherTool(BaseTool):
    name = "weather"
    description = "获取指定城市的天气信息"

    def _run(self, city: str) -> str:
        return f"{city}的天气：晴朗，25°C"

@tool
def get_stock_price(symbol: str) -> str:
    """获取股票价格"""
    import random
    price = round(random.uniform(100, 500), 2)
    return f"{symbol}的当前价格：${price}"

tools = [WeatherTool(), get_stock_price]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # 显示详细执行过程
    handle_parsing_errors=True  # 处理解析错误
)

result1 = agent.run("今天杭州的天气怎么样")
result2 = agent.run("微软的股票价格")
print(result1)
print(result2)
```
