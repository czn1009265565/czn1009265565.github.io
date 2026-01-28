## Spring Boot Thymeleaf

`Thymeleaf` 是一个流行的Java模板引擎，提供了丰富的功能和简洁的语法，使开发者能够轻松地创建动态Web页面。

前端推荐 `Bootstrap 5` + `jQuery`

## Spring Boot 集成

### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

### application配置

```yaml
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
    encoding: UTF-8
    mode: HTML5
    cache: false
  mvc:
    # 静态文件路径配置
    static-path-pattern: /static/**
```

### 创建模板文件
在src/main/resources/templates目录下创建Thymeleaf模板文件

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Thymeleaf Example</title>
</head>
<body>
<h1>Welcome to Thymeleaf</h1>
<p th:text="${message}">This is a placeholder text</p>
</body>
</html>
```

### 创建Controller
创建一个Controller来处理请求并返回模板视图，这里支持两种写法

```java
@Controller
public class IndexController {
    @GetMapping("/index")
    public String index(Model model) {
        model.addAttribute("message", "Hello, Thymeleaf!");
        // 返回模板名称，对应templates目录下的index.html
        return "index";
    }

    @GetMapping("/index2")
    public ModelAndView index2() {
        ModelAndView modelAndView = new ModelAndView("index");
        modelAndView.addObject("message", "Hello, Thymeleaf!");
        return modelAndView;
    }
}
```

## Thymeleaf 标签

### 静态文件引用

```html
<!-- 引用CSS -->
<link rel="stylesheet" th:href="@{/static/css/style.css}" />
 
<!-- 引用JavaScript -->
<script th:src="@{/static/js/script.js}"></script>

<!-- 引用图片 -->
<img th:src="@{/static/images/logo.png}" alt="Logo" />
```

### 变量表达式

```html
<!-- 直接引用变量 -->
<p th:text="${name}"></p>

<!-- 调用对象的方法 -->
<p th:text="${user.getName()}"></p>

<!-- 访问对象的属性 -->
<p th:text="${user.age}"></p>

<!-- 使用默认值 -->
<p th:text="${name} ?: 'default value'"></p>

<!-- 使用三目运算符 -->
<p th:text="${user.isAdmin() ? 'Admin' : 'User'}"></p>
```

### 迭代器

```html
<!-- 迭代集合 -->
<ul>
  <li th:each="item : ${items}" th:text="${item}"></li>
</ul>

<!-- 迭代数组 -->
<ul>
  <li th:each="item : ${#arrays.asList(array)}" th:text="${item}"></li>
</ul>

<!-- 迭代数字范围 -->
<ul>
  <li th:each="i : ${#numbers.sequence(1, 5)}" th:text="${i}"></li>
</ul>
```

### 条件语句

```html
<!-- if语句 -->
<p th:if="${isAdmin}">Welcome, Admin!</p>
<p th:unless="${isAdmin}">Welcome, User!</p>

<!-- switch语句 -->
<div th:switch="${dayOfWeek}">
  <p th:case="'MONDAY'">Monday</p>
  <p th:case="'TUESDAY'">Tuesday</p>
  <p th:case="'WEDNESDAY'">Wednesday</p>
  <p th:case="'THURSDAY'">Thursday</p>
  <p th:case="'FRIDAY'">Friday</p>
  <p th:case="'SATURDAY'">Saturday</p>
  <p th:case="'SUNDAY'">Sunday</p>
  <p th:case="*">Invalid Day</p>
</div>
```

### 模板片段

在 `Thymeleaf` 模板文件中，可以使用 `th:fragment` 属性来定义一段公共的代码片段，然后使用 `th:insert` 属性将模板片段引入。

| 语法                           | 	描述                                               |
|------------------------------|---------------------------------------------------|
| ~{templatename}	             | 引用整个模板文件的代码片段                                     |
| ~{templatename :: selector}	 | selector 可以是 th:fragment 指定的名称或其他选择器，如类选择器、ID选择器等 |
| ~{::selector}	               | 相当于 ~{this :: selector}，表示引用当前模板定义的代码片段           |


#### 定义片段
新建 `src\main\resources\templates\fragments\header.html`
```html
<!-- 定义片段 -->
<div th:fragment="header">
    <h1>Header</h1>
</div>
```

#### 引入片段
在 `src\main\resources\templates\index.html` 中引入片段
```html
<!-- 插入片段 -->
<div th:insert="~{fragments/header :: header}"></div>
<!-- 替换片段 -->
<div th:replace="~{fragments/header :: header}"></div>
```

### 属性设置

```html
<p th:value="placeholder">设置特定的标签属性</p>
<p th:attr="class='text'">attr设置任意属性</p>
```