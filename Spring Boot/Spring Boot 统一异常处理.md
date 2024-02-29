## Spring Boot 异常处理

### 前置类定义
1. 创建异常枚举类

```java
@Getter
public enum ResultEnum {

	SUCCESS(0, "success"),
	PARAM_ERROR(1, "参数异常"),
	NOT_FOUND(2, "数据不存在"),
	TIME_OUT(3, "已超时"),
	;
	private final Integer code;
	private final String msg;

	ResultEnum(Integer code, String msg) {
		this.code = code;
		this.msg = msg;
	}
}
```

2. 创建公共返回值

```java
@Data
public class ResponseVO<T> {
    private Integer code;
    private String msg;
    private T data;

    public ResponseVO() {
    }

    public ResponseVO(Integer code, String msg, T data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }

    public static <T> ResponseVO<T> success() {
        return new ResponseVO<>(ResultEnum.SUCCESS.getCode(), ResultEnum.SUCCESS.getMsg(), null);
    }

    public static <T> ResponseVO<T> success(T data) {
        return new ResponseVO<>(ResultEnum.SUCCESS.getCode(), ResultEnum.SUCCESS.getMsg(), data);
    }

    public static <T> ResponseVO<T> error(Integer code, String msg) {
        return new ResponseVO<>(code, msg, null);
    }

    public static <T> ResponseVO<T> error(ResultEnum resultEnum) {
        return new ResponseVO<>(resultEnum.getCode(), resultEnum.getMsg(), null);
    }
}
```
### 创建异常类
这里我们手动定义BusinessException,继承自RuntimeException.

```java
@Getter
public class BusinessException extends RuntimeException {

    private Integer code;
    private String msg;

    public BusinessException(Integer code, String msg) {
        super(msg);
        this.code = code;
        this.msg = msg;
    }

    public BusinessException(ResultEnum resultEnum) {
        super(resultEnum.getMsg());
        this.code = resultEnum.getCode();
        this.msg = resultEnum.getMsg();
    }
}
```

### 自定义异常捕获

```java
@Slf4j
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    @ResponseBody
    @ResponseStatus(HttpStatus.OK)
    public ResponseVO handleUserNotExistsException(BusinessException e) {
    	log.error("GlobalException :", e);
        return ResponseVO.error(e.getCode(), e.getMsg());
    }
}
```


