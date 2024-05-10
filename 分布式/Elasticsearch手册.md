# Elasticsearch

本文基于Java客户端，记录API的基本使用

## 查询方法

#### matchAllQuery
- 使用方法： 创建一个查询，匹配所有文档。
- 示例：QueryBuilders.matchAllQuery()
- 注意事项：这种查询不加任何条件，会返回索引中的所有文档，可能会影响性能，特别是文档数量很多时。

#### matchQuery
- 使用方法：对指定字段执行全文搜索查询。
- 示例：QueryBuilders.matchQuery("fieldName", "text to search")
- 注意事项：默认会对文本进行分词处理，然后进行搜索。

#### multiMatchQuery
- 使用方法：允许你在多个字段上执行匹配查询。
- 示例：QueryBuilders.multiMatchQuery("text to search", "fieldName1", "fieldName2")
- 注意事项：适用于需要在不同字段上搜索相同文本的情况。

#### termQuery
- 使用方法：对指定字段执行精确匹配查询。
- 示例：QueryBuilders.termQuery("fieldName", "value")
- 注意事项：不会对字段值进行分词。

#### termsQuery
- 使用方法：允许指定多个精确值进行匹配查询。
- 示例：QueryBuilders.termsQuery("fieldName", "value1", "value2")
- 注意事项：不会对字段值进行分词，适用于字段值完全匹配其中一个查询值的情况。

#### rangeQuery
- 使用方法：对指定字段执行范围查询。
- 示例：QueryBuilders.rangeQuery("fieldName").from("startValue").to("endValue")
- 注意事项：可以设置范围的起始和结束值，适用于数值、日期等类型的字段。

#### wildcardQuery
- 使用方法：执行通配符查询，支持*（任意字符序列）和?（单个字符）。
- 示例：QueryBuilders.wildcardQuery("fieldName", "text*")
- 注意事项：可能会影响性能，尤其是通配符在前面时。

#### fuzzyQuery
- 使用方法：对指定字段执行模糊查询。
- 示例：QueryBuilders.fuzzyQuery("fieldName", "text")
- 注意事项：基于Levenshtein编辑距离进行匹配，可以设置模糊程度。

#### boolQuery
- 使用方法：组合多个查询条件，支持must（必须匹配）、should（至少匹配一个）、must_not（不能匹配）和filter（过滤）。
- 示例：QueryBuilders.boolQuery().must(QueryBuilders.termQuery("fieldName", "value"))
- 注意事项：是构建复杂查询逻辑的基础，性能比filter更优。

#### nestedQuery
- 使用方法：查询嵌套对象。
- 示例：QueryBuilders.nestedQuery("path", QueryBuilders.termQuery("path.fieldName", "value"), ScoreMode.Avg)
- 注意事项：path是嵌套对象的路径，必须使用nested类型定义嵌套对象字段。

#### prefixQuery
- 使用方法：搜索具有指定前缀的文档。
- 示例：QueryBuilders.prefixQuery("fieldName", "prefix")
- 注意事项：对性能影响较大，特别是前缀较短时。

#### regexpQuery
- 使用方法：使用正则表达式进行查询。
- 示例：QueryBuilders.regexpQuery("fieldName", "regexp")
- 注意事项：复杂的正则表达式可能会严重影响性能。

#### disMaxQuery
- 使用方法：对子查询的结果做并集，但只用得分最高的那个子查询的得分作为最终得分。
- 示例：QueryBuilders.disMaxQuery().add(QueryBuilders.termQuery("fieldName", "value1")).add(QueryBuilders.termQuery("fieldName", "value2"))
- 注意事项：用于处理多个字段上的查询并想要每个字段上的查询独立计分。

#### matchPhraseQuery
- 使用方法：搜索与指定短语匹配的文档，考虑短语的完整性和顺序。
- 示例：QueryBuilders.matchPhraseQuery("fieldName", "phrase")
- 注意事项：对于精确的短语搜索非常有用。

#### matchPhrasePrefixQuery
- 使用方法：类似于matchPhraseQuery，但是对最后一个词允许前缀匹配。
- 示例：QueryBuilders.matchPhrasePrefixQuery("fieldName", "phrase prefix")
- 注意事项：适用于自动补全或容错的场景。

#### existsQuery
- 使用方法：搜索指定字段有值的文档（不为null或不存在）。
- 示例：QueryBuilders.existsQuery("fieldName")
- 注意事项：用于找出指定字段有值的文档。

#### idsQuery
- 使用方法：根据文档ID搜索文档。
- 示例：QueryBuilders.idsQuery().addIds("1", "2", "3")
- 注意事项：直接通过ID快速检索文档。

#### functionScoreQuery
- 使用方法：允许修改查询得分，通过一系列函数来调整。
- 示例:  
    ```
    FunctionScoreQueryBuilder functionScoreQueryBuilder = QueryBuilders
        .functionScoreQuery(
            // 主查询
            QueryBuilders.matchQuery("content", "Elasticsearch"),
            // 功能分数查询数组
            new FunctionScoreQueryBuilder.FilterFunctionBuilder[] {
                new FunctionScoreQueryBuilder.FilterFunctionBuilder(
                    // 第一个函数的过滤查询
                    QueryBuilders.matchQuery("type", "Tutorial"),
                    // 第一个函数的提分因子
                    ScoreFunctionBuilders.weightFactorFunction(10)
                ),
                new FunctionScoreQueryBuilder.FilterFunctionBuilder(
                    // 第二个函数的过滤查询
                    QueryBuilders.matchQuery("type", "Article"),
                    // 第二个函数的提分因子
                    ScoreFunctionBuilders.weightFactorFunction(5)
                )
            }
        );
    ```
- 注意事项：提供了极高的灵活性，可以根据文档的属性计算得分。

