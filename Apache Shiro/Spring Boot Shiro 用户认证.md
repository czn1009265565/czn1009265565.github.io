## Spring Boot Shiro 用户认证

### 引入依赖

```xml
<dependency>
    <groupId>org.apache.shiro</groupId>
    <artifactId>shiro-spring</artifactId>
    <version>1.9.0</version>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

### ShiroConfig

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
        securityManager.setRealm(usernamePasswordRealm());
        return securityManager;
    }

    @Bean
    public UsernamePasswordRealm usernamePasswordRealm() {
        return new UsernamePasswordRealm();
    }
}
```

其中anon、authc等为Shiro为我们实现的过滤器，具体如下表所示：

|Filter Name|Class|Description|
|---|---|---|
|anon|org.apache.shiro.web.filter.authc.AnonymousFilter|匿名拦截器，即不需要登录即可访问；一般用于静态资源过滤|
|authc|org.apache.shiro.web.filter.authc.FormAuthenticationFilter|基于表单的拦截器；如/**=authc，如果没有登录会跳到相应的登录页面登录|
|authcBasic|org.apache.shiro.web.filter.authc.BasicHttpAuthenticationFilter|Basic HTTP身份验证拦截器|
|logout|org.apache.shiro.web.filter.authc.LogoutFilter|退出拦截器，主要属性：redirectUrl：退出成功后重定向的地址（/）|
|noSessionCreation|org.apache.shiro.web.filter.session.NoSessionCreationFilter|不创建会话拦截器，调用subject.getSession(false)不会有什么问题，但是如果subject.getSession(true)将抛出DisabledSessionException异常|
|perms|org.apache.shiro.web.filter.authz.PermissionsAuthorizationFilter|权限授权拦截器，验证用户是否拥有所有权限；属性和roles一样；示例/user/**=perms["user:create"]|
|port|org.apache.shiro.web.filter.authz.PortFilter|端口拦截器，主要属性port(80)：可以通过的端口；示例/test= port[80]，如果用户访问该页面是非80，将自动将请求端口改为80并重定向到该80端口，其他路径/参数等都一样|
|rest|org.apache.shiro.web.filter.authz.HttpMethodPermissionFilter|rest风格拦截器，自动根据请求方法构建权限字符串；示例/users=rest[user]，会自动拼出user:read,user:create,user:update,user:delete权限字符串进行权限匹配（所有都得匹配，isPermittedAll）|
|roles|org.apache.shiro.web.filter.authz.RolesAuthorizationFilter|角色授权拦截器，验证用户是否拥有所有角色；示例/admin/**=roles[admin]|
|ssl|org.apache.shiro.web.filter.authz.SslFilter|SSL拦截器，只有请求协议是https才能通过；否则自动跳转会https端口443；其他和port拦截器一样；|
|user|org.apache.shiro.web.filter.authc.UserFilter|用户拦截器，用户已经身份验证/记住我登录的都可；示例/**=user|

### Realm

自定义认证逻辑

```java
public class UsernamePasswordRealm extends AuthorizingRealm {

    @Override
    public String getName() {
        return "UsernamePasswordRealm";
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
        // 仅支持UsernamePasswordToken类型的Token
        return authenticationToken instanceof UsernamePasswordToken;
    }

    /**
     * 登录认证
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken) throws AuthenticationException {
        UsernamePasswordToken token = (UsernamePasswordToken) authenticationToken;

        String username = token.getUsername();
        String password = String.valueOf(token.getPassword());
        // 数据库用户查询验证
        if(!"root".equals(username)) {
            throw new UnknownAccountException(); //如果用户名错误
        }
        if(!"root".equals(password)) {
            throw new IncorrectCredentialsException(); //如果密码错误
        }
        return new SimpleAuthenticationInfo(username, password, getName());
    }
}
```

### AuthController

```java
@Controller
public class AuthController {

    @GetMapping("/login")
    public String login() {
        return "login";
    }

    @PostMapping("/login")
    @ResponseBody
    public ResponseVO login(String username, String password) {
        // 密码MD5加密
        // password = MD5Utils.encrypt(username, password);
        UsernamePasswordToken token = new UsernamePasswordToken(username, password);
        // 获取Subject对象
        Subject subject = SecurityUtils.getSubject();
        try {
            subject.login(token);
            return ResponseVO.ok();
        } catch (UnknownAccountException | IncorrectCredentialsException e) {
            return ResponseVO.error("用户名或密码错误");
        } catch (LockedAccountException e) {
            return ResponseVO.error("用户已被锁定");
        } catch (AuthenticationException e) {
            return ResponseVO.error("认证失败！");
        }
    }
}
```

### 页面准备

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
    <script src="/js/jquery-1.11.3.min.js"></script>
</head>
<body>
<div class="login-page">
    <div class="form">
        <input type="text" placeholder="用户名" name="username" required="required"/>
        <input type="password" placeholder="密码" name="password" required="required"/>
        <button onclick="login()">登录</button>
    </div>
</div>
</body>
<script th:inline="javascript">
    function login() {
        var ctx = "/";
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        $.ajax({
            type: "post",
            url: ctx + "login",
            data: {"username": username, "password": password},
            dataType: "json",
            success: function (r) {
                if (r.code === 0) {
                    location.href = ctx + 'index';
                } else {
                    alert(r.msg);
                }
            }
        });
    }
</script>
</html>
```