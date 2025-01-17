## Spring Boot Shiro 手机号认证

### 自定义PhoneToken

```java
@Data
public class PhoneToken implements HostAuthenticationToken, RememberMeAuthenticationToken {
    private String phone;
    private String verificationCode;
    private boolean rememberMe;
    private String host;

    @Override
    public Object getPrincipal() {
        return phone;
    }

    @Override
    public Object getCredentials() {
        return verificationCode;
    }
}
```

### 自定义手机号认证逻辑

```java
public class PhoneRealm extends AuthorizingRealm {

    @Override
    public String getName() {
        return "PhoneRealm";
    }

    /**
     * 获取用户角色和权限
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        return null;
    }

    @Override
    public boolean supports(AuthenticationToken authenticationToken) {
        // 仅支持PhoneToken类型的Token
        return authenticationToken instanceof PhoneToken;
    }

    /**
     * 登录认证
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken) throws AuthenticationException {
        PhoneToken token = (PhoneToken) authenticationToken;

        String phone = token.getPhone();
        String verificationCode = token.getVerificationCode();
        // 1. 根据手机查询用户信息(不存在则创建)
        // 2. 根据手机号查询redis中的验证码
        if(!"8888".equals(verificationCode)) {
            throw new IncorrectCredentialsException();
        }
        return new SimpleAuthenticationInfo(phone, verificationCode, getName());
    }
}
```

### SecurityManager注册多种认证方式

```java
@Configuration
public class ShiroConfig {
    @Bean
    public ShiroFilterFactoryBean shiroFilterFactoryBean(SecurityManager securityManager) {
        ShiroFilterFactoryBean shiroFilterFactoryBean = new ShiroFilterFactoryBean();
        // 设置securityManager
        shiroFilterFactoryBean.setSecurityManager(securityManager);
        // 静态登陆页面url
        shiroFilterFactoryBean.setLoginUrl("/login");
        // 登录成功后跳转的url
        shiroFilterFactoryBean.setSuccessUrl("/index");

        LinkedHashMap<String, String> filterChainDefinitionMap = new LinkedHashMap<>();
        // 定义filterChain
        filterChainDefinitionMap.put("/login", "anon");
        filterChainDefinitionMap.put("/plogin", "anon");
        // 静态资源不拦截
        filterChainDefinitionMap.put("/css/**", "anon");
        filterChainDefinitionMap.put("/js/**", "anon");
        filterChainDefinitionMap.put("/fonts/**", "anon");
        filterChainDefinitionMap.put("/img/**", "anon");
        // 配置退出过滤器，其中具体的退出代码Shiro已经替我们实现了
        filterChainDefinitionMap.put("/logout", "logout");
        // 除上以外所有url都必须认证通过才可以访问，未通过认证自动访问LoginUrl
        filterChainDefinitionMap.put("/**", "authc");

        shiroFilterFactoryBean.setFilterChainDefinitionMap(filterChainDefinitionMap);
        return shiroFilterFactoryBean;
    }

    @Bean
    public SecurityManager securityManager(){
        // 配置SecurityManager,自定义认证逻辑
        DefaultWebSecurityManager securityManager =  new DefaultWebSecurityManager();
        securityManager.setRealms(Arrays.asList(usernamePasswordRealm(), phoneRealm()));
        return securityManager;
    }

    @Bean
    public UsernamePasswordRealm usernamePasswordRealm() {
        return new UsernamePasswordRealm();
    }

    @Bean
    public PhoneRealm phoneRealm() {
        return new PhoneRealm();
    }
}
```

### AuthController


```java
@PostMapping("sendCode")
@ResponseBody
public ResponseVO sendCode(String phone) {
    // 1. 生成随机code
    // 2. redis 限时保存
    // 3. 发送验证码
    return ResponseVO.ok();
}


@PostMapping("/plogin")
@ResponseBody
public ResponseVO plogin(String phone, String verificationCode) {
    // 密码MD5加密
    PhoneToken token = new PhoneToken(phone, verificationCode);
    // 获取Subject对象
    Subject subject = SecurityUtils.getSubject();
    try {
        subject.login(token);
        return ResponseVO.ok();
    } catch (IncorrectCredentialsException e) {
        return ResponseVO.error("验证码错误");
    } catch (LockedAccountException e) {
        return ResponseVO.error("用户已被锁定");
    } catch (AuthenticationException e) {
        return ResponseVO.error("认证失败！");
    }
}
```