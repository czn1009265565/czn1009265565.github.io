# Bootstrap CSS

## 移动设备

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```
- initial-scale=1.0 确保网页加载时，以 1:1 的比例呈现，不会有任何的缩放
- user-scalable=no 可以禁用其缩放（zooming）功能，用户只能滚动屏幕，看上去更原生

## 响应式图像
响应式图像是指能够根据不同的屏幕尺寸、设备特性和网络条件自动调整大小、分辨率和格式的图像。

`img-responsive` 可以让 `Bootstrap` 中的图像对响应式布局的支持更友好
```html
<img src="..." class="img-responsive" alt="响应式图像">
```

## 容器
`container` 是一个核心的布局容器类，用于创建响应式、居中的固定宽度容器。

```html
<div class="container">

</div>
```

## 网格系统(重点)
一个基于 Flexbox 构建的响应式布局系统，用于快速创建灵活且适应不同屏幕尺寸的页面结构

### 网格系统的组成

网格系统由以下三个核心部分组成

1. 容器（Container）：使用 `.container` 或 `.container-fluid` 包裹内容，提供对齐和宽度约束
2. 行（Row）：使用 `.row` 类定义水平分组，包裹列（Column），并通过负边距抵消列的内边距（padding）
3. 列（Column）：使用 `.col-*` 类定义内容区域，是网格的最终布局单元


### 网格规则
1. 12 列系统：每行（Row）最多可划分为 12 列，通过分配不同比例的列类来控制布局
2. 响应式断点：根据屏幕尺寸使用不同的列类前缀

| 断点前缀      | 	屏幕尺寸       | 	描述         |
|-----------|-------------|-------------|
| .col-     | 	<576px（默认） | 	超小屏幕（手机竖屏） |
| .col-sm-  | 	≥576px     | 	小屏幕（手机横屏）  |
| .col-md-  | 	≥768px     | 	中等屏幕（平板）   |
| .col-lg-  | 	≥992px     | 	大屏幕（桌面）    |
| .col-xl-  | 	≥1200px    | 	超大屏幕（大桌面）  |
| .col-xxl- | 	≥1400px    | 	特大屏幕       |

### 基本用法
等宽列 自动分配宽度
```html
<div class="container">
    <div class="row">
        <div class="col">等宽列1</div>
        <div class="col">等宽列2</div>
    </div>
</div>
```

中等屏幕及以上4:8，小于中等屏幕时堆叠
```html
<div class="row">
    <!--  -->
    <div class="col-md-4">左侧内容</div>
    <div class="col-md-8">右侧内容</div>
</div>
```

混合断点 (小屏幕占 12 列（全宽），中等屏幕占 6 列)
```html
<div class="row">
    <div class="col-12 col-md-6">自适应列</div>
</div>
```

偏移列
```html
<div class="row">
    <div class="col-md-4 offset-md-4">居中显示</div>
</div>
```

嵌套网格
```html
<div class="row">
    <div class="col-md-6">
        <div class="row">
            <div class="col-6">内嵌列1</div>
            <div class="col-6">内嵌列2</div>
        </div>
    </div>
</div>
```