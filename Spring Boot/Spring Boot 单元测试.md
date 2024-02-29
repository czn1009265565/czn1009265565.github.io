## Spring Boot 单元测试


### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <scope>test</scope>
</dependency>
```


### 功能测试

实现service层的功能测试.

Junit4

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class JunitTest {

    @Test
    public void test() {
        System.out.println("junit test");
    }
}
```

Junit5

```java
@SpringBootTest
public class JunitTest {

    @Test
    public void test() {
        System.out.println("junit test");
    }
}
```


### 接口测试
实现controller层的测试.


```java
@SpringBootTest
@AutoConfigureMockMvc
class JunitControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Before
    static void init() {
        // 设置全局token数据
    }

    @Test
    void testPath() throws Exception {
        // 路径参数
        String pathParamUrl = "/junit/path/{path}";
        mockMvc.perform(
                        MockMvcRequestBuilders.get(pathParamUrl, "1")
                                .accept(MediaType.APPLICATION_JSON_VALUE)
                                .contentType(MediaType.APPLICATION_JSON))
                // 期望结果 200
                .andExpect(MockMvcResultMatchers.status().isOk())
                // 打印结果
                .andDo(MockMvcResultHandlers.print())
                .andReturn();
    }

    @Test
    void testQuery() throws Exception {
        // 查询参数
        String queryParamUrl = "/junit/query";
        mockMvc.perform(
                        MockMvcRequestBuilders.get(queryParamUrl)
                                .accept(MediaType.APPLICATION_JSON_VALUE)
                                .contentType(MediaType.APPLICATION_JSON)
                                .param("param", "param")
                )
                // 期望结果 200
                .andExpect(MockMvcResultMatchers.status().isOk())
                // 打印结果
                .andDo(MockMvcResultHandlers.print())
                .andReturn();
    }

    @Test
    void testJson() throws Exception {
        // Json 请求
        String jsonParamUrl = "/junit/json";
        ObjectMapper objectMapper = new ObjectMapper();
        String p = objectMapper.writeValueAsString(new Person("Tom", "male"));
        mockMvc.perform(
                        MockMvcRequestBuilders.post(jsonParamUrl)
                                .accept(MediaType.APPLICATION_JSON_VALUE)
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(p)
                )
                // 期望结果 200
                .andExpect(MockMvcResultMatchers.status().isOk())
                // 打印结果
                .andDo(MockMvcResultHandlers.print())
                .andReturn();
    }
}
```