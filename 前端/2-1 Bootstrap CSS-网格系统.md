# Bootstrap CSS-网格系统

Bootstrap 的网格系统是其最强大的功能之一，提供了一个灵活、响应式的布局解决方案

### 网格系统的组成

网格系统由以下三个核心部分组成

1. 容器（Container）：使用 `.container` 固定宽度容器 或者`.container-fluid` 全宽容器
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

- `col`: 自适应宽度，让列自动占据父容器中剩余的可用空间，并与其他 col 列均分宽度
- `col-auto`: 根据内容自动调整宽度，`col-auto` 的宽度由其内部内容决定，不会均分剩余空间

### 基本用法
1. 等宽列 自动分配宽度
```html
<div class="container">
    <div class="row">
        <div class="col">等宽列1</div>
        <div class="col">等宽列2</div>
    </div>
</div>
```

2. 中等屏幕及以上4:8，小于中等屏幕时堆叠
```html
<div class="row">
    <!--  -->
    <div class="col-md-4">左侧内容</div>
    <div class="col-md-8">右侧内容</div>
</div>
```

3. 混合断点 (小屏幕占 12 列（全宽），中等屏幕占 6 列)
```html
<div class="row">
    <div class="col-12 col-md-6">自适应列</div>
</div>
```

4. 偏移列
```html
<div class="row">
    <div class="col-md-4 offset-md-4">居中显示</div>
</div>
```

5. 嵌套网格
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
禁止直接嵌套 row，需通过 col 内再嵌套 row 实现多层布局