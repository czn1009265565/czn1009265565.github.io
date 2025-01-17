# Spring Security 表单认证

## 认证流程

1. 用户向服务器发送用户名和密码用于登陆系统。
2. 服务器验证通过后，服务器为用户创建一个 Session，并将 Session信息存储 起来。
3. 服务器向用户返回一个 SessionID，写入用户的 Cookie。
4. 当用户保持登录状态时，Cookie 将与每个后续请求一起被发送出去。
5. 服务器可以将存储在 Cookie 上的 Session ID 与存储在内存中或者数据库中的 Session 信息进行比较，以验证用户的身份，返回给用户客户端响应信息的时候会附带用户当前的状态。

## Spring Boot 集成

### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

### application.yml配置

```yml
spring:
  security:
    user:
      name: root
      password: root
```

### 新增WebSecurityConfig

配置详情和XML相类似，具体查看源码即可,可以先看主要的三个ExpressionUrlAuthorizationConfigurer,FormLoginConfigurer,LogoutConfigurer
```java
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .antMatchers("/auth/login").permitAll()
                .anyRequest().authenticated()
                .and()
                .formLogin()
                // 自定义登录界面
                .loginPage("/auth/login")
                // 指定处理登录请求的路径
                .loginProcessingUrl("/auth/login")
                .and()
                // 指定的登出路径
                .logout().logoutUrl("/auth/logout")
                .and()
                .httpBasic().disable()
                .csrf().disable()
                ;
    }
}
```

### 集成freemarker
```xml
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-freemarker</artifactId>
</dependency>
```
application配置
```yml
spring:
  freemarker:
    suffix: .ftl
    cache: false
    charset: UTF-8
```
   
### 自定义登陆页面

login.ftl
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form class="login-page" action="/auth/login" method="post">
    <div class="form">
        <h3>账户登录</h3>
        <input type="text" placeholder="用户名" name="username" required="required" />
        <input type="password" placeholder="密码" name="password" required="required" />
        <button type="submit">登录</button>
    </div>
</form>

</body>
</html>
```

AuthController
```java
@Controller
@RequestMapping("/auth")
public class AuthController {
    @GetMapping("/login")
    public ModelAndView login() {
        return new ModelAndView("login");
    }
}
```