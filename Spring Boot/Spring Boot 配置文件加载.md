


## 自定义加载配置文件
**这里通过Spring 启动任务的方式，加载配置文件内容到运行环境中**  
```java
@Component
public class TestFileApplicationListener implements ApplicationListener<ContextRefreshedEvent> {

    private final Properties properties = new Properties();
    private final String propertiesFile = "test.properties";

    @Resource
    private Environment environment;

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        ClassLoader contextClassLoader = Thread.currentThread().getContextClassLoader();
        // 加载配置文件
        URL url = contextClassLoader.getResource(propertiesFile);
        Assert.notNull(url, "配置文件路径不存在!");
        org.springframework.core.io.Resource resource = new UrlResource(url);
        try {
            // 查看源码，根据 =或:来切割成键值对
            properties.load(resource.getInputStream());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        ConfigurableEnvironment configurableEnvironment = (ConfigurableEnvironment) environment;
        configurableEnvironment.getPropertySources().addFirst(new PropertiesPropertySource(propertiesFile, properties));
    }
}
```

**配置获取**  
```java
@RestController
public class TestController {
    @Resource
    private Environment environment;

    @GetMapping("test")
    public String test() {
        return environment.getProperty("test.value");
    }
}
```