# Spring Boot RestTemplate

### 认识RestTemplate
|方法名|描述|
|---|---|
|getForObject|通过 GET 请求获得响应结果|
|getForEntity|通过 GET 请求获取 ResponseEntity 对象，包容有状态码，响应头和响应数据|
|headForHeaders|以 HEAD 请求资源返回所有响应头信息|
|postForLocation|用 POST 请求创建资源，并返回响应数据中响应头的字段 Location 的数据|
|postForObject|通过 POST 请求创建资源，获得响应结果|
|put|通过 PUT 方式请求来创建或者更新资源|
|patchForObject|通过 PATH 方式请求来更新资源，并获得响应结果。(JDK HttpURLConnection 不支持 PATH 方式请求，其他 HTTP 客户端库支持)|
|delete|通过 DELETE 方式删除资源|
|optionsForAllow|通过 ALLOW 方式请求来获得资源所允许访问的所有 HTTP 方法，可用看某个请求支持哪些请求方式|
|exchange|更通用版本的请求处理方法，接受一个 RequestEntity 对象，可以设置路径，请求头，请求信息等，最后返回一个 ResponseEntity 实体|
|execute|最通用的执行 HTTP 请求的方法，上面所有方法都是基于 execute 的封装，全面控制请求信息，并通过回调接口获得响应数据|


### Get请求

定义：

```java
public interface RestOperations {
    <T> T getForObject(URI url, Class<T> responseType) throws RestClientException;

    <T> T getForObject(String url, Class<T> responseType, Map<String, ?> uriVariables) throws RestClientException;

    <T> ResponseEntity<T> getForEntity(URI url, Class<T> responseType) throws RestClientException;

    <T> ResponseEntity<T> getForEntity(String url, Class<T> responseType, Map<String, ?> uriVariables)
            throws RestClientException;
}
```

示例：

```java
public class RestTemplateTest {

    public static RestTemplate restTemplate = new RestTemplate();

    public static void main(String[] args) {
        String url = "http://api.mall.com/product/";
        Product product = restTemplate.getForObject(url, Product.class);

        ResponseEntity<Product> result = restTemplate.getForEntity(url, Product.class);
        int statusCodeValue = result.getStatusCodeValue();
        HttpHeaders headers = result.getHeaders();
        Product body = result.getBody();

        url = "http://api.mall.com/product/{productId}";
        product = restTemplate.getForObject(url, Product.class, Collections.singletonMap("productId", 1));
    }

    public static class Product{
        private String name;
    }
}
```

### Post请求

定义:

```java
public interface RestOperations {
    <T> T postForObject(URI url, @Nullable Object request, Class<T> responseType) throws RestClientException;

    <T> T postForObject(String url, @Nullable Object request, Class<T> responseType, Map<String, ?> uriVariables) throws RestClientException;

    <T> ResponseEntity<T> postForEntity(URI url, @Nullable Object request, Class<T> responseType) throws RestClientException;

    <T> ResponseEntity<T> postForEntity(String url, @Nullable Object request, Class<T> responseType,
    Map<String, ?> uriVariables) throws RestClientException;

}
```

示例:

```java
public class RestTemplateTest {

    public static RestTemplate restTemplate = new RestTemplate();

    public static void main(String[] args) {
        String url = "http://api.mall.com/product/";
        String body = restTemplate.postForObject(url, new Product(), String.class);
        ResponseEntity<String> response = restTemplate.postForEntity(url, new Product(), String.class);
    }
    
    public static class Product{
        private String name;
    }
}
```


### 配置项
```
@Bean
public RestTemplate restTemplate() {
    ClientHttpRequestFactory factory = simpleClientHttpRequestFactory();
    return new RestTemplate(factory);
}

private ClientHttpRequestFactory simpleClientHttpRequestFactory() {
    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
    // 读取超时 5s
    factory.setReadTimeout(5000);
    // 连接超时 10s
    factory.setConnectTimeout(10000);
    // 设置代理
    //factory.setProxy(null);
    return factory;
}
```