# Spring Security基础入门

Spring Security 是一个功能强大且高度可定制的身份验证和访问控制框架，包含如下核心功能:  

- 身份认证（Authentication）：验证用户身份
- 授权（Authorization）：控制用户访问权限
- 防护攻击：CSRF、会话固定等安全防护
- 会话管理：会话超时、并发会话控制
- 密码加密：提供多种密码加密方式

## 第一个Spring Security项目

### 引入依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
</dependencies>
```

### Spring Security 配置

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    /**
     * 密码编码器配置
     * @return PasswordEncoder
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /**
     * 基于内存的用户存储
     * @return UserDetailsService
     */
    @Bean
    public InMemoryUserDetailsManager userDetailsService(PasswordEncoder passwordEncoder) {
        UserDetails user = User.builder()
                .username("user")
                .password(passwordEncoder.encode("password"))
                .roles("USER")
                .build();

        UserDetails admin = User.builder()
                .username("admin")
                .password(passwordEncoder.encode("password"))
                .roles("ADMIN")
                .build();

        return new InMemoryUserDetailsManager(user, admin);
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers("/static/css/**", "/static/js/**", "/static/images/**").permitAll()
                        .requestMatchers("/auth/login", "/auth/register").permitAll()
                        .requestMatchers("/admin/**").hasRole("ADMIN")
                        .requestMatchers("/user/**").hasAnyRole("USER", "ADMIN")
                        .anyRequest().authenticated()
                )
                .formLogin(form -> form
                        // 自定义登陆页面
                        .loginPage("/auth/login")
                        // 登陆表单提交的URL
                        .loginProcessingUrl("/auth/login")
                        // 登录成功后重定向的URL
                        .defaultSuccessUrl("/dashboard", true)
                        // 登录失败后重定向的URL
                        .failureUrl("/auth/login?error=true")
                        // 允许所有人访问登录页面
                        .permitAll()
                )
                .logout(logout -> logout
                        // 退出登录的URL
                        .logoutUrl("/auth/logout")
                        // 退出登录后跳转的URL
                        .logoutSuccessUrl("/auth/login?logout=true")
                        // 使当前Session失效
                        .invalidateHttpSession(true)
                        // 删除JSESSIONID cookie
                        .deleteCookies("JSESSIONID")
                        // 允许所有人访问退出登录
                        .permitAll()
                )
                .sessionManagement(session -> session
                        // 每个用户最多允许1个活跃会话
                        .maximumSessions(1)
                        // 会话过期后跳转的URL
                        .expiredUrl("/auth/login?expired=true")
                )
                .rememberMe(remember -> remember
                        // 加密密钥
                        .key("uniqueSecretKey")
                        // token有效期30天
                        .tokenValiditySeconds(3600 * 24 * 30)
                )
                .csrf(AbstractHttpConfigurer::disable)
        ;

        return http.build();
    }
}
```

### 自定义登录控制器

```java
@Controller
@RequestMapping("auth")
public class AuthController {

    @GetMapping("login")
    public ModelAndView login() {
        return new ModelAndView("login");
    }
}
```

### 自定义登录页面

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
<form class="login-page" action="/auth/login" method="post">
    <div class="form">
        <h3>账户登录</h3>
        <input type="text" name="username" placeholder="用户名" required>
        <input type="password" name="password" placeholder="密码" required>
        <input type="checkbox" name="remember-me"> 记住我
        <button type="submit">登录</button>
    </div>
</form>
</body>
</html>
```