## Spring Boot 整合 Elasticsearch

这里ES版本选择7.17稳定版本

[ik分词插件下载](https://github.com/medcl/elasticsearch-analysis-ik)

### 依赖配置
```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
```

### application配置
```yaml
spring:
  elasticsearch:
    # ES 服务器地址
    uris: http://127.0.0.1:9200  
    # 可选配置
#     username: elastic
#     password: password
```

### 实体类
```
@Data
@Document(indexName = "product")
@Setting(shards = 1, replicas = 0)
public class EsProduct {
    @Id
    private Long id;

    @Field(type = FieldType.Long)
    private Long brandId;

    @Field(type = FieldType.Keyword)
    private String brandName;

    @Field(analyzer = "ik_max_word", type = FieldType.Text)
    private String name;

    @Field(analyzer = "ik_max_word", type = FieldType.Text)
    private String description;

    @Field(type = FieldType.Double)
    private BigDecimal price;

    @Field(type = FieldType.Date, format = DateFormat.date_hour_minute_second)
    private LocalDateTime createTime;
}
```

### Dao层
方法命名规则、分页规则 同Spring Boot Data Jpa
```
public interface EsProductRepository extends ElasticsearchRepository<EsProduct, Long> {

    List<EsProduct> findByName(String name);

    Page<EsProduct> findByName(String name, Pageable pageable);
    
    Page<EsProduct> findByNameOrDescription(String name, String description, Pageable pageable);
}
```

### NativeQuery
NativeQuery 是一个构建查询条件的工具类，通过编写和发送原生的查询 `DSL` 支持复杂查询。

```java
@Service
public class EsProductExtendRepository {

    @Autowired
    private ElasticsearchTemplate elasticsearchTemplate;

    public SearchHits<EsProduct> matchAll() {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        nativeQueryBuilder.withQuery(QueryBuilders.matchAll(builder -> builder));
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> matchAllWithPageable(Integer pageNum, Integer pageSize) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        // 分页
        Pageable pageable = PageRequest.of(pageNum, pageSize);
        nativeQueryBuilder.withPageable(pageable);
        nativeQueryBuilder.withQuery(QueryBuilders.matchAll(builder -> builder));
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> matchAllWithPageableSort(Integer pageNum, Integer pageSize) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        // 分页
        Pageable pageable = PageRequest.of(pageNum, pageSize);
        nativeQueryBuilder.withPageable(pageable);
        nativeQueryBuilder.withQuery(QueryBuilders.matchAll(builder -> builder));
        // 排序 优先级按先后顺序，越靠前优先级越高
        nativeQueryBuilder.withSort(Sort.by(Sort.Order.asc("price")));
        nativeQueryBuilder.withSort(Sort.by(Sort.Order.desc("_score")));

        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> matchQuery(String keyword) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        nativeQueryBuilder.withQuery(QueryBuilders.match(builder -> builder.field("name").query(keyword)));
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> multiMatchQuery(String keyword) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        nativeQueryBuilder.withQuery(QueryBuilders.multiMatch(builder -> builder.fields("name").query(keyword)));
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> boolQuery(String keyword) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        Query boolQuery = QueryBuilders.bool(builder -> {
            builder.must(QueryBuilders.match(b -> b.field("name").query(keyword)));
            builder.must(QueryBuilders.match(b -> b.field("description").query(keyword)));
            return builder;
        });
        nativeQueryBuilder.withQuery(boolQuery);
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> rangeQuery(LocalDateTime startTime, LocalDateTime stopTime) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        Query boolQuery = QueryBuilders.bool(builder -> {
            builder.must(QueryBuilders.range(b -> b.field("createTime").gte(JsonData.of(formatter.format(startTime)))));
            builder.must(QueryBuilders.range(b -> b.field("createTime").lte(JsonData.of(formatter.format(stopTime)))));
            return builder;
        });
        nativeQueryBuilder.withQuery(boolQuery);
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> filter(String keyword) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();

        Query boolQuery = QueryBuilders.bool(builder -> {
            builder.must(QueryBuilders.term(b -> b.field("name").value(keyword)));
            builder.must(QueryBuilders.term(b -> b.field("brandName").value(keyword)));
            return builder;
        });
        nativeQueryBuilder.withFilter(boolQuery);
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }

    public SearchHits<EsProduct> scoreQuery(String keyword) {
        NativeQueryBuilder nativeQueryBuilder = new NativeQueryBuilder();

        List<FunctionScore> functionScoreList = new ArrayList<>();
        functionScoreList.add(new FunctionScore.Builder()
                .filter(QueryBuilders.match(builder -> builder.field("name").query(keyword)))
                .weight(10.0)
                .build());
        functionScoreList.add(new FunctionScore.Builder()
                .filter(QueryBuilders.match(builder -> builder.field("description").query(keyword)))
                .weight(5.0)
                .build());
        FunctionScoreQuery.Builder functionScoreQueryBuilder = QueryBuilders.functionScore()
                .functions(functionScoreList)
                .scoreMode(FunctionScoreMode.Sum)
                .minScore(2.0);
        nativeQueryBuilder.withQuery(builder -> builder.functionScore(functionScoreQueryBuilder.build()));
        // 基于相关系数排序
        nativeQueryBuilder.withSort(Sort.by(Sort.Order.desc("_score")));
        NativeQuery nativeQuery = nativeQueryBuilder.build();
        return elasticsearchTemplate.search(nativeQuery, EsProduct.class);
    }
}
```
