# Java JSON

JSON (JavaScript Object Notation,JS对象简谱)是一种轻量级的数据交换格式。采用完全独立于编程语言的文本格式来存储和表示数据。
简洁和清晰的层次结构使得JSON成为理想的数据交换语言。易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。

## JSON类库
以下是几个常用的JSON类库，推荐使用Jackson

- FastJson: 阿里巴巴开发的 JSON 库，性能优秀
- Jackson: 社区活跃，灵活且具有高性能
- Gson: 谷歌开发的 JSON 库，简洁易用


## FastJson

### 引入依赖

```xml
<dependency>
    <groupId>com.alibaba.fastjson2</groupId>
    <artifactId>fastjson2</artifactId>
    <version>${fastjson2.version}</version>
</dependency>
```

### 使用

自定义实体类

```java
@Data
public class FastJsonUser {
    @JSONField(name = "userId")
    private Long userId;

    @JSONField(name = "username")
    private String username;

    @JSONField(name = "password")
    private String password;

    @JSONField(name = "email")
    private String email;

    @JSONField(format = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

    @JSONField(format = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;
}
```

序列化及反序列化

```java
public class FastJsonTest {
    public static void main(String[] args) {
        // 序列化
        FastJsonUser fastJsonUser = new FastJsonUser();
        fastJsonUser.setUserId(1L);
        fastJsonUser.setUsername("Tom");
        fastJsonUser.setPassword("123456");
        fastJsonUser.setEmail("1@1.com");
        fastJsonUser.setCreateTime(new Date());
        fastJsonUser.setUpdateTime(LocalDateTime.now());
        String jsonString = JSON.toJSONString(fastJsonUser);
        System.out.println(jsonString);

        // 反序列化
        FastJsonUser user = JSON.parseObject(jsonString, FastJsonUser.class);

        // 反序列化JSONObject
        JSONObject jsonObject = JSON.parseObject(jsonString);
        Long userId = jsonObject.getLong("userId");
        String username = jsonObject.getString("username");

        // 反序列化集合对象
        String userListJson = "[{\"password\":\"123456\",\"userId\":1,\"username\":\"Tom\"}]";
        List<FastJsonUser> fastJsonUsers = JSON.parseObject(userListJson, new TypeReference<List<FastJsonUser>>() {});
        System.out.println(fastJsonUsers);
    }
}
```


## Jackson
Jackson 是用来序列化和反序列化 json 的 Java 开源框架

### 引入依赖

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.18.2</version>
</dependency>
```

### 使用

自定义实体类

```java
@Data
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

序列化及反序列化

```java
public class JacksonTest {
    public static void main(String[] args) throws JsonProcessingException {
        // 初始化
        ObjectMapper mapper = new ObjectMapper();

        // 序列化
        JacksonUser jacksonUser = new JacksonUser();
        jacksonUser.setUserId(1L);
        jacksonUser.setUsername("Tom");
        jacksonUser.setPassword("123456");
        jacksonUser.setEmail("1@1.com");
        jacksonUser.setCreateTime(new Date());
        jacksonUser.setUpdateTime(LocalDateTime.now());
        String value = mapper.writeValueAsString(jacksonUser);
        System.out.println(value);

        // 反序列化
        JacksonUser user = mapper.readValue(value, JacksonUser.class);

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

## GSON

### 引入依赖
```xml
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>${gson.version}</version>
</dependency>
```

### 使用

```java
public class GsonTest {

    public static void main(String[] args) {
        // 初始化
        Gson gson = new Gson();

        // 序列化
        // 基础类型
        System.out.println(gson.toJson(1));
        System.out.println(gson.toJson("a"));
        // 对象
        System.out.println(gson.toJson(new GsonUser()));
        // 数组
        System.out.println(gson.toJson(new int[]{1, 2, 3}));
        System.out.println(gson.toJson(new String[]{"abc", "def", "ghi"}));
        // 集合
        System.out.println(gson.toJson(Arrays.asList(1, 2, 3, 4, 5)));

        // 反序列化
        // 基础类型
        int one = gson.fromJson("1", int.class);
        Integer two = gson.fromJson("2", Integer.class);
        Boolean condition = gson.fromJson("false", Boolean.class);
        String str = gson.fromJson("\"abc\"", String.class);
        int[] intArr = gson.fromJson("[1,2,3,4,5]", int[].class);
        // 对象
        GsonUser gsonUser = gson.fromJson("{}", GsonUser.class);
        // 集合
        Type collectionType = new TypeToken<Collection<Integer>>() {}.getType();
        Collection<Integer> integerCollection = gson.fromJson("[1,2,3,4,5]", collectionType);
    }
}
```