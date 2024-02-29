## Spring Boot 整合 Elasticsearch

[ik分词插件下载](https://github.com/medcl/elasticsearch-analysis-ik)

### 依赖配置
```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
```

### application配置
```
spring:
  elasticsearch:
    rest:
      uris: 127.0.0.1:9200
#       username: elastic
#       password: password
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

    @Field(type = FieldType.Long)
    private Long createTime;

    public EsProduct() {
    }

    public EsProduct(Long id, Long brandId, String brandName, String name, String description, BigDecimal price) {
        this.id = id;
        this.brandId = brandId;
        this.brandName = brandName;
        this.name = name;
        this.description = description;
        this.price = price;
    }
}
```

### Dao层
方法命名规则、分页规则 同Spring Boot Data Jpa
```
public interface EsProductRepository extends ElasticsearchRepository<EsProduct, Long> {

    List<EsProduct> findByName(String name);

    Page<EsProduct> findByName(String name, Pageable pageable);
}
```

### 底层API
当模板查询方法没办法满足我们的要求时,我们可以使用ElasticsearchRestTemplate,RestHighLevelClient等更为底层的方法实现

EsProductExtendRepository
```
public interface EsProductExtendRepository {
    
    List<EsProduct> findByCondition(EsProduct esProduct, Integer pageNum, Integer pageSize);

}
```

EsProductExtendRepositoryImpl
```
@Service
public class EsProductExtendRepositoryImpl implements EsProductExtendRepository{

    @Autowired
    private ElasticsearchRestTemplate elasticsearchRestTemplate;

    @Override
    public List<EsProduct> findByCondition(EsProduct esProduct, Integer pageNum, Integer pageSize) {
        BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
        // Long
        Long brandId = esProduct.getBrandId();
        if (brandId != null) {
            boolQueryBuilder.must(QueryBuilders.termQuery("brandId", brandId));
        }
        // keyword
        String brandName = esProduct.getBrandName();
        if (StringUtils.hasLength(brandName)) {
            boolQueryBuilder.must(QueryBuilders.termQuery("brandName", brandName));
        }
        // text
        String name = esProduct.getName();
        if (StringUtils.hasLength(name)) {
            boolQueryBuilder.must(QueryBuilders.matchQuery("name", name));
        }

        NativeSearchQueryBuilder nativeSearchQueryBuilder = new NativeSearchQueryBuilder();
        // 分页 (如果不设置分页参数 默认最大值10000)
        if (pageNum != null && pageSize != null) {
            Pageable pageable = PageRequest.of(pageNum, pageSize);
            nativeSearchQueryBuilder.withPageable(pageable);
        }
        // 动态条件
        if (brandId == null && !StringUtils.hasLength(brandName) && !StringUtils.hasLength(name)) {
            nativeSearchQueryBuilder.withQuery(QueryBuilders.matchAllQuery());
        } else {
            nativeSearchQueryBuilder.withQuery(boolQueryBuilder);
        }

        SearchHits<EsProduct> searchHits = elasticsearchRestTemplate.search(nativeSearchQueryBuilder.build(), EsProduct.class);
        return searchHits.stream().map(SearchHit::getContent).collect(Collectors.toList());
    }
}
```
更多统计相关可以使用Aggregation方法实现,例如groupBy等