# Spring Boot 配置加载

## `@Value`注入

### application配置

```yaml
wechat:
  appId: wechat-app-id
  appSecret: wechat-app-secret
  # 属性间引用
  openAppId: ${wechat.appId}
  openAppSecret: ${wechat.appSecret}
```

### 使用`@Value`读取配置

注意点:  
1. `@Value`注解只能读取单个配置进行赋值
2. 支持添加默认值，在属性名称后面使用冒号 `:default-value`
3. `@Value`注解只能用于被Spring管理的Bean使用
4. `@Value`注解可以用于字段、构造函数参数、方法参数和方法上
5. `@Value`注解不能在static修饰的字段上使用

```java
@Data
@Component
public class WechatAccountConfig {
    @Value("${wechat.appId}")
    private String appId;

    @Value("${wechat.appSecret}")
    private  String appSecret;
}
```

## `@ConfigurationProperties`注入

### 使用`@ConfigurationProperties`注解批量绑定

```java
@Data
@Component
@ConfigurationProperties(prefix = "wechat")
public class WechatAccountConfig {

    /** 公众平台id */
    private String appId;

    /** 公众平台密钥 */
    private String appSecret;

    /** 开放平台id */
    private String openAppId;

    /** 开放平台密钥 */
    private String openAppSecret;
}
```

## 使用Environment动态获取配置

```java
@Data
@Component
public class WechatAccountConfig {
    private String appId;
    private String appSecret;
    private String openAppId;
    private String openAppSecret;

    @Resource
    private Environment environment;

    @PostConstruct
    public void init() {
        appId = environment.getProperty("wechat.appId");
        appSecret = environment.getProperty("wechat.appSecret", "");
        openAppId = environment.getProperty("wechat.openAppId", String.class);
        openAppSecret = environment.getProperty("wechat.openAppSecret", String.class, "");
    }
}
```

除了自动装配方式，也可以从应用上下文中获取，这种方式适用于静态方法调用

```java
@Component
public class SpringUtils implements ApplicationContextAware {

    private static ApplicationContext applicationContext;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        if (SpringUtils.applicationContext == null) {
            SpringUtils.applicationContext = applicationContext;
        }
    }

    /** 获取applicationContext */
    public static ApplicationContext getApplicationContext() {
        Assert.notNull(applicationContext, "ApplicationContext is null!");
        return applicationContext;
    }

    /** 通过name获取 Bean. */
    public static Object getBean(String name) {
        return getApplicationContext().getBean(name);
    }

    /** 通过class获取Bean. */
    public static <T> T getBean(Class<T> clazz) {
        return getApplicationContext().getBean(clazz);
    }

    /** 通过name,以及Clazz返回指定的Bean */
    public static <T> T getBean(String name, Class<T> clazz) {
        return getApplicationContext().getBean(name, clazz);
    }


    public static String getProperty(String key) {
        return getApplicationContext().getEnvironment().getProperty(key);
    }

    public static String getProperty(String key, String defaultValue) {
        return getApplicationContext().getEnvironment().getProperty(key, defaultValue);
    }

    public static <T> T getProperty(String key, Class<T> targetType) {
        return getApplicationContext().getEnvironment().getProperty(key, targetType);
    }

    public static <T> T getProperty(String name, Class<T> clazz, T defaultValue) {
        return getApplicationContext().getEnvironment().getProperty(name, clazz, defaultValue);
    }
}
```

## Java原生方式获取

```java
@Component
public class JavaConfig {

    public Properties load() {
        String configPath = "menu.properties";
        Properties props = new Properties();
        InputStreamReader input = null;
        try {
            //通过类加载器来获取指定路径下的资源文件，并返回一个InputStream对象
            InputStream resourceAsStream = this.getClass().getClassLoader().getResourceAsStream(configPath);
            // 输入流 （字节流转字符流）
            input = new InputStreamReader(resourceAsStream, StandardCharsets.UTF_8);
            // 加载配置
            props.load(input);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } finally {
            if (input!=null)
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
        }
        return props;
    }
}
```


