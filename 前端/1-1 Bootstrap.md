# Bootstrap
Bootstrap 是一个开源的前端框架，由 Twitter 团队开发并维护，用于快速构建响应式、移动优先的网站和 Web 应用。
它提供了一套预定义的 HTML、CSS 和 JavaScript 组件及工具，显著简化了前端开发流程。

特点:

1. 响应式设计：自动适配不同设备（PC、平板、手机）。
2. 组件丰富：提供导航栏、按钮、表单、卡片等现成组件。
3. 网格系统：基于 12 列的灵活布局系统，支持多屏幕尺寸。
4. 预定义样式：内置颜色、间距、字体等标准化设计。
5. 跨浏览器兼容：支持主流浏览器（Chrome、Firefox、Edge 等）

## 环境安装

### 官方下载方式
访问 Bootstrap 官方网站 `http://getbootstrap.com/` 获取指定版本

下载后文件目录结构
```
bootstrap/
├── css/
│   ├── bootstrap.css
│   ├── bootstrap.css.map
│   ├── bootstrap.min.css
│   └── bootstrap.min.css.map
├── js/
│   ├── bootstrap.bundle.js
│   ├── bootstrap.bundle.js.map
│   ├── bootstrap.bundle.min.js
│   ├── bootstrap.bundle.min.js.map
│   ├── bootstrap.js
│   ├── bootstrap.js.map
│   ├── bootstrap.min.js
│   └── bootstrap.min.js.map
```

### CDN 引入
国内推荐使用 `https://www.staticfile.net/`
国际推荐使用 `https://cdnjs.com/`
```html
<!-- CSS only -->
<link href="https://cdn.staticfile.net/bootstrap/5.3.2/css/bootstrap.min.css" rel="stylesheet">

<!-- JavaScript Bundle with Popper -->
<script src="https://cdn.staticfile.net/bootstrap/5.3.2/js/bootstrap.bundle.min.js"></script>
```

### 模板
```html
<!DOCTYPE html>
<html>
<head>
    <title>Bootstrap 模板</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <!-- CSS only -->
    <link href="https://cdn.staticfile.net/bootstrap/5.3.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- JavaScript Bundle with Popper -->
    <script src="https://cdn.staticfile.net/bootstrap/5.3.2/js/bootstrap.bundle.min.js"></script>
</head>
<body>
<h1>Hello, world!</h1>
</body>
</html>
```

- initial-scale=1.0 确保网页加载时，以 1:1 的比例呈现，不会有任何的缩放
- user-scalable=no 可以禁用其缩放（zooming）功能，用户只能滚动屏幕，看上去更原生