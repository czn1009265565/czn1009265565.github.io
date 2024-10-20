# MySQL 操作手册

## MySQL命令

```shell
# 创建连接
mysql -h <地址> -P <端口> -u <用户名> -p
Enter password:

# 导出一张表
mysqldump -u用户名 -p密码 库名 表名 > table_name.sql
# 导出多张表
mysqldump -u用户名 -p密码 库名 表1 表2 表3 > dbname.sql
# 导出所有表
mysqldump -u用户名 -p密码 库名 > dbname.sql
# 导出数据库
mysqldump -u用户名 -p密码 --lock-all-tables --database 库名 > dbname.sql

# mysql导入
source 备份文件
# shell执行导入
mysql -u用户名 -p密码 库名 < 备份文件
```

## 数据类型
### 数值类型

- TINYINT
- SMALLINT
- MEDIUMINT
- INT
- BIGINT
- FLOAT 单精度
- DOUBLE 双精度
- DECIMAL(M,D) M也表示总位数，D表示小数位数。

### 字符串类型

- CHAR
- VARCHAR
- TEXT

### 日期类型

- DATETIME
- TIMESTAMP

## 数据库操作

```mysql
-- 创建数据库
CREATE DATABASE dbname CHARACTER SET utf8 COLLATE utf8_general_ci;
-- 查看已有库
SHOW DATABASES;
-- 查看当前库信息
SHOW CREATE DATABASE dbname;
-- 删除库
DROP DATABASE dbname;
```

## 表操作

### 创建表

```mysql
CREATE TABLE tb_name (
    id BIGINT(20) NOT NULL PRIMARY KEY COMMENT '主键Id',
    title VARCHAR(64) NOT NULL COMMENT '标题',
    create_time DATETIME NOT NULL DEFAULT NOW() COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT NOW() COMMENT '更新时间'
) COMMENT 'tb_name';
```

### 查看所有表

```mysql
SHOW TABLES;
```

### 查看表结构

```mysql
SHOW CREATE TABLE tb_name;
```

### 修改表

```mysql
-- 新增表字段
ALTER TABLE tb_name ADD column_name VARCHAR(32) COMMENT 'column_name';
-- 删除表字段
ALTER TABLE tb_name DROP column_name;
-- 删除表索引
ALTER TABLE tb_name DROP INDEX index_name;
-- 修改表字段
ALTER TABLE tb_name MODIFY column_name VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'column_name';
```

### 删除表

```mysql
-- 删除表
DROP TABLE tb_name;
```

### 清空表

```mysql
-- 清空表数据
TRUNCATE TABLE tb_name;
```

### 复制表

```mysql
-- 复制表结构
CREATE TABLE tb_name_copy LIKE tb_name;
-- 复制表结构和数据
CREATE TABLE tb_name_copy SELECT * FROM tb_name;
```

## 索引操作

### 创建索引

```mysql
-- 创建普通索引
CREATE INDEX index_name ON tb_name(column_name);
-- 创建唯一索引
CREATE UNIQUE INDEX index_name ON tb_name(column_name);
-- 创建联合索引
CREATE INDEX `column_a_column_b_index` using btree on tb_name(column_a,column_b);
```

### 删除索引
    
```mysql
ALTER TABLE tb_name DROP INDEX index_name;
```

### 查看索引

```mysql
SHOW INDEX FROM tb_name;
```

## 数据操作

### 插入数据

```mysql
INSERT INTO tb_name(column_a,column_b,column_c) values(value_a,value_b,value_c);
```

### 删除数据

```mysql
DELETE FROM tb_name;
```

### 更新数据

```mysql
-- 全表更新
UPDATE tb_name SET column_a=value_a,column_b=value_b,column_c=value_c;

-- 条件更新
UPDATE tb_name SET column_a=value_a where id=1;

-- 连表更新
UPDATE tb_name_1 t1,tb_name_2 t2 SET t1.column_a=t2.column_a where t1.column_b=t2.column_b;
```


## 表查询

```
SELECT [ALL|DISTINCT] select_expr FROM -> WHERE -> GROUP BY [合计函数] -> HAVING -> ORDER BY -> LIMIT
a. select_expr
-- 可以用 * 表示所有字段。
select * from tb;
-- 可以使用表达式（计算公式、函数调用、字段也是个表达式）
select stu, 29+25, now() from tb;
-- 可以为每个列使用别名。适用于简化列标识，避免多个列标识符重复。
- 使用 as 关键字，也可省略 as.
        select stu+10 as add10 from tb;
b. FROM 子句
    用于标识查询来源。
    -- 可以为表起别名。使用as关键字。
SELECT * FROM tb1 AS tt, tb2 AS bb;
-- from子句后，可以同时出现多个表。
-- 多个表会横向叠加到一起，而数据会形成一个笛卡尔积。
SELECT * FROM tb1, tb2;
-- 向优化符提示如何选择索引
USE INDEX、IGNORE INDEX、FORCE INDEX
SELECT * FROM table1 USE INDEX (key1,key2) WHERE key1=1 AND key2=2 AND key3=3;
SELECT * FROM table1 IGNORE INDEX (key3) WHERE key1=1 AND key2=2 AND key3=3;
c. WHERE 子句
    -- 从from获得的数据源中进行筛选。
    -- 整型1表示真，0表示假。
    -- 表达式由运算符和运算数组成。
        -- 运算数：变量（字段）、值、函数返回值
        -- 运算符：
            =, <=>, <>, !=, <=, <, >=, >, !, &&, ||,
            in (not) null, (not) like, (not) in, (not) between and, is (not), and, or, not, xor
            is/is not 加上ture/false/unknown，检验某个值的真假
            <=>与<>功能相同，<=>可用于null比较
d. GROUP BY 子句, 分组子句
    GROUP BY 字段/别名 [排序方式]
    分组后会进行排序。升序：ASC，降序：DESC
    以下[合计函数]需配合 GROUP BY 使用：
    count 返回不同的非NULL值数目  count(*)、count(字段)
    sum 求和
    max 求最大值
    min 求最小值
    avg 求平均值
    group_concat 返回带有来自一个组的连接的非NULL值的字符串结果。组内字符串连接。
e. HAVING 子句，条件子句
    与 where 功能、用法相同，执行时机不同。
    where 在开始时执行检测数据，对原数据进行过滤。
    having 对筛选出的结果再次进行过滤。
    having 字段必须是查询出来的，where 字段必须是数据表存在的。
    where 不可以使用字段的别名，having 可以。因为执行WHERE代码时，可能尚未确定列值。
    where 不可以使用合计函数。一般需用合计函数才会用 having
    SQL标准要求HAVING必须引用GROUP BY子句中的列或用于合计函数中的列。
f. ORDER BY 子句，排序子句
    order by 排序字段/别名 排序方式 [,排序字段/别名 排序方式]...
    升序：ASC，降序：DESC
    支持多个字段的排序。
g. LIMIT 子句，限制结果数量子句
    仅对处理好的结果进行数量限制。将处理好的结果的看作是一个集合，按照记录出现的顺序，索引从0开始。
    limit 起始位置, 获取条数
    省略第一个参数，表示从索引0开始。limit 获取条数
h. DISTINCT, ALL 选项
    distinct 去除重复记录
    默认为 all, 全部记录
```

### 子查询

```
/* 子查询 */ ------------------
    - 子查询需用括号包裹。
-- from型
    from后要求是一个表，必须给子查询结果取个别名。
    - 简化每个查询内的条件。
    - from型需将结果生成一个临时表格，可用以原表的锁定的释放。
    - 子查询返回一个表，表型子查询。
    select * from (select * from tb where id>0) as subfrom where id>1;
-- where型
    - 子查询返回一个值，标量子查询。
    - 不需要给子查询取别名。
    - where子查询内的表，不能直接用以更新。
    select * from tb where money = (select max(money) from tb);
    -- 列子查询
        如果子查询结果返回的是一列。
        使用 in 或 not in 完成查询
        exists 和 not exists 条件
            如果子查询返回数据，则返回1或0。常用于判断条件。
            select column1 from t1 where exists (select * from t2);
    -- 行子查询
        查询条件是一个行。
        select * from t1 where (id, gender) in (select id, gender from t2);
        行构造符：(col1, col2, ...) 或 ROW(col1, col2, ...)
        行构造符通常用于与对能返回两个或两个以上列的子查询进行比较。
    -- 特殊运算符
    != all()    相当于 not in
    = some()    相当于 in。any 是 some 的别名
    != some()   不等同于 not in，不等于其中某一个。
    all, some 可以配合其他运算符一起使用。
```

### 连接查询

```
/* 连接查询(join) */ ------------------
    将多个表的字段进行连接，可以指定连接条件。
-- 内连接(inner join)
    - 默认就是内连接，可省略inner。
    - 只有数据存在时才能发送连接。即连接结果不能出现空行。
    on 表示连接条件。其条件表达式与where类似。也可以省略条件（表示条件永远为真）
    也可用where表示连接条件。
    还有 using, 但需字段名相同。 using(字段名)
    -- 交叉连接 cross join
        即，没有条件的内连接。
        select * from tb1 cross join tb2;
-- 外连接(outer join)
    - 如果数据不存在，也会出现在连接结果中。
    -- 左外连接 left join
        如果数据不存在，左表记录会出现，而右表为null填充
    -- 右外连接 right join
        如果数据不存在，右表记录会出现，而左表为null填充
-- 自然连接(natural join)
    自动判断连接条件完成连接。
    相当于省略了using，会自动查找相同字段名。
    natural join
    natural left join
    natural right join
select info.id, info.name, info.stu_num, extra_info.hobby, extra_info.sex from info, extra_info where info.stu_num = extra_info.stu_id;
```

### WITH AS
当我们书写一些结构相对复杂的SQL语句时，可能某个子查询在多个层级多个地方存在重复使用的情况，
这个时候我们可以使用 `with as` 语句将其独立出来，极大提高SQL可读性，简化SQL，常用于实现数据分析需求。

```mysql
with t1 as (select * from a)
select * from t1;

with t1 as (select * from a),
     t2 as (select * from b)
select * from t2;
```