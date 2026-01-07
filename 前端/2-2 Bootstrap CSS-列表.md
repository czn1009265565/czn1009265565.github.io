# Bootstrap CSS-列表

## 基础列表样式

### 无序列表

```html
<ul>
  <li>列表项 1</li>
  <li>列表项 2</li>
</ul>
```

### 有序列表

```html
<ol>
    <li>第一项</li>
    <li>第二项</li>
</ol>
```

### 无样式列表

```html
<ul class="list-unstyled">
  <li>无样式项</li>
</ul>
```

### 内联列表
将列表项水平排列

```html
<ul class="list-inline">
  <li class="list-inline-item">首页</li>
  <li class="list-inline-item">产品</li>
</ul>
```

## 列表组

列表组是 Bootstrap 中常用的组件，用于显示一组项目（如菜单、内容块等）

### 基础列表组

```html
<ul class="list-group">
  <li class="list-group-item">项目一</li>
  <li class="list-group-item">项目二</li>
</ul>
```

### 激活状态与禁用状态

```html
<div class="list-group">
  <a href="#" class="list-group-item list-group-item-action active">激活项</a>
  <a href="#" class="list-group-item list-group-item-action disabled">禁用项</a>
</div>
```

### 颜色变体
使用 contextual classes 设置背景色：

```html
<ul class="list-group">
  <li class="list-group-item list-group-item-primary">主要项</li>
  <li class="list-group-item list-group-item-success">成功项</li>
</ul>
```

### 添加徽章

```html
<ul class="list-group">
  <li class="list-group-item">
      项目一
      <span class="badge bg-primary">新</span>
  </li>
  <li class="list-group-item">项目二</li>
</ul>
```

### 添加自定义内容

```html
<ul class="list-group">
    <li class="list-group-item">
        <h4 class="list-group-item-heading">
            项目一
        </h4>
        <p class="list-group-item-text">
            项目一介绍
        </p>
    </li>
    <li class="list-group-item">项目二</li>
</ul>
```