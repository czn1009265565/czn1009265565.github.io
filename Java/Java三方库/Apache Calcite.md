# Apache Calcite

Apache Calcite 是一个动态的数据管理框架。提供了 SQL解析，SQL组装，SQL校验，SQL查询优化，以及多数据源适配等典型数据库管理功能。


## 多数据源适配

### 功能
1. 多数据源支持标准SQL统一访问
2. 统一SQL联邦查询(支持异构数据源连表查询)
3. 查询性能优化
    1. 谓词下推: 过滤条件在数据源端执行
    2. 列剪裁: 只查询需要的列
    3. 连接顺序优化: 基于成本的连接重排序
4. 支持实时数据分析(流批一体查询)

### 原理
Calcite 采用智能优化策略，优先将操作下推到数据源执行，只在必要时在内存中进行连接处理，并采用各种技术最大限度减少内存使用。

### CalciteProvider

```java
@Component
public class CalciteProvider {

    private Connection connection;

    public Connection getConnection() {
        synchronized (CalciteProvider.class) {
            if (connection == null) {
                initConnectionPool();
                return connection;
            }
            return connection;
        }
    }

    private void initConnectionPool() {
        // 创建 Calcite JDBC连接
        Properties info = new Properties();
        info.setProperty(CalciteConnectionProperty.LEX.camelName(), "JAVA");
        info.setProperty(CalciteConnectionProperty.FUN.camelName(), "all");
        info.setProperty(CalciteConnectionProperty.CASE_SENSITIVE.camelName(), "false");
        info.setProperty(CalciteConnectionProperty.PARSER_FACTORY.camelName(), "org.apache.calcite.sql.parser.impl.SqlParserImpl#FACTORY");
        info.setProperty(CalciteConnectionProperty.DEFAULT_NULL_COLLATION.camelName(), NullCollation.LAST.name());
        info.setProperty("remarks", "true");
        try {
            Class.forName("org.apache.calcite.jdbc.Driver");
            connection = DriverManager.getConnection("jdbc:calcite:", info);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // 新增Schema
        addSchema(
                "jdbc:mysql://127.0.0.1:3306/dbname",
                "root",
                "password",
                "mysql_db",
                null);
        addSchema(
                "jdbc:postgresql://127.0.0.1:5432/dbname",
                "postgres",
                "password",
                "postgres_db",
                "public"
        );
    }

    private void addSchema(String jdbcUrl, String username, String password, String schemaName, String schema) {
        try {
            Connection connection = getConnection();
            CalciteConnection calciteConnection = connection.unwrap(CalciteConnection.class);
            SchemaPlus rootSchema = calciteConnection.getRootSchema();
            DataSource mysqlDataSource = buildDataSource(jdbcUrl, username, password);
            buildJdbcSchema(rootSchema, mysqlDataSource, schemaName, schema);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private DataSource buildDataSource(String jdbcUrl, String username, String password) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(jdbcUrl);
        config.setUsername(username);
        config.setPassword(password);
        config.setMinimumIdle(5);
        config.setMaximumPoolSize(20);
        config.setConnectionTimeout(10000);
        config.setIdleTimeout(300000);
        return new HikariDataSource(config);
    }

    private void buildJdbcSchema(SchemaPlus rootSchema, DataSource dataSource, String schemaName, String schema) {
        JdbcSchema jdbcSchema = JdbcSchema.create(rootSchema,
                schemaName,
                dataSource,
                null,
                schema);
        rootSchema.add(schemaName, jdbcSchema);
    }

    public List<String[]> query(String sql) {
        List<String[]> dataResult = new ArrayList<>();
        Statement stmt = null;
        ResultSet rs = null;
        try {
            Connection connection = getConnection();
            CalciteConnection calciteConnection = connection.unwrap(CalciteConnection.class);
            stmt = calciteConnection.createStatement();
            // 查询 target_database 数据库中的表
            rs = stmt.executeQuery(sql);
            dataResult = getDataResult(rs);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (rs != null) {
                    rs.close();
                }
                if (stmt != null) {
                    stmt.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return dataResult;
    }

    private List<String[]> getDataResult(ResultSet rs) {
        List<String[]> list = new LinkedList<>();
        try {
            ResultSetMetaData metaData = rs.getMetaData();
            int columnCount = metaData.getColumnCount();
            while (rs.next()) {
                String[] row = new String[columnCount];
                for (int j = 0; j < columnCount; j++) {
                    int columnType = metaData.getColumnType(j + 1);
                    switch (columnType) {
                        case Types.DATE:
                            if (rs.getDate(j + 1) != null) {
                                row[j] = rs.getDate(j + 1).toString();
                            }
                            break;
                        case Types.BOOLEAN:
                            row[j] = rs.getBoolean(j + 1) ? "true" : "false";
                            break;
                        default:
                            if (metaData.getColumnTypeName(j + 1).toLowerCase().equalsIgnoreCase("blob")) {
                                row[j] = rs.getBlob(j + 1) == null ? "" : rs.getBlob(j + 1).toString();
                            } else {
                                row[j] = rs.getString(j + 1);
                            }
                            break;
                    }
                }
                list.add(row);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return list;
    }
}
```


### JdbcSchema.create 函数
```
JdbcSchema create(SchemaPlus parentSchema,
                  String name,
                  DataSource dataSource,
                  @Nullable String catalog,
                  @Nullable String schema)
```

- parentSchema: 当前要创建的 JdbcSchema 的父级 Schema
- name: 为此 Jdbc Schema 指定的名称。这个名称将在 SQL 查询中用于标识这个 schema（例如 SELECT * FROM "schema_name"."table_name"）
- dataSource: 封装了到目标数据库的连接信息（如 URL、用户名、密码、连接池配置等）。通常使用如 HikariCP、DBCP 等连接池来创建 DataSource
- catalog: 对应目标数据库中的 Catalog 名称
- schema: 对应目标数据库中的 Schema 名称模式,MySQL 中通常传null。在 PostgreSQL 和 SQL Server 中，这指的是数据库下的 Schema
