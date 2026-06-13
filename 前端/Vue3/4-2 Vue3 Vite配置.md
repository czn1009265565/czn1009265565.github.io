# Vue3 Vite配置

`vite.config.js` 是 Vite 项目的核心配置文件，位于项目根目录。
`Vite` 启动时会自动加载该文件，支持 `ESM / CJS / TypeScript` 三种格式:

- vite.config.js      # ESM (推荐)
- vite.config.mjs     # 强制 ESM
- vite.config.cjs     # CommonJS
- vite.config.ts      # TypeScript（内置支持，无需额外配置）

## 基本结构
vite.config.js

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// ✅ 推荐使用 defineConfig，提供完整的类型提示
export default defineConfig({
  // 配置项...
})

// 也支持函数式配置（可根据命令/模式动态返回）
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  return {
    // command: 'serve' | 'build'
    // mode: 'development' | 'production' | 自定义
  }
})
```

## 基础配置

| 配置项          | 	类型               | 	默认值                   | 	说明                   |
|--------------|-------------------|------------------------|-----------------------|
| root         | 	string           | 	process.cwd()         | 	项目根目录                |
| base         | 	string           | 	/                     | 	公共基础路径（部署子目录时使用）     |
| mode         | 	string           | 	serve=dev, build=prod | 	运行模式                 |
| publicDir    | 	string \|  false | 	public                | 	静态资源目录，构建时直接复制到 dist |
| cacheDir     | 	string           | 	node_modules/.vite    | 	预构建缓存目录              |
| clearScreen	 | boolean           | 	true                  | 	是否清屏                 |

```js
export default defineConfig({
  base: './',
  publicDir: 'static',       // 将 static/ 作为公共资源目录
  cacheDir: '.vite-cache',   // 自定义缓存位置
})
```

## 模块路径解析

import 时用别名 `@` 替代长路径
```js
import path from 'path'

export default defineConfig({
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
})
```

## 插件系统
Vite 的核心扩展机制，兼容 Rollup 插件接口

```js
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
        react(),
    ]
})
```

## 开发服务器

代理配置

```js
export default defineConfig({
    server: {
      port: 3000, // 指定端口号
      host: true, // 0.0.0.0 = true 允许局域网访问
      proxy: {
        // 简单代理
        '/api': {
          target: 'http://localhost:8080',
          changeOrigin: true,
        },
        // WebSocket 代理
        '/ws': {
          target: 'ws://localhost:8080',
          ws: true,
        }
      }
    }
});
```

### rewrite
前端请求路径和后端实际路径不一致时使用，修改代理转发时的请求路径

```
proxy: {
  '/api': {
    target: 'http://localhost:8080',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),
  },
}
```
转发过程: `/api/user/list` → `/user/list`