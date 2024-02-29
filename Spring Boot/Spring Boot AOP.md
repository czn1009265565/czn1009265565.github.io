# Spring Boot AOP

Spring 的核心就是AOP 和 IOC, AOP即面向切面编程

## 常用AOP通知类型

1. 前置通知：在目标方法调用之前调用通知
2. 后置通知：在目标方法调用之后调用通知，此时不会关心方法的输出是什么
3. 返回通知：在目标方法成功执行之后调用通知
4. 异常通知：在目标方法抛出异常后调用通知
5. 环绕通知：通知包裹了被通知方法，在被通知的方法调用之前和之后执行自定义的行为

相关注解:

- `@Aspect`：用于定义切面
- `@Before`：通知方法会在目标方法调用之前执行
- `@After`：通知方法会在目标方法返回或抛出异常后执行
- `@AfterReturning`：通知方法会在目标方法返回后执行
- `@AfterThrowing`：通知方法会在目标方法抛出异常后执行
- `@Around`：通知方法会将目标方法封装起来
- `@Pointcut`：定义切点表达式

表达式标签:

1. `execution()`: 用于匹配方法执行的连接点
2. `args()`: 用于匹配当前执行的方法传入的参数为指定类型的执行方法
3. `this()`: 用于匹配当前AOP代理对象类型的执行方法；注意是AOP代理对象的类型匹配，这样就可能包括引入接口也类型匹配
4. `target()`: 用于匹配当前目标对象类型的执行方法；注意是目标对象的类型匹配，这样就不包括引入接口也类型匹配
5. `within()`: 用于匹配指定类型内的方法执行
6. `@args()`: 于匹配当前执行的方法传入的参数持有指定注解的执行
7. `@target()`: 用于匹配当前目标对象类型的执行方法，其中目标对象持有指定的注解
8. `@within()`: 用于匹配所有持有指定注解类型内的方法
9. `@annotation`: 用于匹配当前执行方法持有指定注解的方法

## Spring Boot 集成

### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

### 反射工具类
```java
public class OperationUtils {

    /** 获取登录用户名 */
    public static String obtainUsername(){
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication.getPrincipal() instanceof UserDetails) {
            UserDetails userDetails = (UserDetails) authentication.getPrincipal();
            return userDetails.getUsername();
        }
        return "";
    }

    /** 获取操作描述 */
    public static String obtainDescription(ProceedingJoinPoint joinPoint){
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Method method = signature.getMethod();
        Operation operation = method.getAnnotation(Operation.class);
        return operation.value();
    }

    /** 获取方法名 */
    public static String obtainMethodName(ProceedingJoinPoint joinPoint){
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        return joinPoint.getTarget().getClass().getName() + "." + signature.getName() + "()";
    }

    /** 获取servlet */
    public static HttpServletRequest obtainServlet(){
        return ((ServletRequestAttributes) Objects.requireNonNull(RequestContextHolder.getRequestAttributes())).getRequest();
    }

    /** 获取浏览器 */
    public static String obtainBrowser(HttpServletRequest request){
        UserAgent userAgent = UserAgent.parseUserAgentString(request.getHeader("User-Agent"));
        Browser browser = userAgent.getBrowser();
        return browser.getName();
    }

    /** 获取真实ip */
    public static String obtainIp(HttpServletRequest request){
        String ip = request.getRemoteAddr();
        // 获取经过Nginx代理后的真实用户ip
        String forwarded = request.getHeader("X-Forwarded-For");
        String real = request.getHeader("X-Real-IP");
        if (!StringUtils.isEmpty(forwarded) && !"unknown".equals(forwarded)) return forwarded;
        if (!StringUtils.isEmpty(real) && !"unknown".equals(real)) return real;
        return ip;
    }

    /** 获取请求参数 */
    public static String obtainRequestParam(JoinPoint joinPoint){
        Object[] args = joinPoint.getArgs();
        LocalVariableTableParameterNameDiscoverer u = new LocalVariableTableParameterNameDiscoverer();
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Method method = signature.getMethod();
        String[] paramNames = u.getParameterNames(method);

        StringBuilder params = new StringBuilder();
        if (args != null && paramNames != null) {
            for (int i = 0; i < args.length; i++) {
                params.append("  ").append(paramNames[i]).append(": ").append(args[i]);
            }
        }
        return params.toString();
    }
}
```
### 执行用时记录
注解
```java
@Documented
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TimeLog {
}
```

切面
```java
@Slf4j
@Aspect
@Component
public class TimeLogAspect {

    @Pointcut("@annotation(com.example.test.annotation.TimeLog)")
    public void pointCut(){}


    @Around("pointCut()")
    public Object doAround(ProceedingJoinPoint joinPoint) throws Throwable {
        Long startTime = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        Long endTime = System.currentTimeMillis();
        Long costTime = endTime - startTime;
        Method method = getMethod(joinPoint);
        log.info("methodName: {}, costTime {}ms", method.getName(),costTime);
        return result;
    }

    /** 获取当前执行的方法 */
    private Method getMethod(ProceedingJoinPoint point) throws NoSuchMethodException {
        MethodSignature methodSignature = (MethodSignature) point.getSignature();
        Method method = methodSignature.getMethod();
        return point.getTarget().getClass().getMethod(method.getName(), method.getParameterTypes());
    }
}
```


### 日志打印(前置通知)

```java
@Slf4j
@Aspect
@Component
public class WebLogAspect {

    @Pointcut("execution(public * com.czndata.blog.web.controller.*.*(..))")
    public void pointCut(){};

    @Before("pointCut()")
    public void doBefore(JoinPoint joinPoint) {
        HttpServletRequest request = OperationUtils.obtainServlet();
        String uri = request.getRequestURI();
        String ip = OperationUtils.obtainIp(request);
        String params = OperationUtils.obtainRequestParam(joinPoint);
        log.info("Url:{} IP:{} args:{}", uri, ip, params);
    }
}
```

### 操作记录(环绕通知)

```java
@Slf4j
@Aspect
@Component
public class OperationAspect {
    @Autowired
    private OperationService operationService;

    @Pointcut("@annotation(com.czndata.znfund.logging.annotation.Operation)")
    public void pointCut(){}

    @Around("pointCut()")
    public Object operationAround(ProceedingJoinPoint joinPoint) throws Throwable {
        Object result = joinPoint.proceed();
        operationService.create(joinPoint);
        return result;
    }

    @AfterThrowing(pointcut = "pointCut()", throwing = "e")
    public void operationThrowing(JoinPoint joinPoint, Throwable e){
        operationService.create((ProceedingJoinPoint) joinPoint, e);
    }
}
```

