## Spark SQL

### Spark 简介

1. Spark SQL 是 Spark 为处理结构化数据而引入的模块，前身是Shark
2. Spark SQL 提供了DataFrame的编程抽象，底层依然是RDD
3. Spark SQL 是分布式查询引擎，支持标准SQL和HSQL

### DataFrame VS RDDS

DataFrame 和 RDDs 最主要的区别在于一个面向的是结构化数据，一个面向的是非结构化数据.
DataFrame 内部的有明确 Scheme 结构，即列名、列字段类型都是已知的，这带来的好处是可以减少数据读取以及更好地优化执行计划，从而保证查询效率。

- RDDs 适合非结构化数据的处理，而 DataFrame & DataSet 更适合结构化数据和半结构化的处理；
- DataFrame & DataSet 可以通过统一的 Structured API 进行访问，而 RDDs 则更适合函数式编程的场景；
- 相比于 DataFrame 而言，DataSet 是强类型的 (Typed)，有着更为严格的静态类型检查；
- DataSets、DataFrames、SQL 的底层都依赖了 RDDs API，并对外提供结构化的访问接口。




