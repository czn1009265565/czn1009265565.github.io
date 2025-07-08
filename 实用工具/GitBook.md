# GitBook

## 简介

GitBook是一款基于Node.js的命令行工具，它为用户提供了一个利用Github、Git以及Markdown语法来创建高质量电子书的平台。
不同于一个关于Git的教程，GitBook专注于简化电子书的编写与发布流程，使得作者能够更加专注于内容创作本身。

## 安装部署

### 安装 Node
由于 `gitbook-cli` 已经停止维护了,因此我们需要下载停止维护前的Nodejs版本 `v10.23.0`

1. 下载Node.js<br>
   ```https://nodejs.org/download/release/v10.23.0/node-v10.23.0-x64.msi```
2. 安装执行
3. 验证是否安装成功，查看对应版本信息<br>
   ```shell
   node -v
   npm -v
   ```

### 安装 gitbook-cli

命令行安装<br>
```shell
npm install -g gitbook-cli
```

若下载速度过慢则可以设置代理  
```shell
# 设置代理
npm config set proxy=http://127.0.0.1:10809
# 取消代理
npm config delete proxy
```

## 创建电子书

### 初始化文件  
执行初始化命令
```shell
gitbook init
```
执行成功会产生两个文件，目录：`SUMMARY.md`，第一篇文章：`README.md`

### 启动服务
启动服务命令
```shell
gitbook serve
```
浏览器访问 `http://localhost:4000`电子书

### 目录格式

```markdown
# Summary

* [Introduction](README.md)
* [Python](Python/README.md)
   * [Python 环境搭建](Python/Python 环境搭建.md)
* [Java](Java/README.md)
   * [Java高并发核心编程](Java/Java高并发核心编程.md)
```

但是目前目录是不支持折叠的，一旦目录过多，平铺的形式并不友好。

让我们新增插件支持目录折叠

1. 在电子书根目录创建一个 `book.json` 文件，内容如下
   ```json
   {
   "plugins":["toggle-chapters"]
   }
   ```
2. 执行 `gitbook install`安装插件
3. 重启服务 `gitbook serve`

至此，我们可以在局域网下访问我们的电子书籍（博客网站），那如果想要在公网下也支持访问呢，
那么其实有多种方案

1. 租用云服务商服务器,自行搭建，并配置域名(操作复杂，需要一定的前后端知识储备，付费)
2. ZeroTier 内网穿透方案 (需要一台闲置服务器，免费)
3. GitHub Pages (配置简单，免费)

## GitHub Pages
GitHub Pages 是一项静态站点托管服务，它直接从 GitHub 上的仓库获取 HTML、CSS 和 JavaScript 文件，（可选）通过构建过程运行文件，然后发布网站。
可以在 GitHub Pages 示例集合中看到 GitHub Pages 站点的示例。

### 新建项目
1. GitHub 创建 `<username>.github.io`项目
2. 拉取项目 `git clone <项目地址>`

### 构建书籍

1. 使用 `gitbook build` 将书籍内容输出到默认目录，也就是当前目录下的 `_book` 目录。
2. 创建 gh-pages 分支 `git checkout -b gh-pages`<br>
   这样 `master` 分支就是书籍源代码，`gh-pages` 分支就是生成后的Html文件
3. 删除除 `_book` 以外所有文件
4. 将 `_book`下的文件放在根目录下
5. 提交代码
6. 设置GitHub Pages site分支为`gh-pages`
7. 访问 `http://<username>.github.io`查看书籍