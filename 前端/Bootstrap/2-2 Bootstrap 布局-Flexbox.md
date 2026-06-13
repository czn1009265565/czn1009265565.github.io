# Bootstrap 布局-Flexbox
Flexbox（弹性盒子布局）是一种一维布局模型，用于在单项中排列元素，可以水平或垂直排列。

网格系统通常作为外层容器，Flexbox 则用于组件内部排列、对齐控制。

## 基本结构

```html
<div class="d-flex">水平排列的 Flex 容器</div>
```

水平排列（默认）
```html
<div class="d-flex flex-row">
  <div>项目1</div>
  <div>项目2</div>
</div>
```

垂直排列
```html
<div class="d-flex flex-column">
  <div>项目1</div>
  <div>项目2</div>
</div>
```

## 对齐控制
### 水平对齐

- 左对齐
```html
<div class="d-flex justify-content-start">
  <div>左对齐项目</div>
</div>
```

- 居中对齐
```html
<div class="d-flex justify-content-center">
  <div>水平居中项目</div>
</div>
```

- 右对齐
```html
<div class="d-flex justify-content-end">
  <div>右对齐项目</div>
</div>
```

- 两侧对齐
```html
<div class="d-flex justify-content-between">
    <div>左项目</div>
    <div>右项目</div>
</div>
```

- 均匀分布
```html
<div class="d-flex justify-content-around">
  <div>项目1</div>
  <div>项目2</div>
  <div>项目3</div>
</div>
```

### 垂直对齐

- 顶部对齐
```html
<div class="d-flex align-items-start">
  <div>顶部对齐</div>
</div>
```

- 垂直居中
```html
<div class="d-flex align-items-center">
    <div>垂直居中</div>
</div>
```

- 底部对齐
```html
<div class="d-flex align-items-end">
  <div>底部对齐</div>
</div>
```

### 组合对齐
- 完全居中(水平+垂直)
```html
<div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
  <div>完全居中内容</div>
</div>
```

- 左上角
```html
<div class="d-flex justify-content-start align-items-start">
  <div>左上角对齐</div>
</div>
```
- 右上角
```html
<div class="d-flex justify-content-end align-items-start">
  <div>右上角对齐</div>
</div>
```

- 左下角
```html
<div class="d-flex justify-content-start align-items-end">
  <div>左下角对齐</div>
</div>
```

- 右下角
```html
<div class="d-flex justify-content-end align-items-end">
  <div>右下角对齐</div>
</div>
```
- 水平居中 + 顶部对齐
```html
<div class="d-flex justify-content-center align-items-start">
  <div>水平居中顶部对齐</div>
</div>
```

- 水平居中 + 底部对齐
```html
<div class="d-flex justify-content-center align-items-end">
  <div>水平居中底部对齐</div>
</div>
```

## 间距控制
基本语法结构 `{属性}{边距方向}-{尺寸}`

### 外边距
- m - 所有四个边
- mt - 上边距 (margin-top)
- mb - 下边距 (margin-bottom)
- ms - 起始边距 (margin-start，LTR布局中是左边距)
- me - 结束边距 (margin-end，LTR布局中是右边距)
- mx - 水平方向（左右边距）
- my - 垂直方向（上下边距）

### 内边距
- p - 所有四个边
- pt - 上内边距 (padding-top)
- pb - 下内边距 (padding-bottom)
- ps - 起始内边距 (padding-start)
- pe - 结束内边距 (padding-end)
- px - 水平方向（左右内边距）
- py - 垂直方向（上下内边距）

### 尺寸数值

- 0 - 0rem (0px)
- 1 - 0.25rem (4px)
- 2 - 0.5rem (8px)
- 3 - 1rem (16px)
- 4 - 1.5rem (24px)
- 5 - 3rem (48px)
- auto - 自动间距

### 水平自动间距

```html
<!-- 左推（元素靠右），右对齐的效果 -->
<div class="d-flex">
    <div class="ms-auto">右侧内容</div>
</div>

<!-- 右推（元素靠左） -->
<div class="d-flex">
    <div class="me-auto">左侧内容</div>
    <div>右侧固定内容</div>
</div>

<!-- 两侧推（中间居中） -->
<div class="d-flex">
    <div class="me-auto">左侧</div>
    <div>中间</div>
    <div class="ms-auto">右侧</div>
</div>
```

### 垂直自动间距

```html
<!-- 顶部推（元素在底部） -->
<div class="d-flex flex-column" style="height: 200px;">
  <div class="mt-auto">底部内容</div>
</div>

<!-- 底部推（元素在顶部） -->
<div class="d-flex flex-column" style="height: 200px;">
  <div class="mb-auto">顶部内容</div>
  <div>其他内容</div>
</div>
```

### 实例

列表底部文字

```html
<div class="container">
    <div class="d-flex flex-column" style="height: 50vh;">

        <!-- 列表区域（可滚动） -->
        <ul class="list-group flex-grow-1" style="overflow-y: auto;">
            <li class="list-group-item">项目一</li>
            <li class="list-group-item">项目二</li>
            <li class="list-group-item">项目三</li>
            <li class="list-group-item">项目四</li>
            <li class="list-group-item">项目五</li>
        </ul>

        <!-- 底部固定文字 -->
        <div class="mt-auto">
            <div class="d-flex justify-content-center">
                <small>共5个项目</small>
            </div>
        </div>
    </div>
</div>
```