# Bootstrap CSS

## 移动设备

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```
- initial-scale=1.0 确保网页加载时，以 1:1 的比例呈现，不会有任何的缩放
- user-scalable=no 可以禁用其缩放（zooming）功能，用户只能滚动屏幕，看上去更原生

## 响应式图像
img-responsive 可以让 Bootstrap 中的图像对响应式布局的支持更友好
```html
<img src="..." class="img-responsive" alt="响应式图像">
```

## 导航栏
```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Logo</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Features</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

## 容器

```html
<div class="container">

</div>
```
### Echarts图表自适应

```html
<div id="chartContainer" class="container" style="width: 100%; height: 400px;"></div>
<script>
    // 初始化图表
    var chart = echarts.init(document.getElementById('chartContainer'));

    // 配置项
    var option = {
        title: { text: '月度销售额' },
        tooltip: {},
        xAxis: { data: ['1月', '2月', '3月', '4月', '5月'] },
        yAxis: {},
        series: [{
            name: '销售额',
            type: 'bar',
            data: [120, 200, 150, 80, 70]
        }]
    };
    // 渲染图表
    chart.setOption(option);
    // 监听窗口变化事件，触发 ECharts 自适应
    window.addEventListener('resize', function() {
        chart.resize();
    });
</script>
```

## 列表

### 有序列表

```html
<ol>
  <li>第一步</li>
  <li>第二步</li>
  <li>第三步</li>
</ol>
```

### 无序列表
```html
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
  <li>Item 4</li>
</ul>
```

### 水平列表
```html
<ul class="list-inline">
  <li class="list-inline-item">X坐标: 100</li>
  <li class="list-inline-item">Y坐标: 100</li>
  <li class="list-inline-item">Z坐标: 100</li>
</ul>
```

## 标题文本

```html
<h2>文本标题</h2>
<p class="text-left">向左对齐文本</p>
<p class="text-center">居中对齐文本</p>
<p class="text-right">向右对齐文本</p>
<p class="text-muted">本行内容是减弱的</p>
<p class="text-primary">本行内容带有一个 primary class</p>
<p class="text-success">本行内容带有一个 success class</p>
<p class="text-info">本行内容带有一个 info class</p>
<p class="text-warning">本行内容带有一个 warning class</p>
<p class="text-danger">本行内容带有一个 danger class</p>
```

## 表格

### 基础表格
```html
<table class="table">
    <thead>
    <tr>
        <th>ID</th>
        <th>姓名</th>
        <th>年龄</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>1</td>
        <td>张三</td>
        <td>25</td>
    </tr>
    <tr>
        <td>2</td>
        <td>李四</td>
        <td>30</td>
    </tr>
    </tbody>
</table>
```

### 响应式表格
```html
<div class="table-responsive">
  <table class="table">
    <!-- 宽表格内容 -->
  </table>
</div>
```

### 滚动条表格

```html
<div class="table-responsive" style="max-height: 300px; overflow-y: auto;">
  <table class="table">
    <!-- 长表格内容 -->
  </table>
</div>
```

### 按钮
```html
<p>
    <button type="button" class="btn btn-primary btn-lg">大的原始按钮</button>
    <button type="button" class="btn btn-default btn-lg">大的按钮</button>
</p>
<p>
    <button type="button" class="btn btn-primary">默认大小的原始按钮</button>
    <button type="button" class="btn btn-default">默认大小的按钮</button>
</p>
<p>
    <button type="button" class="btn btn-primary btn-sm">小的原始按钮</button>
    <button type="button" class="btn btn-default btn-sm">小的按钮</button>
</p>
<p>
    <button type="button" class="btn btn-primary btn-xs">特别小的原始按钮</button>
    <button type="button" class="btn btn-default btn-xs">特别小的按钮</button>
</p>
<p>
    <button type="button" class="btn btn-primary btn-lg btn-block">块级的原始按钮</button>
    <button type="button" class="btn btn-default btn-lg btn-block">块级的按钮</button>
</p>
```

