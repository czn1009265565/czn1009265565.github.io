# Spring Boot SpringDoc

新一代交互式文档

## 依赖配置

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-ui</artifactId>
    <version>1.6.15</version>
</dependency>
```


## application配置

```yaml
springdoc:
  api-docs:
    enabled: true
    path: /v3/api-docs
  swagger-ui:
    enabled: true
    path: /swagger-ui
```

## 注解映射

相较于Swagger UI，下表列出了SpringDoc对应的常用注解

|SpringFox|SpringDoc|
|---|---|
|@Api|@Tag|
|@ApiOperation(value="foo",notes="bar")|@Operation(summary="foo", description="bar")|
|@ApiModel|@Schema|
|@ApiModelProperty|@Schema|
|@ApiIgnore|@Parameter(hidden=true)|


访问 `http://localhost:8080/swagger-ui.html`

