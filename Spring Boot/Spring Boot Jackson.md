# Spring Boot Jackson

Spring Boot羡慕默认引入Jackson依赖，非Spring Boot则手动引入最新版本即可，避免高危漏洞。

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>${jackson.version}</version>
</dependency>
```

### 自定义配置

```java
@Configuration
public class JacksonConfig {
    @Bean
    @Primary
    @ConditionalOnMissingBean(ObjectMapper.class)
    public ObjectMapper jacksonObjectMapper(Jackson2ObjectMapperBuilder builder) {
        ObjectMapper objectMapper = builder.createXmlMapper(false).build();

        // 通过该方法对mapper对象进行设置，所有序列化的对象都将按改规则进行系列化
        // Include.Include.ALWAYS 默认
        // Include.NON_DEFAULT 属性为默认值不序列化
        // Include.NON_EMPTY 属性为 空（""） 或者为 NULL 都不序列化，则返回的json是没有这个字段的。这样对移动端会更省流量
        // Include.NON_NULL 属性为NULL 不序列化,就是为null的字段不参加序列化
        objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
        return objectMapper;
    }
}
```

### 序列化、反序列化
```
ObjectMapper mapper = new ObjectMapper();
// 反序列化时忽略不存在的JavaBean属性
mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
Book book = new Book(1, "Java核心技术", "authorName", "123456", Arrays.asList("Java", "Network"));
String json = mapper.writeValueAsString(book);
System.out.println(json);

Book bookEntity = mapper.readValue(json, Book.class);
System.out.println(bookEntity);
```
但jackson与fastjson不同的是，父类属性也可以反序列化。

### 字段映射
```
@JsonProperty(value="bookId")
private Integer id;
```

### 日期格式化
1. Date
   ```
   @JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
   private Date createTime;
   ```
2. LocalDateTime 详见<a href="###自定义序列化">自定义序列化</a><br/>

### 集合序列化
```
List<Book> bookList = mapper.readValue(bookListJson, new TypeReference<List<Book>>(){});
```

### 自定义序列化
```
@JsonSerialize(using = LocalDateTimeSerializer.class)
@JsonDeserialize(using = LocalDateTimeDeserializer.class)
private LocalDateTime updateTime;
```

LocalDateTimeSerializer
```
public class LocalDateTimeSerializer extends JsonSerializer<LocalDateTime> {
    
    @Override
    public void serialize(LocalDateTime localDateTime, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        jsonGenerator.writeString(formatter.format(localDateTime));
    }
}
```

LocalDateTimeDeserializer
```
public class LocalDateTimeDeserializer extends JsonDeserializer<LocalDateTime> {

    @Override
    public LocalDateTime deserialize(JsonParser jsonParser, DeserializationContext deserializationContext) throws IOException, JsonProcessingException {
        String text = jsonParser.getValueAsString();
        if (text == null || text.isEmpty()) return null;

        DateTimeFormatter df = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        LocalDateTime localDateTime;
        try {
            localDateTime = LocalDateTime.parse(text, df);
            return localDateTime;
        } catch (Exception e) {
            throw new JsonParseException(jsonParser, text, e);
        }
    }
}
```
