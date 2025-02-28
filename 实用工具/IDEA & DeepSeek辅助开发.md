# IDEA & DeepSeek辅助开发

## 背景

对于 Java 开发者而言，将 DeepSeek 集成到IDEA 中，就如同为自己的编程之路配备了一位智能助手，可以大幅提升开发效率。

## 前置环境

1. IDEA 版本2023.3以上
2. Python版本3.10

## 安装CodeGPT(Proxy AI)

File -> Settings -> Plugins -> MarketPlace

搜索 `Proxy AI` 后完成安装


## 账号配置

### 获取 API Key

公网账号: 登陆注册后访问deepseek开放平台 `https://platform.deepseek.com/usage`

内网账号: 

### IDEA Settings配置

File -> Settings -> Tools -> CodeGPT -> Providers -> Custom OpenAI

1. 设置个人API Key 
2. 修改Chat Completions
   1. 设置 URL 为 `https://api.deepseek.com/chat/completions`
   2. 修改 body 中的 model 为 `deepseek-chat`
3. 修改Code Completions
   1. 勾选 Enable code completions，开启代码补全
   2. 勾选 Parse response as Chat Completions
   3. FIM Template 选择 DeepSeek Coder
   4. 设置 URL 为 `https://api.deepseek.com/chat/completions`
   5. 修改 body 中的 model 为 `deepseek-reasoner`
4. 修改Prompts回答语言为中文

## 插件使用

1. 代码补全
2. 代码修改

   选择要修改的代码块后点击 `Proxy AI` 图标即可出现输入框，输入修改要求，回车等待代码生成，如果生成符合要求点击 `Accept Suggestion` 即可保存生成建议，
按esc 或关闭代码编辑弹窗，即可回撤生成的代码。
3. 对话模式
4. 代码优化

   选中代码后右键→CodeGPT 即可使用 bug 查找、代码优化、代码重构、编写测试用例等功能。