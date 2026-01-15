### 选择器
1. `{filed: value}` 查找那些 field 的值等于 value 的文档
2. `{filed1: value, field2: value}` 相当于 and 查询
3. `{$or: [{field1: value}, {field2: value}]}` or查询
4. `{$and: [{field1: value}, {field2: value}]}` and查询
5. `$lt`,`$lte`,`$gt`,`$gte`,`$ne`被用来处理小于，小于等于，大于，大于等于，不等于操作
6. `$exists` 用来匹配字段是否存在
    ```
    db.unicorns.find({
        vampires: {$exists: false}})
    ```
7. `$in`被用来匹配查询文档在我们传入的数组参数中是否存在匹配值
   ```
   db.unicorns.find({
   	loves: {$in:['apple','orange']}})
   ```
我们可以将选择器与find、remove、count方法结合使用。

### 插入
`db.collection.insert(document, options)`
```
// 单文档插入
db.collection.insert({field: value})

// 批量插入
db.collection.insert([{field: value}, {field: value}])
```


### 更新
`db.collection.update(query, update, option)`

1. 覆盖更新
   ```
   db.unicorns.update({name: 'Roooooodles'},
   	{weight: 590})
   ```
2. 改变一个或几个字段`$set`
   ```
   db.unicorns.update({name: 'Roooooodles'},
   	{$set: {weight: 590}})
   ```
3. 批量更新
   ```
   db.unicorns.update({},
   	{$set: {vaccinated: true }},
   	{multi:true});
   ```
   update 只更新第一个匹配文档，因此当你希望更新所有匹配文档时，你要用 multi 。

### 排序、分页
我们指定我们希望排序的字段，以 JSON 方式，其中 1 表示升序 -1 表示降序
```
//heaviest unicorns first
db.unicorns.find().sort({weight: -1})

//by unicorn name then vampire kills:
db.unicorns.find().sort({name: 1,
	vampires: -1})

db.unicorns.find()
	.sort({weight: -1})
	.limit(2)
	.skip(1)
```