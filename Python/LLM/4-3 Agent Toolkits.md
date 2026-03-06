# Agent Toolkits

Toolkits 是 LangChain 中预定义的工具集合，专门针对特定领域或平台提供了一组相关的工具。与单个 Tool 不同，Toolkit 提供了完整的解决方案。

特点:  
- 领域专精：针对特定平台或任务优化
- 工具组合：提供多个相关工具的集合
- 开箱即用：简化配置和使用流程
- 标准化接口：统一的调用方式


## 基本使用

使用SQLDatabaseChain构建的agent，用来根据数据库回答一般问题
```python
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 查看包含的工具
for tool in toolkit.get_tools():
    print(f"{tool.name}: {tool.description}")

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 自然语言描述数据库表
result1 = agent_executor.run("Describe the PlaylistTrack table")
print(result1)
result2 = agent_executor.run("Describe the Playlist table")
print(result2)
# 自然语言查询库表数据
result3 = agent_executor.run(
    "List the total sales per country. Which country's customers spent the most?"
)
print(result3)
```

## 自定义 Toolkits

```python

```