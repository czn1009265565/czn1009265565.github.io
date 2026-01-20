# Bootstrap CSS-颜色样式
Bootstrap 提供了丰富的颜色系统，包括背景色、文本色、边框色等

## 背景颜色 (Background Colors)
主题背景色
```html
<div class="bg-primary">主要背景 - 蓝色</div>
<div class="bg-secondary">次要背景 - 灰色</div>
<div class="bg-success">成功背景 - 绿色</div>
<div class="bg-danger">危险背景 - 红色</div>
<div class="bg-warning">警告背景 - 黄色</div>
<div class="bg-info">信息背景 - 浅蓝色</div>
<div class="bg-light">浅色背景 - 浅灰色</div>
<div class="bg-dark">深色背景 - 深灰色</div>
```

特殊背景色

```html
<div class="bg-white">白色背景</div>
<div class="bg-transparent">透明背景</div>
<div class="bg-body">主体背景 (默认页面背景)</div>
```

渐变背景色
```html
<div class="bg-primary bg-gradient">渐变主要背景</div>
<div class="bg-success bg-gradient">渐变成功背景</div>
```

## 文本颜色 (Text Colors)

主题文本色
```html
<p class="text-primary">主要文本 - 蓝色</p>
<p class="text-secondary">次要文本 - 灰色</p>
<p class="text-success">成功文本 - 绿色</p>
<p class="text-danger">危险文本 - 红色</p>
<p class="text-warning">警告文本 - 黄色</p>
<p class="text-info">信息文本 - 浅蓝色</p>
<p class="text-light bg-dark">浅色文本 (需深色背景)</p>
<p class="text-dark">深色文本 - 黑色</p>
```

其他文本色
```html
<p class="text-body">主体文本色 (默认)</p>
<p class="text-muted">减弱文本色</p>
<p class="text-white bg-dark">白色文本</p>
<p class="text-black-50">黑色50%透明度</p>
<p class="text-white-50 bg-dark">白色50%透明度</p>
```

## 边框颜色 (Border Colors)

```html
<!-- 边框颜色 -->
<div class="border border-primary">主要边框</div>
<div class="border border-success">成功边框</div>
<div class="border border-danger">危险边框</div>

<!-- 特定边边框 -->
<div class="border-top border-primary">上边框</div>
<div class="border-end border-success">右边框</div>
<div class="border-bottom border-warning">下边框</div>
<div class="border-start border-info">左边框</div>
```

## 按钮颜色 (Button Colors)

实心按钮
```html
<button class="btn btn-primary">主要按钮</button>
<button class="btn btn-secondary">次要按钮</button>
<button class="btn btn-success">成功按钮</button>
<button class="btn btn-danger">危险按钮</button>
<button class="btn btn-warning">警告按钮</button>
<button class="btn btn-info">信息按钮</button>
<button class="btn btn-light">浅色按钮</button>
<button class="btn btn-dark">深色按钮</button>
<button class="btn btn-link">链接按钮</button>
```

轮廓按钮
```html
<button class="btn btn-outline-primary">轮廓主要按钮</button>
<button class="btn btn-outline-success">轮廓成功按钮</button>
<button class="btn btn-outline-danger">轮廓危险按钮</button>
```

## 徽章颜色 (Badge Colors)
```html
<span class="badge bg-primary">主要徽章</span>
<span class="badge bg-secondary">次要徽章</span>
<span class="badge bg-success">成功徽章</span>
<span class="badge bg-danger">危险徽章</span>
<span class="badge bg-warning text-dark">警告徽章</span>
<span class="badge bg-info">信息徽章</span>
<span class="badge bg-light text-dark">浅色徽章</span>
<span class="badge bg-dark">深色徽章</span>
```

## 警示框颜色 (Alert Colors)

```html
<div class="alert alert-primary" role="alert">主要警示框</div>
<div class="alert alert-secondary" role="alert">次要警示框</div>
<div class="alert alert-success" role="alert">成功警示框</div>
<div class="alert alert-danger" role="alert">危险警示框</div>
<div class="alert alert-warning" role="alert">警告警示框</div>
<div class="alert alert-info" role="alert">信息警示框</div>
<div class="alert alert-light" role="alert">浅色警示框</div>
<div class="alert alert-dark" role="alert">深色警示框</div>
```

## 表格颜色 (Table Colors)

```html
<!-- 表格行颜色 -->
<tr class="table-primary">主要行</tr>
<tr class="table-success">成功行</tr>
<tr class="table-danger">危险行</tr>

<!-- 表格变体 -->
<table class="table table-primary">主要表格</table>
<table class="table table-dark">深色表格</table>
```

## 进度条颜色 (Progress Bar Colors)

```html
<div class="progress">
    <div class="progress-bar bg-success" style="width: 25%">25%</div>
</div>
<div class="progress">
    <div class="progress-bar bg-info" style="width: 50%">50%</div>
</div>
<div class="progress">
    <div class="progress-bar bg-warning" style="width: 75%">75%</div>
</div>
<div class="progress">
    <div class="progress-bar bg-danger" style="width: 100%">100%</div>
</div>
```

## 列表组颜色 (List Group Colors)

```html
<ul class="list-group">
    <li class="list-group-item list-group-item-primary">主要列表项</li>
    <li class="list-group-item list-group-item-success">成功列表项</li>
    <li class="list-group-item list-group-item-danger">危险列表项</li>
</ul>
```

