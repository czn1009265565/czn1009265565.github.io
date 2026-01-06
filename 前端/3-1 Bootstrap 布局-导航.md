# Bootstrap 导航

导航包括导航栏和导航元素。
- 导航栏是整个导航系统的外层容器，提供完整的导航头部布局。
- 导航元素是导航栏内部的链接容器，专门用于组织导航菜单项。

导航栏提供结构和布局，导航元素提供具体的导航功能

## 导航栏

基本导航栏结构

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="#">菜鸟教程</a>
        </div>
        
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" href="#">首页</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">个人资料</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">消息</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

导航栏基础类：
- `.navbar` - 定义导航栏容器
- `.navbar-expand-{breakpoint}` - 响应式断点（lg, md, sm, xl）
- `.navbar-light/.navbar-dark` - 颜色主题
- `.bg-{color}` - 背景颜色


导航元素类：
- `.navbar-brand` - 品牌/网站名称
- `.navbar-nav` - 导航链接容器
- `.nav-item` - 导航项
- `.nav-link` - 导航链接
- `.active` - 当前激活状态


## 导航元素

### 标签式导航

```html
<ul class="nav nav-tabs">
    <li class="nav-item">
        <a class="nav-link active" href="#">首页</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">个人资料</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">消息</a>
    </li>
</ul>
```

### 胶囊式导航

```html
<ul class="nav nav-pills">
  <li class="nav-item">
    <a class="nav-link active" href="#">首页</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">个人资料</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">消息</a>
  </li>
</ul>
```

### 下拉菜单导航

```html
<ul class="nav nav-tabs">
  <li class="nav-item">
    <a class="nav-link active" href="#">首页</a>
  </li>
  <li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#">
      更多选项
    </a>
    <ul class="dropdown-menu">
      <li><a class="dropdown-item" href="#">设置</a></li>
      <li><a class="dropdown-item" href="#">帮助</a></li>
    </ul>
  </li>
</ul>
```

### 垂直标签导航

```html
<ul class="nav nav-tabs flex-column">
    <li class="nav-item">
        <a class="nav-link active" href="#">首页</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">个人资料</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">消息</a>
    </li>
</ul>
```

- `.flex-column` - 垂直排列