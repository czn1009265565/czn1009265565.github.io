# IDEA Vue环境配置

在 IDEA 中配置 Vue 3 开发环境，核心在于环境准备、插件安装、项目创建与相关配置

## 环境准备

确保系统已安装 Node.js（推荐使用 18.x 及以上的 LTS 版本，以匹配最新的工具链）
```shell
node -v
# v24.14.0

npm -v
# 11.9.0
```

## 启动Vue插件

1. File → Settings → Plugins
2. 搜索 Vue.js → 安装并 勾选启用


## 创建 Vue3项目

建议直接在 Terminal 终端命令窗口执行初始化命令即可

```shell
npm init vue@latest

cd <projectName>
npm install
npm run dev
```

## IDEA 核心配置

1. JavaScript / Vue 语言支持: Settings → Languages & Frameworks → JavaScript
2. TypeScript 配置: Settings → Languages & Frameworks → TypeScript
3. ESLint 集成: Settings → Languages & Frameworks → JavaScript → Code Quality Tools → ESLint
    - 选择: Automatic
    - 勾选: Run on save（推荐与 Prettier 冲突时优先 ESLint）
4. Prettier 集成: Settings → Languages & Frameworks → JavaScript → Prettier
    - 选择: Automatic
    - 这里不勾选 Run on save

## 运行调试配置

点击右上角 Add Configuration → + → npm
Name: Vite Dev
package.json: 选择对应路径下的 package.json 文件
Command: run
Scripts: dev