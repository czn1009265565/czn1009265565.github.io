# JSONPath 最佳实践

JsonPath 是一种用于从 JSON 文档中提取数据的查询语言（类似于 XPath 对于 XML）

## 引入依赖

```xml
<!-- 核心库 -->
<dependency>
    <groupId>com.jayway.jsonpath</groupId>
    <artifactId>jsonpath</artifactId>
    <version>2.9.0</version>
</dependency>

<!-- 推荐使用 Jackson 作为底层 JSON 引擎, 以获得更好的性能、稳定性和功能 -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.17.2</version>
</dependency>
```

## JSONPath语法
JSON Path语法

| 语法                    | 含义                       |
|-----------------------|--------------------------|
| `$`                   | 表示根节点                    |
| `@`                   | 当前节点                     |
| `.<节点名称>`             | 	获取子节点                   |
| `[<节点名称1>(,<节点名称2>)]` | 	获取子节点，与点号不同，这里可以获取多个子节点 |
| `*`                   | 	匹配所有元素节点                |
| `..`	                 | 获取子孙节点，无论嵌套多少层，都可以获取到    |
| `[<下标1>(,<下标2>)]`     | 	表示一个或多个下标               |
| `[start:end:step]`    | 	表示切片语法                  |
| `[?(<表达式>)]`          | 	过滤器表达式，表达式结果必须是布尔值      |
| `()`	                 | 支持表达式计算                  |

## 基础表达式

```java
public static void basic() {
    String jsonString = "{\"store\": {\"books\": [{ \"title\": \"Java\", \"price\": 50 },{ \"title\": \"Python\", \"price\": 30 },{ \"title\": \"Go\", \"price\": 40 }], \"location\": \"北京\"}}";
    // 提取字段值
    String location = JsonPath.read(jsonString, "$.store.location");
    System.out.println(location);

    // 提取数组
    List<String> titles = JsonPath.read(jsonString, "$.store.books[*].title");
    System.out.println(titles);
    // 提取对象
    List<Map<String, Object>> books = JsonPath.read(jsonString, "$.store.books");
    System.out.println(books);

    // 递归搜索
    List<Double> prices = JsonPath.read(jsonString, "$..price");
    System.out.println(prices);

    // 条件筛选
    books = JsonPath.read(jsonString, "$.store.books[?(@.price > 35)]");
    System.out.println(books);
}
```

## 高级配置与最佳实践

### 自定义配置
```java
import com.jayway.jsonpath.Configuration;
import com.jayway.jsonpath.Option;
import com.jayway.jsonpath.spi.json.JacksonJsonProvider;
import com.jayway.jsonpath.spi.mapper.JacksonMappingProvider;

public class JsonPathConfig {
    // 创建全局单例配置
    public static final Configuration SAFE_CONFIG = Configuration.builder()
            .jsonProvider(new JacksonJsonProvider())
            .mappingProvider(new JacksonMappingProvider())
            .options(Option.SUPPRESS_EXCEPTIONS) // 路径不存在不抛异常
            .options(Option.DEFAULT_PATH_LEAF_TO_NULL) // 叶子节点不存在则返回null
            .build();
}
```

### 类型读取
使用 `TypeRef` 指定返回类型
```java
List<Map<String, Object>> books = JsonPath.using(JsonPathConfig.SAFE_CONFIG)
                .parse(jsonString)
                .read("$.store.books", new TypeRef<List<Map<String, Object>>>() {});
```

### 预编译
如果存在多次执行同一个 `JsonPath` 表达式（例如在循环中或处理多个文档），预编译该表达式能带来巨大的性能提升
```java
private static final JsonPath PRE_COMPILED_PATH = JsonPath.compile("$.store.books[?(@.price > 35)]");

public void processData(List<String> documents) {
    for (String document : documents) {
        List<Map<String, Object>> books = PRE_COMPILED_PATH.read(document, JsonPathConfig.SAFE_CONFIG);
    }
}
```

### 流式解析
如果 JSON 文档非常大（例如几百MB），使用 `JsonPath.parse(InputStream, Charset)` 而不是 `parse(String)`，它可以避免将整个字符串一次性加载到内存中。
```java
public static void processStream() {
    try (InputStream inputStream = new FileInputStream("huge-file.json")) {
        List<String> names = JsonPath.using(JsonPathConfig.SAFE_CONFIG)
                .parse(inputStream, String.valueOf(StandardCharsets.UTF_8))
                .read("$..name");
    } catch (Exception e){
        e.printStackTrace();
    }
}
```