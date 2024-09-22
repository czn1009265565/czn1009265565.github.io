# Java 注解

注解是一种特殊的接口，注解继承自 `java.lang.annotation.Annotation`

## 注解作用

1. 简化配置 (Spring Boot中XML配置项)
2. 简化代码 AOP

## 实现注解

这里以日志注解为例

```java
@Target({ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface SystemLog {
    /** 模块名称 */
    String module() default ""; 
    /** 方法名称 */
    String methods() default ""; 
    /** 描述说明 */
    String description() default ""; 
}
```

使用注解

```java
@RestController
public class ProductController {
    @SystemLog(module = "product", methods = "product.addProduct", description = "新增商品")
    public ResponseVO addProduct(AddProductVO addProductVO) {
        return new ResponseVO();
    }
}
```

## 元注解

### @Retention

Retention 是保留的意思，表明注解产生的时间范围。其值是 `java.lang.RetentionPolicy` 枚举。

- RetentionPolicy.SOURCE : 只在源代码级别保留有用，在编译期就丢弃了
- RetentionPolicy.CLASS ： 在编译期保留有效，在运行期（JVM中）开始丢弃；这是默认的保留策略
- RetentionPolicy.RUNTIME ： 在编译期、运行其都保留有效，所以可以在反射中使用

### @Target

@Target 标明注解使用约束的应用上下文，是数组形式，可以标记在多个范围中使用。值由 `java.lang.annotation.ElementType` 指定。

java.lang.annotation.ElementType 的可用值如下：

- TYPE ： 类、接口、注解、枚举的声明中
- FIELD ： 成员变量，包含枚举的常量的声明中
- METHOD ： 方法的声明中
- PARAMETER ： 正式的参数的声明中
- CONSTRUCTOR ： 构造器的声明中
- LOCAL_VARIABLE ： 局部变量的声明中
- ANNOTATION_TYPE ： 注解类型的声明中
- PACKAGE ： 包的声明中
- TYPE_PARAMETER ： 类型参数的声明中（since JDK8）
- TYPE_USE ： 类型的使用（since JDK8）

## 注解生效

注解仅仅是用作标记，要想它真实发挥作用，则需要利用Java反射机制编写注解解析器，用于业务需求。

```java
@Slf4j
@Aspect
@Component
public class WebLogAspect {

    @Pointcut("execution(public * com.example.controller.*.*(..))")
    public void pointCut(){};

    @Before("pointCut()")
    public void doBefore(JoinPoint joinPoint) {
    	// 获取Servlet
        HttpServletRequest request = OperationUtils.obtainServlet();
        // 获取URI路径
        String uri = request.getRequestURI();
        // 获取请求源IP
        String ip = OperationUtils.obtainIp(request);
        // 获取请求入参
        String params = OperationUtils.obtainRequestParam(joinPoint);
        log.info("Url:{} IP:{} args:{}", uri, ip, params);
    }
}
```