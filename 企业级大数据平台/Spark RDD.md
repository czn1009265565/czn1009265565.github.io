## Spark RDD

### RDD 简介

1. RDD 全称弹性分布式数据集
2. RDD 是一种分布式内存抽象，表示一个只读的记录分区的集合
3. RDD 是Spark的核心，我们编写Spark任务本质是对RDD进行各种转换操作

### RDD 特性

#### 只读
RDD 只能通过其他RDD转换而创建，所以RDD之间存在依赖，可以认为是RDD的血缘关系

#### 分区
RDD 逻辑上是分区的，各个分区可以保存到不同的节点，从而可以进行并行计算

#### 转换
RDD 之间可以通过丰富的算子进行转换，这些RDD之间维护着这些关系

### RDD 操作
1. 转化操作 Transformation

- map 将函数应用于 RDD 中的每个元素，将返回值构成新的 RDD
- flatmap 将函数应用于 RDD 中的每个元素，将返回的迭代器的所有内容构成新的 RDD
- filter 返回一个由通过传给 filter() 的函数的元素组成的 RDD
- union 生成一个包含两个 RDD 中所有元素的
- distinct 去重
- groupBy
- groupByKey
- join
- repartition

2. 行动操作 Action

- count()	返回数据集中的元素个数
- collect()	以数组的形式返回数据集中的所有元素
- first()	返回数据集中的第一个元素
- take(n)	以数组的形式返回数据集中的前n个元素
- reduce(func)	通过函数func（输入两个参数并返回一个值）聚合数据集中的元素
- foreach(func)	将数据集中的每个元素传递到函数func中运行

转换的返回值是一个新的RDD集合，而不是单个值。 行动操作计算并返回一个新的值。
转化操作和行动操作的区别在于 RDD只有在第一个行动操作中用到时才会正真计算


### RDD 依赖关系

1. 窄依赖，父子RDD之间的分区是一一对应的。窄依赖的转换操作与RDD中其他分区无关，可以通过管道的方式一气呵成。
2. 宽依赖，子RDD的每个分区与父RDD的所有分区都有关系，多对多。宽依赖的操作涉及RDD不同分区，需要对数据重新整理 Shuffle,产生数据交互

### RDD 转换示例

```shell
# 启动spark-shell
spark-shell --master local[2]
```
