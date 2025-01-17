## Spring Boot Shiro Remember me
登陆成功后Cookie默认是HttpOnly的，即浏览器关闭便失效。
当然Shiro也为我们提供了Remember Me的功能，用户的登录状态不会因为浏览器的关闭而失效，直到Cookie过期

### ShiroConfig新增Cookie配置

```java
public SimpleCookie rememberMeCookie() {
    // 设置cookie名称，对应login.html页面的<input type="checkbox" name="rememberMe"/>
    SimpleCookie cookie = new SimpleCookie("rememberMe");
    // 设置cookie的过期时间，单位为秒，这里为一天
    cookie.setMaxAge(86400);
    return cookie;
}

/**
 * cookie管理对象
 */
public CookieRememberMeManager rememberMeManager() {
    CookieRememberMeManager cookieRememberMeManager = new CookieRememberMeManager();
    cookieRememberMeManager.setCookie(rememberMeCookie());
    // rememberMe cookie加密的密钥 
    cookieRememberMeManager.setCipherKey(Base64.decode("4AvVhmFLUs0KTA3Kprsdag=="));
    return cookieRememberMeManager;
}
```

接下来将cookie管理对象设置到SecurityManager中

```java
@Bean  
public SecurityManager securityManager(){  
    DefaultWebSecurityManager securityManager =  new DefaultWebSecurityManager();
    securityManager.setRealm(usernamePasswordRealm());
    securityManager.setRememberMeManager(rememberMeManager());
    return securityManager;  
}
```

过滤器链配置

```java
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
    // 静态资源不拦截
    filterChainDefinitionMap.put("/css/**", "anon");
    filterChainDefinitionMap.put("/js/**", "anon");
    filterChainDefinitionMap.put("/fonts/**", "anon");
    filterChainDefinitionMap.put("/img/**", "anon");
    // 配置退出过滤器，其中具体的退出代码Shiro已经替我们实现了
    filterChainDefinitionMap.put("/logout", "logout");
    // 除上以外所有url都必须认证通过才可以访问，未通过认证自动访问LoginUrl
    filterChainDefinitionMap.put("/**", "user");

    shiroFilterFactoryBean.setFilterChainDefinitionMap(filterChainDefinitionMap);
    return shiroFilterFactoryBean;
}
```