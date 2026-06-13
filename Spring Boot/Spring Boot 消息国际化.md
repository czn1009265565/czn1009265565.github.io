# Spring Boot 消息国际化

国际化 (Internationalization，简称 i18n) 是指软件应用在设计和开发阶段，就具备支持多种语言和地区格式的能力，而无需对代码进行大规模修改

## 解决的问题

1. 硬编码文本: 代码中充斥着中文或英文字符串
2. 格式混乱: 不同国家的数据格式不同
3. 业务逻辑与展示耦合

## 基础配置

### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

### 消息文件

- messages.properties          # 默认语言
- messages_zh_CN.properties    # 简体中文
- messages_en.properties       # 英语
- messages_fr.properties       # 法语

messages_zh_CN.properties
```properties
welcome=欢迎访问
user.notfound=用户 {0} 不存在
error.invalid=输入数据无效
```

messages_en.properties
```properties
welcome.message=Welcome
user.notfound=User {0} not found
error.invalid.input=Invalid input data
```

### application.properties

```properties
spring.messages.basename=i18n/messages
spring.messages.encoding=UTF-8
spring.messages.cache-duration=3600
```

### 自定义配置类

```java
@Configuration
public class I18nConfig {

    @Bean
    public LocaleResolver localeResolver() {
        // AcceptHeaderLocaleResolver acceptHeaderLocaleResolver = new AcceptHeaderLocaleResolver();
        // SessionLocaleResolver localeResolver = new SessionLocaleResolver();
        CookieLocaleResolver resolver = new CookieLocaleResolver();
        // Cookie 名称
        resolver.setCookieName("lang");
        // 有效期 30 天
        resolver.setCookieMaxAge(3600 * 24 * 30);
        // 默认语言
        resolver.setDefaultLocale(Locale.CHINA);
        return resolver;
    }
}
```

| 特性    | 	CookieLocaleResolver | 	SessionLocaleResolver | 	FixedLocaleResolver | 	AcceptHeaderLocaleResolver (默认) |
|-------|-----------------------|------------------------|----------------------|----------------------------------|
| 存储位置  | 	客户端 Cookie           | 	服务器 Session           | 	代码硬编码               | 	HTTP 请求头 (Accept-Language)      |
| 持久性   | 	高 (可跨浏览器会话)          | 	中 (仅限当前 Session)      | 	永久 (不可变)            | 	无 (每次请求重新协商)                    |
| 分布式友好 | 	✅ 是 (无状态)            | 	❌ 否 (需 Session 共享)	   | ✅ 是                  | 	✅ 是                             |
| 用户可控性 | 	✅ 用户可手动清除/修改         | 	❌ 用户难以直接修改            | 	❌ 不可控               | 	✅ 由浏览器设置决定                      |
| 典型场景	 | 电商、门户、C端产品            | 	后台管理、B端系统             | 	单语言内部系统             | 	REST API、默认行为                   |


## Controller使用

### 获取国际化消息

```java
@RestController
public class GreetingController {

    @Resource
    private MessageSource messageSource;

    @GetMapping("/getWelcome")
    public String getWelcome() {
        Locale locale = LocaleContextHolder.getLocale();
        return messageSource.getMessage("welcome", null, locale);
    }
}
```

### 修改语言

```java
@RestController
public class LanguageController {

    @Autowired
    private LocaleResolver localeResolver;

    @GetMapping("/changeLang")
    public String changeLang(@RequestParam String lang, HttpServletRequest request, HttpServletResponse response) {
        Locale locale;
        if ("zh".equalsIgnoreCase(lang)) {
            locale = Locale.CHINA;
        } else {
            locale = Locale.US;
        }
        localeResolver.setLocale(request, response, locale);
        return "success";
    }
}
```

### 异常处理

```java
@Data
public class UserCreateReqVO {
    @NotBlank(message = "{error.invalid}")
    private String name;
}
```

拦截器
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @Resource
    private MessageSource messageSource;

    /**
     * 处理 @RequestBody 参数校验失败 (@Valid)
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationExceptions(
            MethodArgumentNotValidException ex) {

        Map<String, String> errors = getValidationErrors(ex.getBindingResult().getFieldErrors());

        Map<String, Object> body = new HashMap<>();
        body.put("code", 400);
        body.put("message", "Validation Failed");
        body.put("errors", errors);

        return ResponseEntity.badRequest().body(body);
    }

    /**
     * 处理表单参数校验失败 (@Validated on GET params etc.)
     */
    @ExceptionHandler(BindException.class)
    public ResponseEntity<Map<String, Object>> handleBindExceptions(
            BindException ex) {

        Map<String, String> errors = getValidationErrors(ex.getBindingResult().getFieldErrors());

        Map<String, Object> body = new HashMap<>();
        body.put("code", 400);
        body.put("message", "Validation Failed");
        body.put("errors", errors);

        return ResponseEntity.badRequest().body(body);
    }

    /**
     * 核心方法：将 FieldError 列表转换为 Map<字段名, 国际化消息>
     */
    private Map<String, String> getValidationErrors(List<FieldError> fieldErrors) {
        // 获取当前请求的 Locale (由 LocaleResolver 决定，如 zh_CN 或 en_US)
        var locale = LocaleContextHolder.getLocale();

        return fieldErrors.stream()
                .collect(Collectors.toMap(
                        FieldError::getField,
                        fieldError -> {
                            // 1. 获取 defaultMessage (通常是 messages.properties 中的 Key 或硬编码消息)
                            String code = fieldError.getDefaultMessage();

                            // 2. 尝试从 MessageSource 中解析国际化消息
                            // 如果 code 是一个 Key (如 user.name.NotNull)，它会去 properties 文件找
                            // 如果 code 是硬编码文本，getMessage 会原样返回（因为找不到 Key）
                            try {
                                return messageSource.getMessage(code, fieldError.getArguments(), locale);
                            } catch (Exception e) {
                                // 如果解析失败，返回原始消息
                                return code;
                            }
                        },
                        // 如果一个字段有多个错误，保留第一个
                        (existing, replacement) -> existing
                ));
    }
}
```