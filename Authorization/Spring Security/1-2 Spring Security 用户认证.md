# Spring Security 用户认证
上文实现了Spring Security 基于内存的用户存储，但仅局限于固定用户，无法完成多用户注册管理。
本文则实现了数据库用户认证以及自定义登录、登出接口。

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

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
    </dependency>
</dependencies>
```

### 数据库连接配置

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/dbname
    username: root
    password: root
    driver-class-name: com.mysql.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: true
```

### 创建用户表
```mysql
CREATE TABLE `sys_user`(
    `id` VARCHAR(32) NOT NULL PRIMARY KEY COMMENT 'id',
    `username` VARCHAR(100) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `enabled` BOOLEAN NOT NULL COMMENT '用户是否可用',
    `roles` VARCHAR(255) COMMENT '用户角色',
    `email` VARCHAR(255) COMMENT '邮箱',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
)COMMENT='用户详情表';

CREATE UNIQUE INDEX `username_index` USING BTREE ON `sys_user`(`username`);
```

### 用户实体类与持久层

```java
@Data
@Entity
@Table(name = "sys_user")
public class SysUserDO {
    @Id
    private String id;
    private String username;
    private String password;
    private Boolean enabled;
    private String roles;
    private String email;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}
```

```java
@Repository
public interface SysUserRepository extends JpaRepository<SysUserDO, String> {
    SysUserDO findByUsername(String username);
}
```

### 自定义用户认证

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoginUser implements UserDetails {

    private SysUserDO sysUserDO;

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Arrays.stream(sysUserDO.getRoles().split(","))
                .filter(StringUtils::hasLength)
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());
    }

    @Override
    public String getPassword() {
        return sysUserDO.getPassword();
    }
    @Override
    public String getUsername() {
        return sysUserDO.getUsername();
    }
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }
    @Override
    public boolean isEnabled() {
        return sysUserDO.getEnabled();
    }
}
```

注意点：在Spring Security Config中角色配置如下`ADMIN`,`USER`,而在数据库中需要`ROLE_`前缀

```java
@Component
public class UserDetailsServiceImpl implements UserDetailsService {

    @Resource
    private SysUserRepository sysUserRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        SysUserDO sysUserDO = sysUserRepository.findByUsername(username);
        if (sysUserDO == null) {
            throw new UsernameNotFoundException("用户不存在");
        }
        LoginUser loginUser = new LoginUser();
        loginUser.setSysUserDO(sysUserDO);
        return loginUser;
    }

    /**
     * 获取已登录用户
     * @return LoginUser
     */
    public LoginUser obtainLoginUser() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication.getPrincipal() instanceof LoginUser) {
            return (LoginUser) authentication.getPrincipal();
        }
        return null;
    }
}
```

### 自定义用户登录、登出

```java
@Slf4j
@Controller
@RequestMapping("auth")
public class AuthController {

    @Resource
    private AuthenticationManager authenticationManager;

    @GetMapping("login")
    public ModelAndView login() {
        return new ModelAndView("login");
    }

    @PostMapping("login")
    @ResponseBody
    public ResponseVO<String> login(@RequestBody AuthLoginReqVO authLoginReqVO, HttpServletRequest request) {
        try {
            // 手动进行认证
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            authLoginReqVO.getUsername(),
                            authLoginReqVO.getPassword()
                    )
            );
            // 设置认证信息到安全上下文
            SecurityContextHolder.getContext().setAuthentication(authentication);
            // 创建和管理Session
            request.getSession().setAttribute("SPRING_SECURITY_CONTEXT",
                    SecurityContextHolder.getContext());
            // 获取用户详细信息
            UserDetails userDetails = (UserDetails) authentication.getPrincipal();
            log.info("用户登录成功: {} - Session: {}",
                    authLoginReqVO.getUsername(), request.getSession().getId());
            return ResponseVO.success();

        } catch (BadCredentialsException e) {
            log.warn("登录失败 - 用户名或密码错误: {}", authLoginReqVO.getUsername());
            return ResponseVO.error(401, "用户名或密码错误");
        } catch (DisabledException e) {
            log.warn("登录失败 - 用户已被禁用: {}", authLoginReqVO.getUsername());
            return ResponseVO.error(401, "用户已被禁用");
        } catch (Exception e) {
            log.error("登录过程发生错误: {}", e.getMessage(), e);
            return ResponseVO.error(401, "登录失败");
        }
    }

    /**
     * 自定义退出登录接口
     */
    @GetMapping("/logout")
    @ResponseBody
    public ResponseVO<String> logout(HttpServletRequest request,
                                     HttpServletResponse response) {
        try {
            // 1. 清除SecurityContext
            SecurityContextHolder.clearContext();

            // 2. 使Session失效
            HttpSession session = request.getSession(false);
            if (session != null) {
                session.invalidate();
            }
            // 3. 清除Cookie（如果需要）
            Cookie cookie = new Cookie("JSESSIONID", null);
            cookie.setPath("/");
            cookie.setMaxAge(0);
            response.addCookie(cookie);
            return ResponseVO.success();
        } catch (Exception e) {
            return ResponseVO.error(500, "退出登录失败");
        }
    }
}
```

### 自定义登录页面

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - 我的应用</title>
    <link href="https://cdn.staticfile.net/bootstrap/5.3.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-secondary">
    <div class="container-fluid">
        <a class="navbar-brand" href="/index">我的应用</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" href="/auth/login">登录</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/auth/register">注册</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="login-container">
    <h2 class="text-center mb-4">用户登录</h2>
    <form>
        <div class="mb-3">
            <label for="username" class="form-label">用户名</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="请输入用户名">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">密码</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="请输入密码">
        </div>
        <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="remember" name="remember">
            <label class="form-check-label" for="remember">记住我</label>
        </div>
        <button type="submit" class="btn btn-secondary w-100" id="login">登录</button>
    </form>
</div>

<!-- 模态框 -->
<div class="modal fade" id="alertModal" tabindex="-1" aria-labelledby="alertModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-body">
                <p id="modalText"></p>
            </div>
        </div>
    </div>
</div>

<footer class="bg-light text-center py-3 mt-5">
    <div class="container">
        <span class="text-muted">© 2023 我的应用 - 版权所有</span>
    </div>
</footer>

<script src="https://cdn.staticfile.net/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdn.staticfile.net/bootstrap/5.3.2/js/bootstrap.bundle.min.js"></script>

<script>
    function alert(msg) {
        $('#modalText').text(msg);
        $('#alertModal').modal('show');

        setTimeout(function () {
            $('#alertModal').modal('hide')
        }, 3000);
    }

    function login(element) {
        // 阻止表单默认提交
        element.preventDefault();

        let username = $('#username').val();
        let password = $('#password').val();
        $.ajax({
            url: '/auth/login',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                "username": username,
                "password": password
            }),
            success: function(response) {
                if (response.code === 0) {
                    // 跳转至主页
                    window.location.href = '/index';
                } else {
                    alert(response.msg);
                }
            },
            error: function(xhr, status, error) {
                alert('登录接口请求异常!');
            }
        });

    }
    // 绑定登录按钮
    $(function() {
        // 绑定注册按钮
        $('#login').click(login);
    });
</script>
</body>
</html>
```

### 自定义失败处理器
认证失败时返回json数据或跳转至登录页面

```java
@Slf4j
@Controller
public class AuthenticationEntryPointHandler implements AuthenticationEntryPoint {

    @Override
    public void commence(HttpServletRequest request,
                         HttpServletResponse response,
                         AuthenticationException authException) throws IOException {

        // 如果是 AJAX 请求，返回 JSON 响应
        if (isAjaxRequest(request)) {
            response.setContentType("application/json;charset=UTF-8");
            response.setStatus(HttpStatus.UNAUTHORIZED.value());
            response.getWriter().write(
                    "{\"code\": 401, \"msg\": \"未认证，请先登录\"}"
            );
        } else {
            // 普通请求重定向到登录页
            response.sendRedirect("/auth/login");
        }
    }

    private boolean isAjaxRequest(HttpServletRequest request) {
        return "XMLHttpRequest".equals(request.getHeader("X-Requested-With")) ||
                request.getHeader("Accept") != null &&
                        request.getHeader("Accept").contains("application/json");
    }
}
```

### Spring Security 配置

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Resource
    private AuthenticationEntryPointHandler authenticationEntryPointHandler;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
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
                // 禁用默认的表单登录
                .formLogin(AbstractHttpConfigurer::disable)
                // 禁用默认的登出
                .logout(AbstractHttpConfigurer::disable)
                // 配置自定义的认证入口点和失败处理
                .exceptionHandling(exception -> exception
                        .authenticationEntryPoint(authenticationEntryPointHandler)
                )
                .sessionManagement(session -> session
                        // 每个用户最多允许1个活跃会话
                        .maximumSessions(1)
                        // 后登录的会使先登录的失效
                        .maxSessionsPreventsLogin(false)
                        // 会话过期后跳转的URL
                        .expiredUrl("/auth/login?expired=true")
                )
                .rememberMe(remember -> remember
                        // 加密密钥
                        .key("uniqueSecretKey")
                        // token有效期30天
                        .tokenValiditySeconds(3600 * 24 * 30)
                )
                // 禁用csrf校验
                .csrf(AbstractHttpConfigurer::disable);
        return http.build();
    }
}
```