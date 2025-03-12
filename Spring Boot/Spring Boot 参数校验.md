# Spring Boot 参数校验

## 请求参数
Spring MVC接受允许以多种方式将客户端中的数据传送到控制器的处理方法中：

### @RequestParam 与 @ModelAttribute
`@RequestParam`: 适用于查询参数(GET请求)与表单数据(POST请求)

`@ModelAttribute`: 适用于将请求参数或表单字段绑定到一个模型对象

查询参数
```java
@RequestMapping(method=GET)
public ResponseVO list(
       @RequestParam("pageNum") Integer pageNum,
       @RequestParam("pageSize") Integer pageSize,
       @ModelAttribute UserParam userParam
){
   // ...
}
```

表单参数
```java
@PostMapping("/register")
public void register(@ModelAttribute UserParam userParam){
   // ...
}
```

同时上传文件和表单数据
```java
@RequestMapping(value = "/upload", method = RequestMethod.POST)
public UploadFileVO upload(@RequestParam("file") MultipartFile file, @ModelAttribute UserParam userParam) {
  // ...
}
```

### @PathVariable
用于提取URL路径参数

```java
@RequestMapping(value="/user/{id}",method=GET)
public ResponseVO user(
       @PathVariable("id") int id
){
   // ...
}
```

### @RequestBody
用于接收HTTP请求的body部分，通常用于POST、PUT等方法，接收JSON格式的数据

```java
@PostMapping("/register")
public void register(@RequestBody User user){
   // ...
}
```

### @RequestHeader
用于获取请求头中的信息

```java
@GetMapping(value = "/refreshToken")
public  ResponseVO refreshToken(@RequestHeader("Authorization") String token) {
    return ResponseVO.success();
}
```

## 参数校验

1. 引入依赖

```xml
<dependency>
   <groupId>javax.validation</groupId>
   <artifactId>validation-api</artifactId>
</dependency>

<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

2. 注解

| 注解           | 描述                                       |
|--------------|------------------------------------------|
| @AssertFalse | 所注解的元素必须为boolean类型，且值为false              |
| @AssertTrue  | 所注解的元素必须为boolean类型，且值为true               |
| @DecimalMax  | 所注解的元素必须是数字，且值小于等于给定的BigDecimalString值   |
| @DecimalMin  | 所注解的元素必须是数字，且值大于等于给定的BigDecimalString值   |
| @Digits      | 所注解的元素必须是数字,且值必须有指定的位数                   |
| @Future      | 所注解的元素必须是一个将来的日期                         |
| @Past        | 所注解的元素必须是一个已过去的日期                        |
| @Max         | 所注解的元素必须是数字,且值小于或等于给定的值                  |
| @Min         | 所注解的元素必须是数字,且值大于或等于给定的值                  |
| @NotNull     | 所注解的元素必须不能为null                          |
| @Null        | 所注解的元素必须为null                            |
| @Pattern     | 所注解的元素必须匹配给定的正则表达式                       |
| @Size        | 所注解的元素必须为String、集合或数组，且长度符合给定范围          |
| @NotEmpty    | 是不能为null并且长度必须大于0的                       |
| @NotBlank    | 只能作用在String上，不能为null，而且调用trim()后，长度必须大于0 |

**@NotEmpty用在集合类上面 @NotBlank用在String上面 @NotNull用在基本类型上**


## 自定义参数校验器


1. 参数注解

```java
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = {SpecialCharacterValidator.class})
public @interface SpecialCharacter {

    String message() default "com.example.validation.annotation";
    String pattern() default "";

    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};

}
```

2. 校验器

```java
public class SpecialCharacterValidator implements ConstraintValidator<SpecialCharacter, String> {
    private String pattern = "";

    @Override
    public void initialize(SpecialCharacter constraintAnnotation) {
        pattern = constraintAnnotation.pattern();
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext constraintValidatorContext) {
        boolean result = true;
        if (StringUtils.isNotEmpty(value)) {
            Pattern p = Pattern.compile(pattern);
            Matcher m = p.matcher(value);
            result = m.find();
        }
        return result;
    }
}
```

3. 请求参数

```java
@Data
public class QueryParam {
    @SpecialCharacter(pattern = "^([1][3,4,5,6,7,8,9])\\d{9}$", message = "手机号格式不合法")
    private String mobile;
    @SpecialCharacter(pattern = "^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$", message = "域名格式不合法")
    private String domain;
    @SpecialCharacter(pattern = "^((\\d{18})|([0-9x]{18})|([0-9X]{18}))$", message = "身份证不合法")
    private String idCard;
    @SpecialCharacter(pattern = "\\d{6}(?!\\d)", message = "邮政编码不合法")
    private String postalCode;
    @SpecialCharacter(pattern = "((?:(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d)))\\.){3}(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d))))", message = "IP 不合法")
    private String IP;
}
```

4. Controller层添加`@Validated`注解


## 异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 通用@validated表单参数异常处理
    @ExceptionHandler(value={BindException.class, ValidationException.class, MethodArgumentNotValidException.class})
    public ResponseVO notValidExceptionHandle(MethodArgumentNotValidException e) {
        BindingResult bindingResult = e.getBindingResult();
        String message = bindingResult.getFieldErrors()
                .stream()
                .findFirst()
                .map(FieldError::getDefaultMessage)
                .orElse(null);
        return new ResponseVO(ResultEnum.PARAM_ERROR.getCode(), message, null);
    }
}
```