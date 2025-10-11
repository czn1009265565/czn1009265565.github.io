# Java JDBC

`JDBC API`是一系列的接口，它统一和规范了应用程序与数据库的连接，执行SQL语句并得到返回结果等各类操作，相关类和接口在java.sql和javax.sql包下。

## 获取连接

### 通过new关键字

```java
import org.postgresql.Driver;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.Properties;

public class JDBCTest {
    public static void main(String[] args) throws SQLException {
        // 加载驱动
        Driver driver = new Driver();

        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String user = "postgres";
        String password = "postgres";
        Properties info = new Properties();
        info.setProperty("user",user);
        info.setProperty("password",password);
        // 获取连接
        Connection connect = driver.connect(url, info);
        System.out.println("基于new关键字创建连接" + connect);

        // 释放资源
        connect.close();
    }
}
```
通过new的方法获取到Driver对象，Driver对象属于第三方，并且是静态加载，导致灵活性低，依赖性强

### 通过反射

```java
import java.sql.Connection;
import java.sql.Driver;
import java.util.Properties;

public class JDBCTest {
    public static void main(String[] args) throws Exception {
        // 加载驱动
        Class<?> clazz = Class.forName("org.postgresql.Driver");
        Driver driver = (Driver) clazz.newInstance();

        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String user = "postgres";
        String password = "postgres";
        Properties info = new Properties();
        info.setProperty("user",user);
        info.setProperty("password",password);
        // 获取连接
        Connection connect = driver.connect(url, info);
        System.out.println("基于反射创建连接" + connect);

        // 释放资源
        connect.close();
    }
}
```
相比new关键字的方式具有更高的灵活性，同时也减低了依赖性

### 通过DriverManager

```java
import java.lang.reflect.Constructor;
import java.sql.Connection;
import java.sql.Driver;
import java.sql.DriverManager;

public class JDBCTest {
    public static void main(String[] args) throws Exception {
        //使用反射机制加载Driver类
        Class<?> clazz = Class.forName("org.postgresql.Driver");
        Constructor<?> constructor = clazz.getConstructor();
        Driver driver = (Driver) constructor.newInstance();

        //注册Driver驱动
        DriverManager.registerDriver(driver);

        //创建url,user,password
        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String user = "postgres";
        String password = "postgres";

        //获取连接
        Connection connection = DriverManager.getConnection(url, user, password);
        System.out.println("通过DriverManager创建连接" + connection);
        
        // 释放资源
        connection.close();
    }
}
```
在反射机制的基础上，使用DriverManager替代Driver，进行统一管理，具有更好的拓展性

简化(实际开发过程中的写法)  
```java
import java.sql.Connection;
import java.sql.DriverManager;

public class JDBCTest {
    public static void main(String[] args) throws Exception {
        // 加载驱动，也可以省略，JDK基于对应Driver jar包下META-INF\services\java.sql.Driver文本中的类名称自动注册
        Class.forName("org.postgresql.Driver");

        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String user = "postgres";
        String password = "postgres";
        // 创建连接
        Connection connection = DriverManager.getConnection(url, user, password);

        // 关闭连接
        connection.close();
    }
}
```

## 接口定义

### Connection
Connection接口代表Java程序和数据库的连接

- `getMetaData()`: 返回表示数据库元数据DatabaseMetaData对象，可以获取表、字段等信息
- `createStatement()`: 创建一个Statement对象来将SQL发送到数据库
- `prepareStatement`: 创建一个PreparedStatement对象来将参数化的SQL发送到数据库
- `prepareCall()`: 创建一个CallableStatement对象来调用数据库存储过程
- `commit()`: 手动提交
- `rollback()`: 手动回滚


### Statement
Statement 接口用于向数据库发送 SQL 语句，在 Statement 接口中，提供了三个执行 SQL 语句的方法

- `execute(String sql)`: 用于执行各种SQL语句，该方法返回一个boolean类型的值，如果为true，表示所查询的SQL具有返回结果，可以通过Statement.getResultSet()获取查询结果
- `executeQuery(String sql)`: 用于执行SQL中的select语句，该方法返回一个表示查询结果的ResultSet
- `executeUpdate(String sql)`: 用于执行SQL中的insert、update、delete语句，该方法返回一个int值，表示数据库中受该SQL语句影响的数据行数

### ResultSet
ResultSet 接口表示 select 查询语句得到的结果集，该结果集封装在一个逻辑表格中。
在ResultSet接口内部有一个指向表格数据行的游标，ResultSet对象初始化时，游标在表格的第一行之前。

- `next()`: 将游标从当前位置下移一行
- `close()`: 关闭结果集
- `getString(int columnIndex)`: 用于获取指定字段String值，columnIndex代表字段的索引
- `getString(String columnLabel)`: 用于获取指定字段String值，columnLabel代表字段名称
- `getBoolean(int columnIndex)`: 用于获取指定字段boolean值
- `getBoolean(String columnLabel)`: 用于获取指定字段boolean值
- `getInt(int columnIndex)`: 用于获取指定字段int值
- `getInt(String columnLabel)`: 用于获取指定字段int值
- `getDate(int columnIndex, Calendar cal)`: 用于获取指定字段Date值
- `getDate(String columnLabel, Calendar cal)`: 用于获取指定字段Date值

## 功能实现

### 获取表元数据

```java
public class TableMetaService {

    /**
     * 数据库连接信息
     */
    private static final String URL = "jdbc:mysql://localhost:3306/dbname";
    private static final String USERNAME = "username";
    private static final String PASSWORD = "password";

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USERNAME, PASSWORD);
    }

    public static List<TableInfo> getAllTables() throws SQLException {
        List<TableInfo> tables = new ArrayList<>();

        try (Connection conn = getConnection()) {
            DatabaseMetaData metaData = conn.getMetaData();

            // 获取所有表
            ResultSet rs = metaData.getTables(null, null, "%", new String[]{"TABLE"});

            while (rs.next()) {
                TableInfo table = new TableInfo();
                table.setTableCatalog(rs.getString("TABLE_CAT"));
                table.setTableSchema(rs.getString("TABLE_SCHEM"));
                table.setTableName(rs.getString("TABLE_NAME"));
                table.setTableType(rs.getString("TABLE_TYPE"));
                table.setRemarks(rs.getString("REMARKS"));
                tables.add(table);
            }
        }
        return tables;
    }

    public static List<ColumnInfo> getTableColumns(String tableName) throws SQLException {
        List<ColumnInfo> columns = new ArrayList<>();

        try (Connection conn = getConnection()) {
            DatabaseMetaData metaData = conn.getMetaData();

            ResultSet rs = metaData.getColumns(null, null, tableName, "%");

            while (rs.next()) {
                ColumnInfo column = new ColumnInfo();
                column.setColumnName(rs.getString("COLUMN_NAME"));
                column.setDataType(rs.getInt("DATA_TYPE"));
                column.setTypeName(rs.getString("TYPE_NAME"));
                column.setColumnSize(rs.getInt("COLUMN_SIZE"));
                column.setDecimalDigits(rs.getInt("DECIMAL_DIGITS"));
                column.setNullable(rs.getInt("NULLABLE"));
                column.setRemarks(rs.getString("REMARKS"));
                column.setColumnDefault(rs.getString("COLUMN_DEF"));
                column.setIsAutoIncrement(rs.getString("IS_AUTOINCREMENT"));
                columns.add(column);
            }
        }
        return columns;
    }
}
```


### 事务管理
Connection对象支持事务管理。事务是一组SQL操作，要么全部成功，要么全部失败。
通过Connection对象，可以开启手动提交或回滚事务。

```java
public class JDBCTest {
    public static void main(String[] args) throws SQLException {
        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        String user = "postgres";
        String password = "postgres";
        Connection connection = null;
        Statement statement = null;
        ResultSet resultSet = null;
        try  {
            connection = DriverManager.getConnection(url, user, password);
            // 开始事务
            connection.setAutoCommit(false);

            // 执行一系列SQL操作，包括select、insert、update、delete
            statement = connection.createStatement();
            statement.executeQuery("select * from pg_tables");
            resultSet = statement.getResultSet();
            while (resultSet.next()) {
                String schemaName = resultSet.getString("schemaname");
                String tableName = resultSet.getString("tablename");
                String format = String.format("schemaName: %s tableName: %s", schemaName, tableName);
                System.out.println(format);
            }
            // 提交事务
            connection.commit();
        } catch (SQLException e) {
            e.printStackTrace();
            // 发生异常时回滚事务
            if (connection != null) {
                connection.rollback();
            }
        } finally {
            if (resultSet != null) {
                resultSet.close();
            }
            if (statement != null) {
                statement.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
}
```

### 连接池
使用HikariCP创建数据库连接池
```java
public class JDBCTest {
    public static void main(String[] args) throws SQLException {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://127.0.0.1:5432/postgres");
        config.setUsername("postgres");
        config.setPassword("postgres");
        // 可以省略
        // hikariDataSource.setDriverClassName("org.postgresql.Driver");
        // 最小连接数
        config.setMinimumIdle(5);
        // 最大连接数
        config.setMaximumPoolSize(10);
        // 是否自动提交，默认为true
        config.setAutoCommit(true);
        // 连接测试语句，一般为 select 1
        config.setConnectionTestQuery("select 1");
        // 连接超时时长，单位毫秒
        config.setConnectionTimeout(30000);
        // 最大生命时长，单位毫秒
        config.setMaxLifetime(1800000);
        // 连接池名称
        config.setPoolName("HikariCP");

        // 配置连接池
        HikariDataSource hikariDataSource = null;
        try {
            // 创建 Hikari 数据源
            hikariDataSource = new HikariDataSource();
        } catch (Exception e){
            e.printStackTrace();
        } finally {
            if (hikariDataSource != null) {
                hikariDataSource.close();
            }
        }
    }
}
```