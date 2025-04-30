## Spring Boot Thymeleaf Echarts

在如今的数据可视化时代，统计图对于直观呈现数据趋势、分布等信息至关重要。
Spring Boot 作为主流的 Java 后端框架，结合强大的前端可视化库 Echarts，能轻松打造出专业且炫酷的数据展示页面。

### 环境准备

从 Echarts 官网 `https://echarts.apache.org/zh/download.html`
下载编译后的 `echarts.js` 文件，放入 Spring Boot 项目的 `resources/static/js` 目录下，后续在 `HTML` 页面中直接引用。

从 JQuery 官网 `https://jquery.com/download/`
下载对应版本的 `https://code.jquery.com/jquery-3.6.0.min.js` 文件，这里以3.6.0版本为例，
放入 Spring Boot 项目的 `resources/static/js` 目录下。

### 后端数据准备

```java
@RestController
@RequestMapping("/api")
public class DataControllerApi {
    @GetMapping("/data")
    public List<Map> getData() {
        return List.of(
                Map.of("productName", "产品A", "productPrice", 100),
                Map.of("productName", "产品B", "productPrice", 150),
                Map.of("productName", "产品C", "productPrice", 80)
        );
    }
}
```

### 前端页面搭建

在resources/templates目录下创建index.html

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Echarts in Spring Boot</title>
    <!-- 引入js依赖文件 -->
    <script th:src="@{/static/js/echarts.js}"></script>
    <script th:src="@{/static/js/jquery-3.6.0.min.js}"></script>
</head>
<body>
<div id="chartContainer" style="width: 600px;height:400px;"></div>
<script>
    // Echarts初始化与数据加载逻辑将在此编写
</script>
</body>
</html>
```

使用 JavaScript 代码初始化 Echarts 图表并从后端接口获取数据填充

```js
$(document).ready(function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('chartContainer'));
    // 通过jQuery的getJSON方法请求后端数据接口
    $.getJSON('/api/data', function (data) {
        var productNames = [];
        var productPrices = [];
        // 遍历后端返回的数据，提取名称和销量数据
        data.forEach(function (item) {
            productNames.push(item.productName);
            productPrices.push(item.productPrice);
        });
        // 指定图表的配置项和数据
        var option = {
            xAxis: {
                type: 'category',
                data: productNames
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: productPrices,
                type: 'bar'
            }]
        };
        // 使用刚指定的配置项和数据显示图表
        myChart.setOption(option);
    });
});
```
更多图表类型查看示例 `https://echarts.apache.org/examples/zh/index.html`