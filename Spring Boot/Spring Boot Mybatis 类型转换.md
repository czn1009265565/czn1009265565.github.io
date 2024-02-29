## Spring Boot Mybatis 类型转换

### 抽象类

```java
public abstract class AbstractJsonTypeHandler<T> extends BaseTypeHandler<T> {
    public AbstractJsonTypeHandler() {
    }

    public void setNonNullParameter(PreparedStatement ps, int i, T parameter, JdbcType jdbcType) throws SQLException {
        ps.setString(i, this.toJson(parameter));
    }

    public T getNullableResult(ResultSet rs, String columnName) throws SQLException {
        String json = rs.getString(columnName);
        return StringUtils.isBlank(json) ? null : this.parse(json);
    }

    public T getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        String json = rs.getString(columnIndex);
        return StringUtils.isBlank(json) ? null : this.parse(json);
    }

    public T getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        String json = cs.getString(columnIndex);
        return StringUtils.isBlank(json) ? null : this.parse(json);
    }

    protected abstract T parse(String json);

    protected abstract String toJson(T obj);
}
```

### JacksonTypeHandler

```java
@Slf4j
public class JacksonTypeHandler extends AbstractJsonTypeHandler<Object> {

    private static ObjectMapper OBJECT_MAPPER;
    private final Class<?> type;

    public JacksonTypeHandler(Class<?> type) {
        if (log.isTraceEnabled()) {
            log.trace("JacksonTypeHandler(" + type + ")");
        }

        Assert.notNull(type, "Type argument cannot be null");
        this.type = type;
    }

    protected Object parse(String json) {
        try {
            return getObjectMapper().readValue(json, this.type);
        } catch (IOException var3) {
            throw new RuntimeException(var3);
        }
    }

    protected String toJson(Object obj) {
        try {
            return getObjectMapper().writeValueAsString(obj);
        } catch (JsonProcessingException var3) {
            throw new RuntimeException(var3);
        }
    }

    public static ObjectMapper getObjectMapper() {
        if (null == OBJECT_MAPPER) {
            OBJECT_MAPPER = new ObjectMapper();
        }

        return OBJECT_MAPPER;
    }

    public static void setObjectMapper(ObjectMapper objectMapper) {
        Assert.notNull(objectMapper, "ObjectMapper should not be null");
        OBJECT_MAPPER = objectMapper;
    }
}
```

### 实体类

```java
@Data
public class UserDO {
    private Long id;
    private String name;
    private String sex;
    private Integer age;
    private Date createTime;
    private Date updateTime;
    private Integer status;
    private Tag tag;

    @Data
    public static class Tag {
        private String license;
        private String identity;
    }
}
```

### UserDao

```java
@Mapper
public interface UserDao {
    List<UserDO> selectAll();

    void insert(@Param("userDO") UserDO userDO);
}
```


### Mapper
UserMapper示例

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.readwrite.dao.UserDao">

    <resultMap id="userDO" type="com.example.readwrite.entity.UserDO">
        <id property="id" column="id" />
        <result property="name" column="name"  jdbcType="VARCHAR"/>
        <result property="age" column="age"  jdbcType="INTEGER"/>
        <result property="createTime" column="create_time"  jdbcType="TIMESTAMP"/>
        <result property="updateTime" column="update_time"  jdbcType="TIMESTAMP"/>
        <result property="status" column="status"  jdbcType="INTEGER"/>
        <result property="tag" column="tag"  jdbcType="OTHER" typeHandler="com.example.readwrite.handler.JacksonTypeHandler"/>
    </resultMap>

    <sql id="Base_Column_List">
        id, name, sex, age, create_time, update_time, status, tag
    </sql>

    <insert id="insert">
        insert into tab_user(<include refid="Base_Column_List" />)
        values (#{userDO.id}, #{userDO.name}, #{userDO.sex}, #{userDO.age}, now(), now(), #{userDO.status}, #{userDO.tag, typeHandler=com.example.readwrite.handler.JacksonTypeHandler})
    </insert>

    <select id="selectAll" resultMap="userDO">
        select <include refid="Base_Column_List" /> from tab_user
    </select>
</mapper>
```