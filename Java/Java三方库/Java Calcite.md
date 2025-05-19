# Java Calcite
Apache Calcite 是一个动态的数据管理框架。提供了 SQL解析，SQL组装，SQL校验，SQL查询优化，以及数据库连接查询等典型数据库管理功能。

## SQL 解析
Apache Calcite 提供了强大的 SQL 解析功能，可以将 SQL 字符串转换为抽象语法树 (AST)

```java
public class SQLTest {
    public void parseSQL(String originSQL) throws SqlParseException {
        // 使用配置构建解析器
        SqlParser.Config config = SqlParser.config()
                .withLex(Lex.MYSQL)  // 使用MySQL词法
                .withCaseSensitive(false);  // 不区分大小写

        SqlParser parser = SqlParser.create(originSQL, config);
        // 解析SQL
        SqlNode sqlNode = parser.parseStmt();

        // 解析SelectList
        if (sqlNode instanceof SqlSelect) {
            SqlSelect select = (SqlSelect) sqlNode;
            System.out.println("Select List: " + select.getSelectList());
            System.out.println("From: " + select.getFrom());
            System.out.println("Where: " + select.getWhere());
            System.out.println("Group by: " + select.getGroup());
            System.out.println("Order by: " + select.getOrderList());
        }

    }

    public static void main(String[] args) throws SqlParseException {
        new SQLTest().parseSQL("select c1,c2,c3 from t");
    }
}
```

## SQL 组装

```java
public class SQLTest {
    public void buildSQL() {
        List<String> columns = List.of("c1", "c2", "c3");
        String tableName = "t";
        List<String> indexColumns = List.of("c1", "c2", "c3");

        // 创建 SELECT 列表
        SqlNodeList selectList = new SqlNodeList(SqlParserPos.ZERO);
        for (String col : columns) {
            selectList.add(new SqlIdentifier(col, SqlParserPos.ZERO));
        }

        // 创建 FROM 子句
        SqlNode from = new SqlIdentifier(tableName, SqlParserPos.ZERO);

        // 创建 WHERE 条件
        SqlNode whereCondition = new SqlBasicCall(
                SqlStdOperatorTable.GREATER_THAN,
                List.of(selectList.get(0), SqlLiteral.createExactNumeric("500", SqlParserPos.ZERO)),
                SqlParserPos.ZERO
        );

        // 创建 GROUP BY
        SqlNodeList groupByList = null;
        if (!CollectionUtils.isEmpty(indexColumns)) {
            groupByList = new SqlNodeList(SqlParserPos.ZERO);
            for (String col : indexColumns) {
                groupByList.add(new SqlIdentifier(col.trim(), SqlParserPos.ZERO));
            }
        }
        SqlSelect sqlSelect = new SqlSelect(SqlParserPos.ZERO,
                null,
                selectList,
                from,
                whereCondition,
                groupByList,
                null,
                null,
                null,
                null,
                null,
                null,
                null);
        System.out.println(sqlSelect.toSqlString(CalciteSqlDialect.DEFAULT).getSql());
    }
    
    public static void main(String[] args) {
        new SQLTest().buildSQL();
    }
}
```

## SQL 查询优化
Apache Calcite 提供了强大的 SQL 查询优化能力，可以将 SQL 查询转换为最优化的执行计划

```java
public class SQLTest {
    public static void main(String[] args) throws Exception {
        // 1. 创建框架配置
        FrameworkConfig config = Frameworks.newConfigBuilder()
                .build();
        // 2. 创建 Planner
        Planner planner = Frameworks.getPlanner(config);
        // 3. 解析 SQL
        String sql = "SELECT d.name, COUNT(*) FROM emps e JOIN depts d ON e.deptno = d.deptno " +
                "WHERE e.age > 30 GROUP BY d.name";
        SqlNode sqlNode = planner.parse(sql);
        SqlNode validated = planner.validate(sqlNode);
        // 4. 转换为关系代数
        RelRoot relRoot = planner.rel(validated);
        // 5. 优化
        RelNode optimizedRel = optimize(relRoot.project());
        // 6. 输出优化后的 SQL
        String optimizedSql = toSql(optimizedRel);
        System.out.println("Optimized SQL:\n" + optimizedSql);
    }

    private static RelNode optimize(RelNode relNode) {
        // 创建优化器
        RelOptPlanner planner = relNode.getCluster().getPlanner();

        // 设置规则集
        planner.addRule(ProjectToWindowRule.PROJECT);
        planner.addRule(FilterJoinRule.FILTER_ON_JOIN);
        // 常用规则
//        planner.addRule(FilterProjectTransposeRule.INSTANCE);  // 过滤和投影交换
//        planner.addRule(ProjectMergeRule.INSTANCE);           // 合并投影
//        planner.addRule(FilterJoinRule.FILTER_ON_JOIN);       // 将过滤条件下推到连接
//        planner.addRule(AggregateProjectMergeRule.INSTANCE);  // 合并聚合和投影
//        planner.addRule(SortRemoveRule.INSTANCE);             // 移除不必要的排序

        // 执行优化
        return planner.findBestExp();
    }

    private static String toSql(RelNode relNode) {
        RelToSqlConverter converter = new RelToSqlConverter(CalciteSqlDialect.DEFAULT);
        SqlNode sqlNode = converter.visitChild(0, relNode).asStatement();
        return sqlNode.toSqlString(CalciteSqlDialect.DEFAULT).getSql();
    }
}
```



