# Spring Boot SpringDoc

新一代交互式文档

## 依赖配置

```xml
<dependencys>
    <!-- Spring Boot 2.X-->
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-ui</artifactId>
        <version>1.8.0</version>
    </dependency>

    <!-- Spring Boot 3.X-->
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>2.6.0</version>
    </dependency>
</dependencys>
```


## application配置

```yaml
springdoc:
  api-docs:
    enabled: true
    path: /v3/api-docs
  swagger-ui:
    enabled: true
```

默认地址: `http://localhost:8080/swagger-ui/index.html`

## 注解映射

相较于Swagger UI，下表列出了SpringDoc对应的常用注解

|SpringFox|SpringDoc|
|---|---|
|@Api|@Tag|
|@ApiOperation|@Operation|
|@ApiModel|@Schema|
|@ApiModelProperty|@Schema|
|@ApiIgnore|@Parameter(hidden=true)|

### 接口定义

```java
@Tag(name = "AdminControllerApi", description = "管理员管理")
public interface AdminControllerApi {

    @Operation(summary = "添加用户",
            description = "根据姓名添加用户并返回")
    CommonResult<User> addUser(String name);
}
```

### 实体类定义

```java
@Data
@AllArgsConstructor
@Schema(name = "CommonResult", description = "通用返回对象")
public class CommonResult<T> {
    @Schema(name = "code", description = "状态码")
    private long code;

    @Schema(name = "message", description = "提示信息")
    private String message;

    @Schema(name = "data", description = "数据封装")
    private T data;
}
```


