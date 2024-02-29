## Spring Boot PostgreSQL


### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```

### application配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/datatest
    username: postgres
    password: postgres
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: create
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
```

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