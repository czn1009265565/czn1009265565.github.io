## Spring Boot Freemarker

### 引入依赖
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-freemarker</artifactId>
</dependency>
```

### application配置
```yml
spring:
   freemarker:
      request-context-attribute: request
      # 模板后缀名
      suffix: .ftl
      #设置响应的内容类型
      content-type: text/html;charset=utf-8
      #是否允许mvc使用freemarker
      enabled: true
      #是否开启template caching
      cache: false
      #设定模板的加载路径
      template-loader-path: classpath:/templates/
      #设定Template的编码
      charset: UTF-8
      settings:
         # 关闭数字中显示逗号
         number_format: 0
   mvc:
      # 静态文件路径配置
      static-path-pattern: /static/**
```

### 模板

#### 变量
index.ftl
```html
<h1>Welcome ${username}!</h1>
```

模板渲染
```java
@Controller
public class IndexController {
    @GetMapping("/")
    public ModelAndView index(Model model){
        model.addAttribute("username", "admin");
        return new ModelAndView("index");
    }
}
```

模板变量`${}`
- 子变量每级之间用点分隔`article.title`
- 下标访问`articleList[0]`
- 变量null值处理`${user.username!"visitor"}!`

#### 控制结构

```html
<!-- if else -->
<#if animals.python.price < animals.elephant.price>
   Pythons are cheaper than elephants today. 
<#elseif animals.elephant.price < animals.python.price>
   Elephants are cheaper than pythons today.
<#else>
   Elephants and pythons cost the same today.
</#if>

<!-- null值判断 -->
<#if username??>
  ${username}
<#else>
  stranger
</#if>

<!-- for循环 -->
<table>
   <#list animals as animal>
      <tr>
         <!-- 循环下标 从0开始-->
         <td>${animal_index}</td>
         <td>${animal.name}</td>
         <td>${animal.price} Euros</td>
      </tr>
   </#list>
</table>
```

#### 模板继承
适用场景: 多个模板具有完全相同的顶部和底部内容

```
<body>
<#include "components/header.ftl">
<#include "components/footer.ftl">
</body>
```

#### 宏
适用场景: 多个模板中具有相同的模板代码内容，但是内容中部分值不一样

定义common.ftl组件
```
<#macro head title>
  <title>${title}</title>
</#macro>

<#macro footer>
</#macro>
```   
引用组件
```
<#import 'common.ftl' as common>
<@common.head title="主页"></@common.head>
```

