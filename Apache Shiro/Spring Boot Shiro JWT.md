## Spring Boot Shiro JWT

### 引入依赖

```xml
<dependency>
    <groupId>org.apache.shiro</groupId>
    <artifactId>shiro-spring</artifactId>
    <version>1.9.0</version>
</dependency>

<dependency>
    <groupId>com.auth0</groupId>
    <artifactId>java-jwt</artifactId>
    <version>4.0.0</version>
</dependency>
```

### JwtToken
封装JwtToken来替换shiro的原生token，需要实现AuthenticationToken接口

```java
public class JwtToken implements AuthenticationToken {
    private final String token;

    public JwtToken(String token) {
        this.token = token;
    }

    @Override
    public Object getPrincipal() {
        return token;
    }

    @Override
    public Object getCredentials() {
        return token;
    }
}
```

### 新增JwtUtil

```java
public class JwtUtil {
    public static final String ACCOUNT = "username";
    public static final long EXPIRE_TIME = 30 * 60 * 1000;

    /** 根据密码生成jwt校验器，校验token是否正确 */
    public static boolean verify(String token, String username, String secret) {
        try{
            Algorithm algorithm = Algorithm.HMAC256(secret);
            JWTVerifier verifier = JWT.require(algorithm)
                    .withClaim(ACCOUNT, username)
                    .build();

            DecodedJWT jwt = verifier.verify(token);
            return true;
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }

    /** 获得token中指定字段的信息 */
    public static String getClaimField(String token,String claim){
        try{
            DecodedJWT jwt = JWT.decode(token);
            return jwt.getClaim(claim).asString();
        }catch (JWTDecodeException e){
            e.printStackTrace();
            return  null;
        }
    }

    /** 生成附带用户信息及过期时间的签名 */
    public static String sign(String username, String secret) {
        Date date = new Date(System.currentTimeMillis() + EXPIRE_TIME);
        Algorithm algorithm = Algorithm.HMAC256(secret);
        return JWT.create()
                .withClaim(ACCOUNT, username)
                .withExpiresAt(date)
                .sign(algorithm);
    }
}
```

### 添加JwtFilter拦截器
继承AccessControlFilter 类，验证从请求的header中取出的token信息

```java
public class JwtFilter extends AccessControlFilter {
    public static String ACCESS_TOKEN = "Access-Token";

    @Override
    protected boolean isAccessAllowed(ServletRequest request, ServletResponse response, Object mappedValue) throws Exception {
        return false;
    }

    @Override
    protected boolean onAccessDenied(ServletRequest request, ServletResponse response) throws Exception {
        HttpServletRequest req = (HttpServletRequest) request;
        // 解决跨域问题
        if(HttpMethod.OPTIONS.toString().matches(req.getMethod())) {
            return true;
        }
        if (isLoginAttempt(request, response)) {
            JwtToken token = new JwtToken(req.getHeader(ACCESS_TOKEN));
            try {
                getSubject(request, response).login(token);
                return true;
            } catch (Exception e) {
            }
        }
        onLoginFail(response);
        return false;
    }

    protected boolean isLoginAttempt(ServletRequest request, ServletResponse response) {
        HttpServletRequest req = (HttpServletRequest) request;
        String authorization = req.getHeader(ACCESS_TOKEN);
        return authorization != null;
    }

    //登录失败时默认返回401状态码
    private void onLoginFail(ServletResponse response) throws IOException {
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        httpResponse.setContentType("application/json;charset=utf-8");
        httpResponse.getWriter().write("login fail");
    }
}
```

### 新增JwtRealm

自定义认证逻辑

```java
@Slf4j
public class JwtRealm extends AuthorizingRealm {
    @Override
    public boolean supports(AuthenticationToken token) {
        return token instanceof JwtToken;
    }

    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principals) {
        String username = principals.toString();
        SimpleAuthorizationInfo simpleAuthorizationInfo = new SimpleAuthorizationInfo();
        // 查询用户角色、权限
        simpleAuthorizationInfo.addRoles(Collections.singleton("admin"));
        simpleAuthorizationInfo.addStringPermissions(Arrays.asList("create","delete","update","read"));
        return simpleAuthorizationInfo;
    }

    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken) throws AuthenticationException {
        String token = (String) authenticationToken.getCredentials();
        String userName = null;
        try {
            userName = JwtUtil.getClaimField(token, JwtUtil.ACCOUNT);
            // TODO 数据库用户查询
            if (!"root".equals(userName)) {
                log.info("用户不存在");
                return null;
            }
            // TODO 获取用户密码校验
            boolean verify = JwtUtil.verify(token, userName, "password");
            if (!verify) {
                log.info("Token校验不正确");
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new SimpleAuthenticationInfo(
                userName, token, getName());
    }
}
```

### 创建JwtSubjectFactory 关闭session

```java
public class JwtSubjectFactory extends DefaultWebSubjectFactory {
    @Override
    public Subject createSubject(SubjectContext context) {
        context.setSessionCreationEnabled(false);
        return super.createSubject(context);
    }
}
```

### ShiroConfig
这里除了配置shiro自身三个核心组件filter、realm、securityManager的注入外，还关闭了shiro的会话管理，注入Subject工厂，以及开启对shiro注解的支持

```java
@Configuration
public class ShiroConfig {
    @Bean
    public ShiroFilterFactoryBean shiroFilter(@Qualifier("defaultWebSecurityManager") DefaultWebSecurityManager webSecurityManager){
        ShiroFilterFactoryBean shiroFilterFactoryBean = new ShiroFilterFactoryBean();
        shiroFilterFactoryBean.setSecurityManager(webSecurityManager);

        Map<String,String> filterChainDefinitionMap=new LinkedHashMap<>();
        filterChainDefinitionMap.put("/toLogin","anon");
        shiroFilterFactoryBean.setLoginUrl("/login");
        shiroFilterFactoryBean.setSuccessUrl("/index");

        //shiro自定义过滤器
        Map<String, Filter> filters = new LinkedHashMap<>();
        filters.put("jwt", new JwtFilter());
        shiroFilterFactoryBean.setFilters(filters);
        filterChainDefinitionMap.put("/**","jwt");

        shiroFilterFactoryBean.setFilterChainDefinitionMap(filterChainDefinitionMap);
        return shiroFilterFactoryBean;
    }

    @Bean
    public DefaultWebSessionManager sessionManager() {
        DefaultWebSessionManager defaultSessionManager = new DefaultWebSessionManager();
        defaultSessionManager.setSessionValidationSchedulerEnabled(false);
        return defaultSessionManager;
    }

    @Bean
    public DefaultWebSubjectFactory subjectFactory() {
        return new JwtSubjectFactory();
    }

    @Bean(name = "defaultWebSecurityManager")
    public DefaultWebSecurityManager defaultWebSecurityManager(@Qualifier("realm") JwtRealm realm,
                                                               SubjectFactory subjectFactory, SessionManager sessionManager){
        DefaultWebSecurityManager webSecurityManager=new DefaultWebSecurityManager();
        webSecurityManager.setRealm(realm);

        //关闭shiro自带的session
        DefaultSubjectDAO subjectDAO = new DefaultSubjectDAO();
        DefaultSessionStorageEvaluator defaultSessionStorageEvaluator = new DefaultSessionStorageEvaluator();
        defaultSessionStorageEvaluator.setSessionStorageEnabled(false);
        subjectDAO.setSessionStorageEvaluator(defaultSessionStorageEvaluator);
        webSecurityManager.setSubjectDAO(subjectDAO);

        webSecurityManager.setSubjectFactory(subjectFactory);
        webSecurityManager.setSessionManager(sessionManager);
        return webSecurityManager;
    }

    @Bean(name = "realm")
    public JwtRealm myRealm(){
        return new JwtRealm();
    }

    @Bean
    public LifecycleBeanPostProcessor lifecycleBeanPostProcessor() {
        return new LifecycleBeanPostProcessor();
    }

    @Bean
    @DependsOn({"lifecycleBeanPostProcessor"})
    public DefaultAdvisorAutoProxyCreator advisorAutoProxyCreator() {
        DefaultAdvisorAutoProxyCreator advisorAutoProxyCreator = new DefaultAdvisorAutoProxyCreator();
        advisorAutoProxyCreator.setProxyTargetClass(true);
        return advisorAutoProxyCreator;
    }

    @Bean
    public AuthorizationAttributeSourceAdvisor authorizationAttributeSourceAdvisor(SecurityManager securityManager) {
        AuthorizationAttributeSourceAdvisor authorizationAttributeSourceAdvisor = new AuthorizationAttributeSourceAdvisor();
        authorizationAttributeSourceAdvisor.setSecurityManager(securityManager);
        return authorizationAttributeSourceAdvisor;
    }
}
```

### LoginController

```java
@RestController
public class LoginController {

    @GetMapping("/toLogin")
    public String login() {
        String username = "root";
        String password = "password";
        return JwtUtil.sign(username, password);
    }

    @GetMapping("/test")
    public String test() {
        return "success";
    }
}
```

测试

```shell
curl --location --request GET 'localhost:8080/test' \
--header 'ACCESS-TOKEN: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTcwMjU4MTgsInVzZXJuYW1lIjoicm9vdCJ9.HY5i0ny6RSN3T2F22CHRgTTUuMj_KuQszUVPZqoE1UM'
```