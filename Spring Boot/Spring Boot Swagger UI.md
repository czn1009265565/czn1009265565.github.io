## Spring Boot 整合 Swagger UI

Swagger 交互式文档


### 依赖配置
适配Spring Boot 2.5.6

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>

<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
</dependency>
```

### application配置

```yaml
swagger:
  apiBasePackage: com.czndata.springboot.controller
  enableSwagger: true
  enableSecurity: true
  title: swagger-ui
  description: description
  version: 1.0.0
  contactName: zenan
  contactUrl: blog.czndata.cn
  contactEmail: 1009265565@qq.com
```

对应属性映射类 SwaggerProperties

```java
@Data
@Component
@ConfigurationProperties(prefix = "swagger")
public class SwaggerProperties {
    /**
     * API文档基础地址
     */
    private String apiBasePackage;

    /**
     * 是否启用Swagger
     */
    private boolean enableSwagger;

    /**
     * 是否启用登录认证
     */
    private boolean enableSecurity;

    /**
     * 文档标题
     */
    private String title;

    /**
     * 文档描述
     */
    private String description;

    /**
     * 文档版本
     */
    private String version;

    /**
     * 联系人姓名
     */
    private String contactName;

    /**
     * 联系人url
     */
    private String contactUrl;

    /**
     * 联系人邮箱
     */
    private String contactEmail;

}
```

### SwaggerConfig配置

```java
@Configuration
@EnableSwagger2
public class SwaggerConfig {

    @Resource
    private SwaggerProperties swaggerProperties;

    @Bean
    public Docket createRestApi(){

        return new Docket(DocumentationType.SWAGGER_2)
                .enable(swaggerProperties.isEnableSwagger())
                .apiInfo(apiInfo(swaggerProperties))
                .select()
                // 为当前包下controller生成API文档
                .apis(RequestHandlerSelectors.basePackage(swaggerProperties.getApiBasePackage()))
                // 为有@Api注解的Controller生成API文档
                // .apis(RequestHandlerSelectors.withClassAnnotation(Api.class))
                // 为有@ApiOperation注解的Controller生成API文档
                // .apis(RequestHandlerSelectors.withMethodAnnotation(ApiOperation.class))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo(SwaggerProperties swaggerProperties) {
        return new ApiInfoBuilder()
                .title(swaggerProperties.getTitle())
                .description(swaggerProperties.getDescription())
                .contact(new Contact(swaggerProperties.getContactName(), swaggerProperties.getContactUrl(), swaggerProperties.getContactEmail()))
                .version(swaggerProperties.getVersion())
                .build();
    }
}
```

### 注解
- @Api：修饰整个类，描述Controller的作用；
- @ApiOperation：描述一个类的一个方法，或者说一个接口；
- @ApiParam：单个参数描述；
- @ApiModel：用对象来接收参数；
- @ApiModelProperty：用对象接收参数时，描述对象的一个字段；
- @ApiResponse：HTTP响应其中1个描述；
- @ApiResponses：HTTP响应整体描述；
- @ApiIgnore：使用该注解忽略这个API；
- @ApiError ：发生错误返回的信息；
- @ApiImplicitParam：一个请求参数；
- @ApiImplicitParams：多个请求参数。

### 示例

```java
@Api(tags = "用户管理")
@RestController
@RequestMapping(value = "/user")
public class UserController {

    @GetMapping(value = "/list")
    @ApiOperation(value = "用户列表")
    public List<User> list(UserQueryParam userQueryParam){
        return new ArrayList<>();
    }

    @GetMapping(value = "/{id}")
    @ApiOperation(value = "获取用户信息", notes = "根据用户id获取用户信息", response = User.class)
    @ApiImplicitParam(name = "id", value = "用户id", required = true, dataType = "Long", paramType = "path")
    public User detail(@PathVariable(value = "id") Integer id){
        return new User();
    }
}
```

实体类

```java
@Data
@ApiModel(value = "用户实体类")
public class User {
    @ApiModelProperty(value = "id")
    private Integer id;

    @ApiModelProperty(value = "用户名")
    private String username;

    @ApiModelProperty(value = "手机号")
    private String mobile;
}

@Data
@ApiModel(value = "用户查询对象")
public class UserQueryParam {
    @ApiModelProperty(value = "用户名")
    private String username;

    @ApiModelProperty(value = "手机号")
    private String mobile;
}
```

访问 `http://localhost:8080/swagger-ui.html`


## 文档导出

### 引入依赖

```xml
<dependency>
    <groupId>io.github.swagger2markup</groupId>
    <artifactId>swagger2markup</artifactId>
    <version>1.3.3</version>
</dependency>
```

### 生成文档
本文介绍单元测试方式生成离线文档,注意点 需要先启动服务,再执行单元测试

```java
@SpringBootTest
public class SwaggerTest {

    @Test
    public void generateAsciiDocs() throws Exception {

        URL remoteSwaggerFile = new URL("http://localhost:8888/v2/api-docs");
        Path outputDirectory = Paths.get("src/docs/asciidoc/generated/document");

        Swagger2MarkupConfig config = new Swagger2MarkupConfigBuilder()
                // 指定输出格式 ASCIIDOC,MARKDOWN,CONFLUENCE_MARKUP
                .withMarkupLanguage(MarkupLanguage.ASCIIDOC)
                .build();

        Swagger2MarkupConverter
                // 指定了生成静态部署文档的源头配置
                .from(remoteSwaggerFile)
                .withConfig(config)
                .build()
                // 指定最终生成文件的具体目录位置
                .toFile(outputDirectory);
    }
}
```




