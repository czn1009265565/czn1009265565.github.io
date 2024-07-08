## Spring Boot 获取 Bean

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