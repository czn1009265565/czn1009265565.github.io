# Spring Boot Jackson

Spring Boot默认引入Jackson依赖，非Spring Boot则手动引入最新版本即可，避免高危漏洞。

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
      ObjectMapper objectMapper = builder.build();

      objectMapper.setDateFormat(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));
      // 设置反序列化时忽略未知属性(否则存在未知属性时会抛出异常)
      objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
      // 设置为null的字段不参加序列化
      objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
      // 添加Java8时间模块支持
      objectMapper.registerModule(new JavaTimeModule());

      return objectMapper;
   }
}
```

### 序列化、反序列化
```
ObjectMapper mapper = new ObjectMapper();
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
```java
public class LocalDateTimeSerializer extends JsonSerializer<LocalDateTime> {
    
    @Override
    public void serialize(LocalDateTime localDateTime, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        jsonGenerator.writeString(formatter.format(localDateTime));
    }
}
```

LocalDateTimeDeserializer
```java
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
