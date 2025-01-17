# Spring Security 图形验证码

## 生成图形验证码
### 引入依赖
验证码功能需要用到`hutool`依赖

```xml
<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
</dependency>
```

### 自定义验证码对象

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Captcha {
    private String code; //验证码
    private LocalDateTime expireTime; //过期时间

    //构造函数
    public Captcha(String code, long expireIn) {
        this.code = code;
        this.expireTime = LocalDateTime.now().plusSeconds(expireIn);
    }

    //判断验证码是否过期
    public boolean isExpired() {
        return LocalDateTime.now().isAfter(expireTime);
    }
}
```

### CaptchaController
```java
@RestController
@RequestMapping("captcha")
public class CaptchaController {

    public static final String SESSION_KEY = "captcha";

    @GetMapping("/get")
    public void getCaptcha(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("image/jpeg");
        response.setHeader("Pragma", "no-cache");
        response.setHeader("Cache-Control", "no-cache");
        response.setDateHeader("Expires", 0);
        //定义图形验证码的长、宽、验证码字符数、干扰线宽度
        ShearCaptcha shearCaptcha = CaptchaUtil.createShearCaptcha(150, 40, 5, 4);
        //图形验证码写出，可以写出到文件，也可以写出到流
        shearCaptcha.write(response.getOutputStream());
        //获取验证码中的文字内容
        request.getSession().setAttribute(SESSION_KEY, new Captcha(shearCaptcha.getCode(), LocalDateTime.now().plusMinutes(5)));
    }
}
```
### AuthController

```java
@Controller
@RequestMapping("/auth")
public class AuthController {
    @GetMapping("/login")
    public ModelAndView login(HttpServletRequest request, Model model) {
        String msg = request.getParameter("msg");
        if (StringUtils.hasLength(msg)) {
            model.addAttribute("msg", msg);
        }
        return new ModelAndView("login");
    }

    @GetMapping("/logout")
    public ModelAndView logout() {
        return new ModelAndView("logout");
    }
}
```

### 改造登录页

```html
<form class="login-page" action="/auth/login" method="post">
    <!-- 新增csrf校验 -->
    <input name="${_csrf.parameterName}" type="hidden" value="${_csrf.token}">
    <div class="form">
        <h3>账户登录</h3>
        <input type="text" placeholder="用户名" name="username" required="required" />
        <input type="password" placeholder="密码" name="password" required="required" />
        <input type="text" placeholder="验证码" name="captcha" required="required" />
        <img src="/captcha/get"/>
        <#if msg??>
            <p>${msg}</p>
        </#if>
    <button type="submit">登录</button>
    </div>
</form>
```

## 添加验证码校验

### 自定义验证码异常
```java
public class ValidateCodeException extends AuthenticationException {

    public ValidateCodeException(String message) {
        super(message);
    }
}
```

### 自定义认证成功处理器

```java
@Component
public class AuthSuccessHandler implements AuthenticationSuccessHandler {
    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response,
                                        Authentication authentication) throws IOException {
        response.sendRedirect("/");
    }
}
```

### 自定义认证失败处理器

```java
@Component
public class AuthFailureHandler implements AuthenticationFailureHandler {

    @Override
    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response,
                                        AuthenticationException exception) throws IOException {
        // 重定向至登录页，并传递错误信息
        response.sendRedirect("/auth/login?msg=" + URLEncoder.encode(exception.getMessage(), StandardCharsets.UTF_8));
    }
}
```

### 添加校验过滤器

```java
@Component
public class ValidateCodeFilter extends OncePerRequestFilter {

    @Resource
    private AuthenticationFailureHandler authenticationFailureHandler;

    @Override
    protected void doFilterInternal(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse,
                                    FilterChain filterChain) throws ServletException, IOException {
        if (httpServletRequest.getRequestURI().equalsIgnoreCase("/auth/login")
                && httpServletRequest.getMethod().equalsIgnoreCase("post")) {
            try {
                validateCode(httpServletRequest);
            } catch (ValidateCodeException e) {
                // 交给认证失败处理器处理
                authenticationFailureHandler.onAuthenticationFailure(httpServletRequest, httpServletResponse, e);
                return;
            }
        }
        filterChain.doFilter(httpServletRequest, httpServletResponse);
    }
    private void validateCode(HttpServletRequest httpServletRequest) {
        HttpSession session = httpServletRequest.getSession();
        Captcha captcha = (Captcha) session.getAttribute(CaptchaController.SESSION_KEY);
        String code = httpServletRequest.getParameter(CaptchaController.SESSION_KEY);
        if (!StringUtils.hasLength(code)) {
            throw new ValidateCodeException("验证码不能为空！");
        }
        if (captcha == null) {
            throw new ValidateCodeException("验证码不存在！");
        }
        if (captcha.isExpired()) {
            session.removeAttribute(CaptchaController.SESSION_KEY);
            throw new ValidateCodeException("验证码已过期！");
        }
        if (!code.equalsIgnoreCase(captcha.getCode())) {
            throw new ValidateCodeException("验证码不正确！");
        }
        session.removeAttribute(CaptchaController.SESSION_KEY);
    }
}
```

### 配置验证码过滤器

```java
@Configuration
// 开启@PreAuthorize权限校验
@EnableGlobalMethodSecurity(prePostEnabled=true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Resource
    private ValidateCodeFilter validateCodeFilter;

    @Resource
    private AuthenticationSuccessHandler authenticationSuccessHandler;

    @Resource
    private AuthenticationFailureHandler authenticationFailureHandler;

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Override
    protected void configure(HttpSecurity httpSecurity) throws Exception {
        httpSecurity
                .addFilterBefore(validateCodeFilter, UsernamePasswordAuthenticationFilter.class)
                .authorizeRequests()
                .antMatchers("/auth/login").permitAll()
                .antMatchers("/captcha/get").permitAll()
                .antMatchers(
                        HttpMethod.GET,
                        "/*.html",
                        "/**/*.html",
                        "/**/*.css",
                        "/**/*.js"
                ).permitAll()
                .anyRequest().authenticated()
                .and()
                .formLogin()
                // 自定义登录界面
                .loginPage("/auth/login")
                // 指定处理登录请求的路径
                .loginProcessingUrl("/auth/login")
                // 注册登录成功处理器
                .successHandler(authenticationSuccessHandler)
                // 注册登录失败处理器
                .failureHandler(authenticationFailureHandler)
                .and()
                // 指定的登出路径
                .logout().logoutUrl("/auth/logout")
                .and()
                .httpBasic().disable()
                // 开启csrf认证
                .csrf();
    }
}
```
上面代码中，我们注入了`ValidateCodeFilter`，
然后通过`addFilterBefore`方法将`ValidateCodeFilter`验证码校验过滤器添加到了`UsernamePasswordAuthenticationFilter`前面。

