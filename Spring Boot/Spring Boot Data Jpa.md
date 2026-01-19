## Spring Boot 整合 Jpa


### 依赖配置
```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>${mysql.version}</version>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

### application配置
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/database
    username: root
    password: root
    driver-class-name: com.mysql.jdbc.Driver
  jpa:
    hibernate:
      # 自动创建、更新、验证数据库表结构
      ddl-auto: validate
    show-sql: true
```

1. create：每次加载hibernate时都会删除上一次的生成的表，然后根据你的model类再重新来生成新表，哪怕两次没有任何改变也要这样执行，这就是导致数据库表数据丢失的一个重要原因。
2. create-drop：每次加载hibernate时根据model类生成表，但是sessionFactory一关闭,表就自动删除。
3. update：最常用的属性，第一次加载hibernate时根据model类会自动建立起表的结构（前提是先建立好数据库），以后加载hibernate时根据model类自动更新表结构，即使表结构改变了但表中的行仍然存在不会删除以前的行。要注意的是当部署到服务器后，表结构是不会被马上建立起来的，是要等应用第一次运行起来后才会。
4. validate：每次加载hibernate时，验证创建数据库表结构，只会和数据库中的表进行比较，不会创建新表，但是会插入新值。
初次创建时会设为create,创建好后改为validate.

### 实体类
```java
@Data
@Entity
@Table(name = "person")
public class Person {
    @Id
    private Long id;

    private String name;

    private Integer age;

    @Column(name = "create_time")
    private LocalDateTime createTime;
}
```

### Dao层
```java
public interface PersonRepository extends JpaRepository<Person, Long> {

    List<Person> findByName(String name);

    Page<Person> findByName(String name, Pageable pageable);
}
```
1. 方法的命名规则(Spring Boot Data 通用)

|关键字|方法命名|sql where 字句|
|---|---|---|
|And|findByNameAndPwd|where name= ? and pwd =?|
|Or|findByNameOrSex|where name= ? or sex=?|
|Is,Equal|findById|where id=?|
|Between|findByIdBetween|where id between ? and ?|
|LessThan|findByIdLessThan|where id < ?|
|LessThanEqual|findByIdLessThanEquals|where id <= ?|
|GreaterThan|findByIdGreaterThan|where id > ?|
|GreaterThanEqual|findByIdGreaterThanEquals|where id > = ?|
|After|findByIdAfter|where id > ?|
|Before|findByIdBefore|where id < ?|
|IsNull|findByNameIsNull|where name is null|
|NotNull|findByNameNotNull|where name is not|
|Like|findByNameLike|where name like ?|
|NotLike|findByNameNotLike|where name not like ?|
|StartingWith|indByNameStartingWith|where name like '?%'|
|EndingWith|findByNameEndingWith|where name like '%?'|
|Containing|findByNameContaining|where name like '%?%'|
|OrderBy|findByIdOrderByXDesc|where id=? order by x desc|
|Not|findByNameNot|where name <> ?|
|In|findByIdIn(Collection<?> c)|where id in (?)|
|NotIn|findByIdNotIn(Collection<?> c)|where id not in (?)|
|True|findByAaaTue|where aaa = true|
|False|findByAaaFalse|where aaa = false|
|IgnoreCase|findByNameIgnoreCase|where UPPER(name)=UPPER(?)|

2. 分页查询简单实现

```java
@Component
public class PersonServiceImpl {
    @Autowired
    private PersonRepository personRepository;

    public Page<Person> listByName(String name, Integer pageNum, Integer pageSize) {
        // 省略参数校验......
        // 注意点: 第一页 从 0 开始，排序根据属性名非字段名
        Pageable pageable = PageRequest.of(pageNum, pageSize, Sort.Direction.DESC, "createTime");
        return personRepository.findByName(name, pageable);
    }
}
```

### 原生SQL
在较为复杂的环境中，往往模板查询方法无法满足我们的要求，那就需要我们写原生查询语句
```java
public interface PersonRepository extends JpaRepository<Person, Long> {

    /**
     * nativeQuery=true 则查询语句使用原生sql，不加则使用HQL
     */
    @Query(value = "select id,name,age,create_time as createTime from person where name=?1", nativeQuery = true)
    List<Person> findByName(String name);

    @Query(value = "select id,name,age,create_time as createTime from person where name in (:names)", nativeQuery = true)
    List<Person> findByNameIn(@Param("names") List<String> names);
}
```

