# Claude Code

Claude Code 是由 Anthropic 公司开发的一款具有代理能力的智能编程工具（Agentic coding tool）

## 核心功能

1. 代码编辑与Bug修复：能够跨文件进行代码编辑，并自动修复代码中的错误
2. 代码理解与解答：可以快速回答关于代码架构和逻辑的疑问，帮助开发者提升代码理解效率
3. 测试与质量检查：支持自动执行测试、修复报错、进行代码质量检查，确保代码可靠性
4. Git 工作流处理：支持搜索 Git 历史记录、解决合并冲突、创建提交（commit）和 Pull Request，简化版本控制操作

## Claude Code安装

### 1.安装 Node.js 和 npm
- 确保您的系统已安装 `Node.js` 和 `npm`。可以通过命令 `node -v` 和 `npm -v` 检查版本。
- 如果未安装，前往 `Node.js`(https://nodejs.org/zh-cn) 官网 下载并安装。

### 全局安装 Claude Code CLI

1. 打开终端（Terminal），执行以下命令
```shell
npm install -g @anthropic-ai/claude-code
```

2. 安装完成后，可以通过 `claude --version` 验证是否安装成功


## CC GUI 插件安装

1. 确认 IntelliJ IDEA 版本， IntelliJ IDEA 版本为 2024.2 或更高版本
2. 安装 CC GUI 插件，`File → Settings → Plugins`，在 Marketplace 标签页中搜索“CC GUI”，点击Install
3. IDEA 右侧工具栏会出现 `CC GUI`

## CC GUI 插件配置

推荐使用本地 `settings.json`，路径如下

- macOS / Linux 系统: `~/.claude/settings.json`
- Windows 系统: `C:\Users\<用户名>\.claude\settings.json`


打开 CC GUI 面板，点击右上角的 ⚙️ 设置图标，选择“供应商管理”，然后选择“使用本地 settings.json”并授权

这里以接入GLM模型为例，修改对应的ANTHROPIC_AUTH_TOKEN

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "apiKey",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-4.7",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
  }
}
```

配置完成后，对话框输入请做个自我介绍，查看模型输出结果
