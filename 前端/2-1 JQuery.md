# JQuery

jQuery 是一个快速、简洁的 JavaScript 库，简化了 HTML 文档遍历、事件处理、动画和 Ajax 交互

```html
<!-- 使用 CDN -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<!-- 或下载本地文件 -->
<script src="/static/js/jquery-3.6.0.min.js"></script>
```
## 文档就绪函数

```javascript
$(document).ready(function() {
    // 代码在这里执行
});

// 简写方式
$(function() {
    // 代码在这里执行
});
```

## DOM操作

### 选择器

```javascript
// ID 选择器
$("#myId")

// 类选择器
$(".myClass")

// 元素选择器
$("div")

// 属性选择器
$("input[name='email']")

// 复合选择器
$("div.myClass, p#myId")
```

遍历操作
```javascript
// each() 方法
$("li").each(function(index) {
    console.log(index + ": " + $(this).text());
});

// 查找子元素
$("#parent").find(".child");

// 父元素
$(".child").parent();

// 兄弟元素
$("#element").siblings();

// 下一个元素
$("#element").next();

// 上一个元素
$("#element").prev();
```

### 获取和设置内容

```javascript
// 获取文本内容
var text = $("#element").text();

// 设置文本内容
$("#element").text("新内容");

// 获取 HTML 内容
var html = $("#element").html();

// 设置 HTML 内容
$("#element").html("<p>新段落</p>");

// 获取和设置值
var value = $("#input").val();
$("#input").val("新值");

// 追加子元素
$("#parent").append('<div>新的子元素</div>')
```

### 属性操作

```javascript
// 获取属性
var src = $("img").attr("src");

// 设置属性
$("img").attr("src", "new-image.jpg");

// 设置多个属性
$("img").attr({
    "src": "new-image.jpg",
    "alt": "描述文字"
});

// 移除属性
$("img").removeAttr("alt");
```

### CSS 操作

```javascript
// 获取 CSS 属性
var color = $("#element").css("color");

// 设置 CSS 属性
$("#element").css("color", "red");

// 设置多个 CSS 属性
$("#element").css({
    "color": "red",
    "font-size": "16px",
    "background-color": "#f0f0f0"
});
```

## 事件处理

```javascript
// 鼠标左键点击事件
$("#button").click(function() {
    alert("按钮被点击了！");
});

// 鼠标右键点击事件
$("#element").on("contextmenu", function(event) {
    event.preventDefault(); // 阻止浏览器默认右键菜单
    console.log("右键点击事件触发");
    console.log("点击位置: X=" + event.clientX + ", Y=" + event.clientY);

    // 显示自定义右键菜单
    $("#customMenu")
        .css({
            left: event.pageX + "px",
            top: event.pageY + "px"
        })
        .show();
});

// 鼠标悬停
$("#element").hover(
    function() {
        $(this).css("background-color", "yellow");
    },
    function() {
        $(this).css("background-color", "white");
    }
);

// 键盘事件
$("#input").keypress(function(event) {
    console.log("按键代码: " + event.which);
});

// 表单事件
$("#form").submit(function(event) {
    event.preventDefault(); // 阻止表单提交
    // 处理表单数据
});

// 文档加载完成
$(window).on("load", function() {
    console.log("所有资源加载完成");
});
```

事件委托
```javascript
// 为动态添加的元素绑定事件
$("#container").on("click", ".dynamic-element", function() {
    // 处理点击事件
});
```

## AJAX请求

GET请求
```javascript
$.get("/users", function(response, status) {
    console.log("数据: " + response + "\n状态: " + status);
});

// 带参数
$.get("/users", {name: "John", age: 30}, function(response) {
    console.log(response)
});
```

POST请求
```javascript
$.post("/users", 
    {name: "John", age: 30}, 
    function(response) {
        console.log(response);
    }
);
```