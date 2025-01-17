# Spring Security RBAC

RBAC（Role-Based Access Control）权限模型的概念，即：基于角色的权限控制。通过角色关联用户，角色关联权限的方式间接赋予用户权限。
## 表结构

| 实体                | 表                  | 说明         |
|-------------------|--------------------|------------|
| SysUserDO	        | sys_user	          | 用户信息       |
| SysRoleDO	        | sys_role	          | 用户角色       |
| SysUserRoleRelDO	 | sys_user_role_rel	 | 用户和角色关联表   |
| SysMenuDO	        | sys_menu	          | 菜单权限       |
| SysRoleMenuRelDO	 | sys_role_menu_rel	 | 角色和菜单权限关联表 |


### SysUserDO
```java
@Data
@NoArgsConstructor
public class SysUserDO {
    /** 用户编号 */
    private Long userId;
    /** 用户名 */
    private String username;
    /** 用户昵称 */
    private String nickname;
    /** 用户邮箱 */
    private String email;
    /** 手机号码 */
    private String mobile;
    /** 性别 1-男,2-女,3-未知 */
    private Integer sex;
    /** 用户头像 */
    private String avatar;
    /** 密码 */
    private String password;
    /** 最后登录IP */
    private String loginIp;
    /** 最后登录时间 */
    private LocalDateTime loginDate;
    /** 状态 0-正常,1-停用 */
    private Integer status;
    /** 是否删除 */
    private Integer deleted;
    /** 创建时间 */
    private LocalDateTime createTime;
    /** 更新时间 */
    private LocalDateTime updateTime;
}
```

建表语句

```sql
create table sys_user
(
    user_id     bigint(20) not null primary key comment '用户ID',
    username    varchar(30) not null comment '用户账号',
    nickname    varchar(30) not null comment '用户昵称',
    email       varchar(50)  default '' comment '用户邮箱',
    mobile varchar(11)  default '' comment '手机号码',
    sex         tinyint      default '0' comment '用户性别（0男 1女 2未知）',
    avatar      varchar(100) default '' comment '头像地址',
    password    varchar(100) default '' comment '密码',
    status      tinyint      default '0' comment '帐号状态（0正常 1停用）',
    deleted    tinyint     default '0' comment '删除标志（0代表存在 2代表删除）',
    login_ip    varchar(50)  default '' comment '最后登录IP',
    login_date  datetime comment '最后登录时间',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) engine=innodb comment = '用户信息表';
```

### SysRoleDO

```java
@Data
@NoArgsConstructor
public class SysRoleDO {
    /** 角色ID */
    private Long roleId;
    /** 角色名称 */
    private String roleName;
    /** 角色权限 */
    private String roleCode;
    /** 角色排序 */
    private String sort;
    /** 状态 0-正常,1-停用 */
    private Integer status;
    /** 是否删除 */
    private Integer deleted;
    /** 创建时间 */
    private LocalDateTime createTime;
    /** 更新时间 */
    private LocalDateTime updateTime;
}
```

建表语句
```sql
CREATE TABLE `sys_role`  (
  role_id bigint NOT NULL PRIMARY KEY COMMENT '角色ID',
  role_name varchar(30) NOT NULL COMMENT '角色名称',
  role_code varchar(100) NOT NULL COMMENT '角色权限',
  sort int NOT NULL COMMENT '显示顺序',
  status tinyint NOT NULL DEFAULT '0' COMMENT '角色状态（0正常 1停用）',
  deleted tinyint NOT NULL DEFAULT '0' COMMENT '是否删除',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB COMMENT = '角色信息表';
```

### SysUserRoleRelDO

```java
@Data
@NoArgsConstructor
public class SysUserRoleRelDO {
    private Long relId;
    /** 用户ID */
    private Long userId;
    /** 角色ID */
    private Long roleId;
    /** 是否删除 */
    private Integer deleted;
    /** 创建时间 */
    private LocalDateTime createTime;
    /** 更新时间 */
    private LocalDateTime updateTime;
}
```

建表语句

```sql
create table sys_user_role_rel (
  rel_id    bigint(20) not null primary key comment '关联ID',
  user_id   bigint(20) not null comment '用户ID',
  role_id   bigint(20) not null comment '角色ID',
  deleted tinyint NOT NULL DEFAULT '0' COMMENT '是否删除',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) engine=innodb comment = '用户和角色关联表';
```

### SysMenuDO

```java
@Data
@NoArgsConstructor
public class SysMenuDO {
    /** 菜单ID */
    private Long menuId;
    /** 菜单名称 */
    private String menuName;
    /** 父菜单ID */
    private Long parentId;
    /** 显示顺序 */
    private String sort;
    /** 路由地址 */
    private String path;
    /** 组件路径 */
    private String component;
    /** 类型（1-目录 2-菜单 3-按钮） */
    private Integer menuType;
    /** 权限 */
    private String permission;
    /** 菜单图标 */
    private String icon;
    /** 状态 0-正常,1-停用 */
    private Integer status;
    /** 是否删除 */
    private Integer deleted;
    /** 创建时间 */
    private LocalDateTime createTime;
    /** 更新时间 */
    private LocalDateTime updateTime;
}
```

建表语句

```sql
create table sys_menu
(
    menu_id     bigint(20) not null primary key comment '菜单ID',
    menu_name   varchar(50) not null comment '菜单名称',
    parent_id   bigint(20) default 0 comment '父菜单ID',
    sort        int(4) default 0 comment '显示顺序',
    path        varchar(200)         default '' comment '路由地址',
    component   varchar(255)         default null comment '组件路径',
    menu_type   tinyint              comment '菜单类型（1目录 2菜单 3按钮）',
    permission  varchar(100)         default null comment '权限标识',
    icon        varchar(100)         default '#' comment '菜单图标',
    status      tinyint     NOT NULL DEFAULT '0' COMMENT '角色状态（0正常 1停用）',
    deleted     tinyint     NOT NULL DEFAULT '0' COMMENT '是否删除',
    create_time datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) engine=innodb comment = '菜单权限表';
```

### SysRoleMenuRelDO

```java
@Data
@NoArgsConstructor
public class SysRoleMenuRelDO {
    /** 关联ID */
    private Long relId;
    /** 角色ID */
    private Long roleId;
    /** 菜单ID */
    private Long menuId;
    /** 是否删除 */
    private Integer deleted;
    /** 创建时间 */
    private LocalDateTime createTime;
    /** 更新时间 */
    private LocalDateTime updateTime;
}
```

建表语句

```sql
CREATE TABLE sys_role_menu_rel
(
    rel_id      bigint(20) NOT NULL PRIMARY KEY COMMENT '关联ID',
    role_id     bigint(20) NOT NULL COMMENT '角色ID',
    menu_id     bigint(20) NOT NULL COMMENT '菜单ID',
    deleted     tinyint  NOT NULL DEFAULT '0' COMMENT '是否删除',
    create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB COMMENT = '角色和菜单关联表';
```

### 初始化SQL

```sql
insert into sys_role(role_id,role_name,role_code,sort,status,deleted) values(1,'超级管理员','super_admin',1,0,0);
insert into sys_role(role_id,role_name,role_code,sort,status,deleted) values(2,'普通角色','common',1,0,0);

insert into sys_user(user_id,username,nickname,password) values (1,'admin','admin','$2a$10$05ANF09hggcuRmZvKj8iAehZ6bPARxgxt.PodMKDzf3Y.G/kumULK');
insert into sys_user(user_id,username,nickname,password) values (2,'test001','test001','$2a$10$05ANF09hggcuRmZvKj8iAehZ6bPARxgxt.PodMKDzf3Y.G/kumULK');
insert into sys_user(user_id,username,nickname,password) values (3,'test002','test002','$2a$10$05ANF09hggcuRmZvKj8iAehZ6bPARxgxt.PodMKDzf3Y.G/kumULK');

insert into sys_user_role_rel(rel_id,user_id,role_id) values (1,1,1),(2,2,2);

insert into sys_menu(menu_id,menu_name,permission) values (1,'用户列表','system:user:list');
insert into sys_menu(menu_id,menu_name,permission) values (2,'用户创建','system:user:create');
insert into sys_menu(menu_id,menu_name,permission) values (3,'用户更新','system:user:update');
insert into sys_menu(menu_id,menu_name,permission) values (4,'用户删除','system:user:delete');

insert into sys_role_menu_rel(rel_id,role_id,menu_id) values (1,2,1);
```

## 自定义登录用户 LoginUser

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoginUser implements UserDetails {
    private SysUserDO sysUserDO;
    private Set<String> roles;
    private Set<String> permissions;
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.emptyList();
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
        return sysUserDO.getStatus() == 0 && sysUserDO.getDeleted() == 0;
    }
}
```

## 用户加载
继承 `UserDetailsService` 接口，实现 `loadUserByUsername` 获得指定用户名对应的用户信息。
```java
@Component
public class UserDetailsServiceImpl implements UserDetailsService {

    @Resource
    private SysUserDao sysUserDao;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserDetails userDetails = createLoginUser(username);
        if (userDetails == null) {
            throw new UsernameNotFoundException("用户不存在");
        }
        return userDetails;
    }

    /** 封装登录用户 */
    public UserDetails createLoginUser(String username) {
        SysUserDO sysUserDO = sysUserDao.selectByUsername(username);
        if (Objects.isNull(sysUserDO)) return null;
        List<SysRoleDO> sysRoleDOList = sysUserDao.selectRoleByUserId(sysUserDO.getUserId());
        List<SysMenuDO> sysMenuDOList = sysUserDao.selectMenuByUserId(sysUserDO.getUserId());
        Set<String> roleSet = sysRoleDOList.stream().map(SysRoleDO::getRoleCode).collect(Collectors.toSet());
        Set<String> permissionSet = sysMenuDOList.stream().map(SysMenuDO::getPermission).collect(Collectors.toSet());
        return new LoginUser(sysUserDO, roleSet, permissionSet);
    }
}
```

### SysUserDao
```java
public interface SysUserDao extends BaseMapper<SysUserDO> {
    default SysUserDO selectByUsername(String username) {
        LambdaQueryWrapper<SysUserDO> lambdaQueryWrapper = new LambdaQueryWrapper<>();
        lambdaQueryWrapper.eq(SysUserDO::getUsername, username);
        return this.selectOne(lambdaQueryWrapper);
    }

    List<SysRoleDO> selectRoleByUserId(@Param("userId") Long userId);

    List<SysMenuDO> selectMenuByUserId(@Param("userId") Long userId);
}
```
### SysUserMapper.xml
```xml
<mapper namespace="com.example.securityrbac.dao.SysUserDao">
    <select id="selectRoleByUserId" resultType="com.example.securityrbac.entity.SysRoleDO">
        select sys_role.* from sys_user
        left join sys_user_role_rel on sys_user.user_id=sys_user_role_rel.user_id
        inner join sys_role on sys_user_role_rel.role_id=sys_role.role_id
        where sys_user.user_id=#{userId}
    </select>

    <select id="selectMenuByUserId" resultType="com.example.securityrbac.entity.SysMenuDO">
        select sys_menu.* from sys_user
        left join sys_user_role_rel on sys_user.user_id=sys_user_role_rel.user_id
        left join sys_role_menu_rel on sys_user_role_rel.role_id=sys_role_menu_rel.role_id
        inner join sys_menu on sys_role_menu_rel.menu_id=sys_menu.menu_id
        where sys_user.user_id=#{userId}
    </select>
</mapper>
```

## 自定义权限校验

```java
public interface PermissionService {
    /**
     * 判断是否有权限，任一一个即可
     *
     * @param permissions 权限
     * @return 是否
     */
    boolean hasAnyPermissions(String... permissions);

    /**
     * 判断是否有角色，任一一个即可
     *
     * @param roles 角色数组
     * @return 是否
     */
    boolean hasAnyRoles(String... roles);
}
```

```java
@Service("ps")
public class PermissionServiceImpl implements PermissionService{

    public static final String SUPER_ADMIN = "super_admin";

    /** 获取已登录用户 */
    public LoginUser obtainLoginUser() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication.getPrincipal() instanceof LoginUser) {
            return (LoginUser) authentication.getPrincipal();
        }
        return null;
    }

    @Override
    public boolean hasAnyPermissions(String... permissions) {
        LoginUser loginUser = obtainLoginUser();
        // 如果需要的权限为空，说明有权限
        if (ArrayUtil.isEmpty(permissions)) {
            return true;
        }
        Set<String> permissionSet = loginUser.getPermissions();
        // 情况一：遍历判断每个权限，如果有一满足，说明有权限
        for (String permission : permissions) {
            if (permissionSet.contains(permission)) {
                return true;
            }
        }
        // 情况二：如果是超管，也说明有权限
        Set<String> roleSet = loginUser.getRoles();
        return roleSet.contains(SUPER_ADMIN);
    }

    @Override
    public boolean hasAnyRoles(String... roles) {
        LoginUser loginUser = obtainLoginUser();
        Set<String> roleSet = loginUser.getRoles();
        for (String role : roles) {
            if (roleSet.contains(role)) {
                return true;
            }
        }
        return roleSet.contains(SUPER_ADMIN);
    }
}
```

## 自定义配置

```java
@Configuration
// 开启@PreAuthorize权限校验
@EnableGlobalMethodSecurity(prePostEnabled=true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Override
    protected void configure(HttpSecurity httpSecurity) throws Exception {
        httpSecurity.authorizeRequests()
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

## 自定义登录登出

### 集成Freemarker

```xml
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-freemarker</artifactId>
</dependency>
```

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
### 登录页

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

### 登出页

```html
<form action="/auth/logout" method="post">
    <input name="${_csrf.parameterName}" type="hidden" value="${_csrf.token}">
    <input id="exit" type="submit" value="退出">
</form>
```

## URL权限校验

```java
@RestController
@RequestMapping("user")
public class UserController {

    @GetMapping("/list")
    @PreAuthorize("@ps.hasAnyPermissions('system:user:list')")
    public String listUser(){
        return "success";
    }

    @GetMapping("/create")
    @PreAuthorize("@ps.hasAnyPermissions('system:user:create')")
    public String createUser(){
        return "success";
    }

    @GetMapping("/delete")
    @PreAuthorize("@ps.hasAnyRoles('super_admin')")
    public String deleteUser(){
        return "success";
    }
}
```