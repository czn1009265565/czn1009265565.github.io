# Explain

Explain 可用来分析SQL的执行计划

## 输出结果

| 字段	           | 含义              |
|---------------|-----------------|
| id	           | 该语句的唯一标识        |
| select_type	  | 查询类型            |
| table	        | 	表名             |
| partitions	   | 	匹配的分区          |
| type	         | 	联接类型           |
| possible_keys | 可能的索引选择         |
| key	          | 实际选择的索引         |
| key_len	      | 	索引的长度          |
| ref	          | 索引的哪一列被引用了      |
| rows	         | 	估计要扫描的行        |
| filtered	     | 	表示符合查询条件的数据百分比 |
| Extra	        | 	附加信息           |

### id

该语句的唯一标识。如果explain的结果包括多个id值，则数字越大越先执行；而对于相同id的行，则表示从上往下依次执行。

### select_type
查询类型

| 查询类型	                 | 作用                                                                                               |
|-----------------------|--------------------------------------------------------------------------------------------------|
| SIMPLE	               | 简单查询（未使用UNION或子查询）                                                                               |
| PRIMARY               | 	最外层的查询                                                                                          |
| UNION                 | 	在UNION中的第二个和随后的SELECT被标记为UNION。如果UNION被FROM子句中的子查询包含，那么它的第一个SELECT会被标记为DERIVED。                 |
| DEPENDENT UNION       | 	UNION中的第二个或后面的查询，依赖了外面的查询                                                                       |
| UNION RESULT	         | UNION的结果                                                                                         |
| SUBQUERY	             | 子查询中的第一个 SELECT                                                                                  |
| DEPENDENT SUBQUERY	   | 子查询中的第一个 SELECT，依赖了外面的查询                                                                         |
| DERIVED	              | 用来表示包含在FROM子句的子查询中的SELECT，MySQL会递归执行并将结果放到一个临时表中。MySQL内部将其称为是Derived table（派生表），因为该临时表是从子查询派生出来的 |
| DEPENDENT DERIVED	    | 派生表，依赖了其他的表                                                                                      |
| MATERIALIZED	         | 物化子查询                                                                                            |
| UNCACHEABLE SUBQUERY	 | 子查询，结果无法缓存，必须针对外部查询的每一行重新评估                                                                      |
| UNCACHEABLE UNION	    | UNION属于UNCACHEABLE SUBQUERY的第二个或后面的查询                                                            |

### table
表示当前正在查询的表名，如果SQL定义了别名，则展示表的别名