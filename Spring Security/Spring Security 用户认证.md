# Spring Security 用户认证
上文实现了Spring Security 表单认证，但仅局限于单用户，无法完成多用户注册管理。

好在Spring Security支持各种来源的用户数据，包括内存、数据库、LDAP等。
它们被抽象为一个UserDetailsService接口，任何实现了 UserDetailsService 接口的对象都可以作为认证数据源。

## Spring Boot 集成

### 创建用户表
```sql
CREATE TABLE `sys_user`(
    `id` BIGINT(20) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
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

### 用户实体类`SysUserDO`

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysUserDO {
   private Long id;
   private String username;
   private String password;
   private Boolean enabled;
   private String roles;
   private String email;
   private LocalDateTime createTime;
   private LocalDateTime updateTime;
}
```

### 自定义用户认证类(实现UserDetails接口)

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

注意点：在Spring Security Config中角色配置如下`ADMIN`,`USER`,而在数据库中需要`ROLE_`前缀，查看hasRole源码可知

### 重写用户校验

```java
@Component
public class UserDetailsServiceImpl implements UserDetailsService {

    private static Map<String, UserDetails> userDetailsMap;

    static {
        // 初始化用户
        PasswordEncoder passwordEncoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
        LoginUser loginUser = new LoginUser();
        loginUser.setSysUserDO(new SysUserDO(10001L, "admin", passwordEncoder.encode("123456"), true, "ROLE_ADMIN", "163@163.com", LocalDateTime.now(), LocalDateTime.now()));
        userDetailsMap = Collections.singletonMap("admin", loginUser);
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserDetails userDetails = userDetailsMap.get(username);
        if (userDetails == null) {
            throw new UsernameNotFoundException("用户不存在");
        }
        return userDetails;
    }

    /** 获取已登录用户 */
    public LoginUser obtainLoginUser() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication.getPrincipal() instanceof LoginUser) {
            return (LoginUser) authentication.getPrincipal();
        }
        return null;
    }
}
```

### WebSecurityConfig
这里与上文表单认证不同，我们开启了csrf认证.
```java
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .antMatchers("/auth/login").permitAll()
                .antMatchers("/admin/**").hasAnyRole("ADMIN")
                .antMatchers("/user/**").hasAnyRole("USER")
                .antMatchers("/app/**").permitAll()
                .anyRequest().authenticated()
                .and()
                .formLogin()
                // 自定义登录界面
                .loginPage("/auth/login")
                // 指定处理登录请求的路径
                .loginProcessingUrl("/auth/login")
                .and()
                // 指定的登出路径 注意需要是POST请求
                .logout().logoutUrl("/auth/logout")
                .and()
                .httpBasic().disable()
                // 开启csrf认证
                .csrf()
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

### AuthController
```java
@Controller
@RequestMapping("/auth")
public class AuthController {
    @GetMapping("/login")
    public ModelAndView login() {
        return new ModelAndView("login");
    }

    @GetMapping("/logout")
    public ModelAndView logout() {
        return new ModelAndView("logout");
    }
}
```

### 自定义登录页面

login.ftl
```html
<form class="login-page" action="/auth/login" method="post">
    <!-- 新增csrf校验 -->
    <input name="${_csrf.parameterName}" type="hidden" value="${_csrf.token}">
    <div class="form">
        <h3>账户登录</h3>
        <input type="text" placeholder="用户名" name="username" required="required" />
        <input type="password" placeholder="密码" name="password" required="required" />
        <button type="submit">登录</button>
    </div>
</form>
```

### 自定义登出页面

logout.ftl
```html
<form action="/auth/logout" method="post">
    <!-- 新增csrf校验 -->
    <input name="${_csrf.parameterName}" type="hidden" value="${_csrf.token}">
    <input id="exit" type="submit" value="退出">
</form>
```