# Spring Security 数据库表单认证

## 认证流程

1. 用户向服务器发送用户名和密码用于登陆系统。
2. 服务器验证通过后，服务器为用户创建一个 Session，并将 Session信息存储 起来。
3. 服务器向用户返回一个 SessionID，写入用户的 Cookie。
4. 当用户保持登录状态时，Cookie 将与每个后续请求一起被发送出去。
5. 服务器可以将存储在 Cookie 上的 Session ID 与存储在内存中或者数据库中的 Session 信息进行比较，以验证用户的身份，返回给用户客户端响应信息的时候会附带用户当前的状态。

## Spring Boot 集成

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

    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
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
        <input type="checkbox" name="remember"> 记住我
        <button type="submit">登录</button>
    </div>
</form>
</body>
</html>
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
                        // 覆盖登录
                        .maxSessionsPreventsLogin(false)  
                        // 会话过期后跳转的URL
                        .expiredUrl("/auth/login?expired=true")
                )
                .rememberMe(remember -> remember
                        // 加密密钥
                        .key("uniqueSecretKey")
                        // 参数名，与前端传参一致
                        .rememberMeParameter("remember")
                        // token有效期30天
                        .tokenValiditySeconds(3600 * 24 * 30)
                )
                .csrf(AbstractHttpConfigurer::disable);
        return http.build();
    }
}
```