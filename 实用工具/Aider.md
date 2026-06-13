# Aider

Aider 是目前开源社区中最受推崇的 终端原生 AI 结对编程工具

核心功能:
1. 直接文件操作
2. 完整的代码库上下文感知
3. 与 Git 无缝集成
4. 支持主流及本地模型
5. 聊天与编辑模式

## 安装部署

```shell
pip install pipx
pipx ensurepath
pipx install aider-chat
```

验证安装
```shell
aider --version
```

## 配置自部署模型

在项目根目录创建 `.aider.conf.yml`

### OpenAI 兼容 API

```yaml
model: openai/EB-Qwen3.6-Plus
openai-api-base: http://your-server-ip:8000/v1
openai-api-key: sk-your-private-key

# 💡 指定弱模型处理简单任务，大幅降低 Token 消耗
weak-model: openai/qwen2.5-coder-7b-instruct
```

### Ollama 本地原生模型

```yaml
model: ollama/qwen2.5-coder:32b-instruct
```

## IDEA 使用

Aider 是终端原生工具，不需要安装任何 IDEA 插件，直接在 IDE 内置终端操作体验最佳

1. 打开 IDEA 底部的 Terminal 面板
2. cd 到你的项目根目录
3. 输入 aider 回车
4. 等待 Repo Map（仓库地图）构建完成，出现 > 提示符即代表就绪


## 核心工作流与高频命令

Aider 的核心逻辑是: 自然语言对话 → 自动定位文件 → 应用 Diff → 自动 Git Commit

### 多文件编辑

直接描述需求，Aider 会自动寻找相关文件并修改

```shell
> 基于user.sql文件，生成对应的实体类，Dao，Mapper文件
```

### 只读问答模式
只想问问题、梳理逻辑，防止误改代码时，需要添加前缀 `/ask`

```shell
> /ask 介绍下该项目
```

### 手动管理上下文

当项目太大，Aider 找错文件或遗漏文件时

```shell
/add backend                           # 添加整个目录
/add pom.xml                           # 添加单文件
/drop README.md                        # 移除无关文件
/ls                                    # 查看当前已加载的上下文文件
/map                                   # 查看 Repo Map 结构
```

### 回滚

一键撤销上一次修改，注意该项目必须是Git项目

```shell
/undo
```