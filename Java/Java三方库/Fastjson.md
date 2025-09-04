# Fastjson

Fastjson 是阿里巴巴开源的高性能 JSON 库，用于 Java 对象与 JSON 字符串之间的序列化和反序列化。
但由于严重的安全漏洞历史，以及生态兼容性问题，因此新项目不推荐使用。

## 引入依赖

新版本
```xml
<dependency>
    <groupId>com.alibaba.fastjson2</groupId>
    <artifactId>fastjson2</artifactId>
    <version>${fastjson2.version}</version>
</dependency>
```

老版本
```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>${fastjson.version}</version>
</dependency>
```

## 序列化
使用 `JSON.toJSONString()` 方法

### 序列化集合类
```java
public static void serializeCollection() {
    Map<String, Object> map = new HashMap<>();
    map.put("name", "Tom");
    map.put("age", 23);
    String jsonString = JSON.toJSONString(map);
    System.out.println(jsonString);
}
```

### 序列化实体类
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDO {
    @JSONField(name = "userId")
    private Long userId;

    @JSONField(name = "username")
    private String username;

    /**
     * 忽略序列化
     */
    @JSONField(serialize = false)
    private String password;

    /**
     * 处理日期格式
     */
    @JSONField(format = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

    @JSONField(format = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;
}
```

```java
public static void serializeEntity() {
    UserDO userDO = UserDO
            .builder()
            .userId(1L)
            .username("Tom")
            .password("123456")
            .createTime(new Date())
            .updateTime(LocalDateTime.now())
            .build();
    String userString = JSON.toJSONString(userDO);
    System.out.println(userString);
}
```

## 反序列化

使用 `JSON.parseObject()` 或 `JSON.parseArray()`

### 序列化实体类
```java
public static void deserializeEntity() {
    String jsonString = "{\"userId\":1,\"username\":\"Tom\"}";
    String jsonStringArray = "[{\"userId\":1,\"username\":\"Tom\"}]";

    UserDO user = JSON.parseObject(jsonString, UserDO.class);
    List<UserDO> users = JSON.parseArray(jsonStringArray, UserDO.class);
    System.out.println(user);
    System.out.println(users);
}
```

### 序列化泛型

```java
public static void deserializeCollection() {
    String jsonStringArray = "[{\"userId\":1,\"username\":\"Tom\"}]";
    List<UserDO> users = JSON.parseObject(jsonStringArray, new TypeReference<List<UserDO>>(){});
    System.out.println(users);
}
```

## JSONPath
JSONPath 通过路径表达式（类似文件路径）定位 JSON 中的字段或元素

| 表达式	           | 说明                  |
|----------------|---------------------|
| $              | 	根对象                |
| .key 或 ['key'] | 	取当前对象的字段（属性）       |
| [n]	           | 取数组的第 n 个元素（从 0 开始） |
| [*]	           | 匹配所有元素（通配符）         |
| ..key	         | 递归搜索所有子层级中的字段       |
| [start:end]	   | 数组切片（支持步长）          |
| [?(表达式)]	      | 过滤表达式（支持逻辑判断）       |

JSON样例数据
```json
{
  "store": {
    "books": [
      { "title": "Java", "price": 50 },
      { "title": "Python", "price": 30 },
      { "title": "Go", "price": 40 }
    ],
    "location": "北京"
  }
}
```

### 提取字段值
```java
String location = (String) JSONPath.eval(jsonString, "$.store.location");
```

### 提取数组
```java
List<String> titles = (List<String>) JSONPath.eval(jsonString, "$.store.books[*].title");
```

### 递归搜索
```java
List<Integer> prices = (List<Integer>) JSONPath.eval(jsonString, "$.store..price");
```

### 条件过滤

```java
List<Object> booksSingle = (List<Object>) JSONPath.eval(jsonString, "$.store.books[?(@.price > 35)]");
```

### 多条件过滤
```java
List<Object> booksMultiple = (List<Object>) JSONPath.eval(jsonString, "$.store.books[?(@.price > 30 && @.price < 45)]");
```

### 路径判断

```java
boolean exists = JSONPath.contains(jsonString, "$.store.books");
```