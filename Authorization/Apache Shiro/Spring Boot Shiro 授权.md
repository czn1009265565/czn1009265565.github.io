## Spring Boot Shiro 授权


### 获取用户角色和权限

```java
public class UsernamePasswordRealm extends AuthorizingRealm {
    /**
     * 获取用户角色和权限
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        SimpleAuthorizationInfo simpleAuthorizationInfo = new SimpleAuthorizationInfo();

        String username = (String) SecurityUtils.getSubject().getPrincipal();
        // 查询用户角色集
        Set<String> roleList = new HashSet<>(Arrays.asList("user", "admin"));
        // 根据角色集查询用户权限集
        Set<String> permissionList = new HashSet<>(Arrays.asList("create", "retrieve", "update", "delete"));
        simpleAuthorizationInfo.setRoles(roleList);
        simpleAuthorizationInfo.setStringPermissions(permissionList);
        return simpleAuthorizationInfo;
    }

    // ...... 	
}
```

### 授权方式

1. 代码方式

```java
Subject subject = SecurityUtils.getSubject();  
if(subject.hasRole("admin") && subject.isPermitted("create")) {  
    //有权限  
} else {  
    //无权限  
}
```

2. 注解方式

```language
// 表示当前Subject需要角色admin和user。  
@RequiresRoles(value={"admin", "user"}, logical= Logical.AND)  

// 表示当前Subject需要权限create或update。
@RequiresPermissions (value={"create", "update"}, logical= Logical.OR)
```

要开启这些注解的使用，需要在ShiroConfig中添加如下配置,且需要引入AOP依赖

```java
@Bean
public AuthorizationAttributeSourceAdvisor authorizationAttributeSourceAdvisor(SecurityManager securityManager) {
    AuthorizationAttributeSourceAdvisor authorizationAttributeSourceAdvisor = new AuthorizationAttributeSourceAdvisor();
    authorizationAttributeSourceAdvisor.setSecurityManager(securityManager);
    return authorizationAttributeSourceAdvisor;
}
```

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```
