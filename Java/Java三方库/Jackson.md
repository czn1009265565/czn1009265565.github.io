# Jackson
Jackson 是 Java 生态中最主流、功能最强大的 JSON 处理库

- 核心模块 (jackson-core): 定义底层流式 API
- 注解模块 (jackson-annotations): 提供注解支持
- 数据绑定模块 (jackson-databind): 提供对象与 JSON 的相互转换（最常用）

## 引入依赖

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>${jackson.version}</version>
</dependency>
```

##  核心功能与基本用法
ObjectMapper 是 Jackson 的核心，负责序列化（Java → JSON）和反序列化（JSON → Java）

```java
ObjectMapper mapper = new ObjectMapper();
```

### 自定义实体类

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JacksonUser {
    @JsonProperty(value = "userId")
    private Long userId;

    @JsonProperty(value = "username")
    private String username;

    @JsonProperty(value = "password")
    private String password;

    @JsonProperty(value = "email")
    private String email;

    @JsonProperty(value = "createTime")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

    @JsonProperty(value = "updateTime")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @JsonDeserialize(using = LocalDateTimeDeserializer.class)
    @JsonSerialize(using = LocalDateTimeSerializer.class)
    private LocalDateTime updateTime;
}
```


### 序列化与反序列化
```java
public class JacksonTest {
    public static void main(String[] args) throws JsonProcessingException {
        // 初始化
        ObjectMapper mapper = new ObjectMapper();

        // 序列化
        JacksonUser jacksonUser = JacksonUser
                .builder()
                .userId(1L)
                .username("Tom")
                .password("123456")
                .email("1@1.com")
                .createTime(new Date())
                .updateTime(LocalDateTime.now())
                .build();
        String jsonValue = mapper.writeValueAsString(jacksonUser);
        System.out.println(jsonValue);

        // 反序列化
        JacksonUser user = mapper.readValue(jsonValue, JacksonUser.class);

        // 反序列化集合对象
        String userListJson = "[{\"password\":\"123456\",\"userId\":1,\"username\":\"Tom\"}]";
        List<JacksonUser> jacksonUsers = mapper.readValue(userListJson, new TypeReference<List<JacksonUser>>() {});
        System.out.println(jacksonUsers);
    }
}
```

### 注解

- `@JsonProperty`: 将当前的属性名在 JSON 字符串中重新命名为当前设置的这个值
- `@JsonIgnore`: 将被标注的属性在生成 JSON 字符串的时候，直接忽略
- `@JsonInclude`: 控制字段在序列化时是否包含到 JSON 中，例如 JsonInclude.Include.NON_NULL排除null值，JsonInclude.Include.NON_EMPTY排除排除null或空值
- `@JsonSerialize`: 使用自定义的类来实现自定义的字段转换。写入操作
- `@JsonDeserialize`: 解析的时候，自定义的转换器；读取操作
- `@JsonAutoDetect`: 设置类的访问策略，是否所有的属性都可以，还是按照一定的方式来提取
- `@JsonRawValue`: 无转换的将属性值写入到json 字符串中。 写入操作
- `@JsonValue`: 标注方法，用以替代缺省的方法，由该方法来完成json的字符输出