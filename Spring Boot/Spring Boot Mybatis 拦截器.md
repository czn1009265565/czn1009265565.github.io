# Spring Boot Mybatis 拦截器


## 应用场景

- `SQL` 语句执行监控：可以拦截执行的 `SQL` 方法，打印执行的 SQL 语句、参数等信息，并且还能够记录执行的总耗时，可供后期的 `SQL` 分析时使用。
- `SQL` 分页查询：`MyBatis` 中使用的 `RowBounds` 使用的内存分页，在分页前会查询所有符合条件的数据，在数据量大的情况下性能较差。通过拦截器，可以在查询前修改 SQL 语句，提前加上需要的分页参数。
- 公共字段的赋值：在数据库中通常会有 `createTime` ， `updateTime` 等公共字段，这类字段可以通过拦截统一对参数进行的赋值，从而省去手工通过 `set` 方法赋值的繁琐过程。
- 数据权限过滤：在很多系统中，不同的用户可能拥有不同的数据访问权限，例如在多租户的系统中，要做到租户间的数据隔离，每个租户只能访问到自己的数据，通过拦截器改写 SQL 语句及参数，能够实现对数据的自动过滤。
`SQL` 语句替换：对 `SQL` 中条件或者特殊字符进行逻辑替换。


## 拦截器实现

```java
@Slf4j
@Component
@Intercepts({@Signature(type = StatementHandler.class, method = "prepare", args = {Connection.class, Integer.class})})
public class DynamicSqlInterceptor implements Interceptor {

    @Override
    public Object intercept(Invocation invocation) throws Throwable {
        // 1. 获取 StatementHandler 对象也就是执行语句
        StatementHandler statementHandler = (StatementHandler) invocation.getTarget();
        // 2. MetaObject 是 MyBatis 提供的一个反射帮助类，可以优雅访问对象的属性，这里是对 statementHandler 对象进行反射处理，
        MetaObject metaObject = MetaObject.forObject(statementHandler, SystemMetaObject.DEFAULT_OBJECT_FACTORY,
                SystemMetaObject.DEFAULT_OBJECT_WRAPPER_FACTORY,
                new DefaultReflectorFactory());
        // 3. 通过 metaObject 反射获取 statementHandler 对象的成员变量 mappedStatement
        MappedStatement mappedStatement = (MappedStatement) metaObject.getValue("delegate.mappedStatement");
        // mappedStatement 对象的 id 方法返回执行的 mapper 方法的全路径名，如com.mall.core.dao.UserMapper.insertUser
        String id = mappedStatement.getId();
        // 4. 通过 id 获取到 Dao 层类的全限定名称，然后反射获取 Class 对象
        Class<?> classType = Class.forName(id.substring(0, id.lastIndexOf(".")));
        // 5. 获取包含原始 sql 语句的 BoundSql 对象
        BoundSql boundSql = statementHandler.getBoundSql();
        String sql = boundSql.getSql();
        log.info("替换前---sql：{}", sql);
        // 6. 修改SQL 去掉双引号
        String mSql = sql.replace("\"", "");

        if (StringUtils.isNotBlank(mSql)) {
            log.info("替换后---mSql：{}", mSql);
            // 7. 对 BoundSql 对象通过反射修改 SQL 语句。
            Field field = boundSql.getClass().getDeclaredField("sql");
            field.setAccessible(true);
            field.set(boundSql, mSql);
        }
        // 8. 执行修改后的 SQL 语句。
        return invocation.proceed();
    }

    @Override
    public Object plugin(Object target) {
        // 使用 Plugin.wrap 方法生成代理对象
        return Plugin.wrap(target, this);
    }

    @Override
    public void setProperties(Properties properties) {
        // 获取配置文件中的属性值
    }
}
```