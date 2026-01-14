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

### 图片+文字

```html
<div class="list-group">
    <div class="list-group-item">
        <div class="row align-items-center">
            <!-- 图片 -->
            <div class="col-auto">
                <img src="https://picsum.photos/150/120?random=1" style="width: 50px; height: 50px;" alt="产品图片">
            </div>
            <!-- 名称 -->
            <div class="col">
                <span class="fw-bold">产品名称</span>
            </div>
            <!-- 价格 -->
            <div class="col-auto">
                <span class="text-danger fw-bold">¥99.00</span>
            </div>
        </div>
    </div>
</div>
```

- `align-items-center`: 垂直居中对齐
- `col`: 自适应宽度，让列自动占据父容器中剩余的可用空间，并与其他 col 列均分宽度
- `col-auto`: 根据内容自动调整宽度

左侧图片宽度由图片自身决定，中间的"产品名称"列使用 `col`，会占据所有剩余可用空间，右侧的价格宽度也由自身决定。
由于中间列填充了所有剩余空间，将右侧的价格列"推"到了容器的最右边。

### 支持滚动下拉

```html
<ul class="list-group" style="max-height: 50vh; overflow-y: auto;">
  <li class="list-group-item">项目一</li>
  <li class="list-group-item">项目二</li>
</ul>
```
- `max-height: 50vh;`: 设置元素的最大高度限制为视口高度的 50%
- `overflow-y: auto;`: 垂直方向超过最大高度时，自动显示滚动条
