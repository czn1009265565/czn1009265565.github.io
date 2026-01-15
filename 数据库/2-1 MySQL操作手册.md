# MySQL 操作手册

## 连接数据库

```shell
# 查看版本
mysql --version

# 创建连接
mysql -h <地址> -P <端口> -u <用户名> -p
Enter password:
```

## 数据迁移

```shell
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

### 更新数据

```mysql
-- 全表更新
UPDATE tb_name SET column_a=value_a,column_b=value_b,column_c=value_c;

-- 条件更新
UPDATE tb_name SET column_a=value_a where id=1;

-- 连表更新
UPDATE tb_name_1 t1,tb_name_2 t2 SET t1.column_a=t2.column_a where t1.column_b=t2.column_b;
```

### 删除数据

```mysql
DELETE FROM tb_name;
```

## 表查询

基本语法  
```
SELECT [DISTINCT] columnName,..[n] FROM tableName 
WHERE condition 
GROUP BY columnName,..[n] 
HAVING condition 
ORDER BY columnName,..[n] 
LIMIT 10 OFFSET 0;
```

### 子查询
子查询需用括号包裹

From子查询  
```mysql
select * from (select * from table1) as t1;
```

Where子查询
```mysql
-- 子查询返回列则可以用IN查询
select * from table1 where code in (select code from table2);

-- 子查询返回至少一行结果，EXISTS表达式就会返回TRUE，反之返回False
select * from table1 where exists (select * from table2)
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
with temp1 as (select * from t1)
select * from temp1;

with temp1 as (select * from t1),
     temp2 as (select * from t2)
select * from temp2;
```

### 窗口函数

窗口函数是对一组值进行操作，不需要使用GROUP BY 子句对数据进行分组，还能够在同一行中同时返回基础行的列和聚合列。

基本语法  
```
OVER([PARTITION  BY  columnName,..[n] ] [ORDER  BY  columnName] )
```

应用场景  
```mysql
-- 共同展示聚合列和基础列
SELECT name, score, CAST(AVG(score) OVER () AS decimal(5, 2)) AS '平均分' FROM student;

-- 数据去重
SELECT  *  FROM  (
 SELECT  row_number() OVER(PARTITION  BY  name  ORDER  BY  create_time DESC)  AS  part ,name, score, create_time  FROM  student
)  AS  t WHERE t.part = 1;
```

排序函数  
- ROW_NUMBER(): 返回结果集内的行号，每个分区从1开始计算，ORDER BY可确定在特定分区中为行分配唯一 ROW_NUMBER 的顺序
- RANK(): 返回结果集的分区内每行的排序。行的排名是从1开始算。若2行具有相同的值，则该2行排名相同，但是下一个不同行的排名将跳过一个排名
- DENSE_RANK(): 返回结果集的分区内每行的排序。行的排名是从1开始算。若2行具有相同的值，则该2行排名相同，但排名依旧连续

### 递归查询
递归查询是通过CTE来实现的。CTE至少包含两个查询部分:

1. 非递归成员: 这是CTE的初始查询，它提供了递归的基础或起始点。
2. 递归成员: 这个查询引用了CTE本身，用于生成递归结果。


递归查询的执行过程如下:

1. 执行非递归成员，返回初始结果集。
2. 使用初始结果集作为输入，执行递归成员，生成新的结果。
3. 将新的结果集与初始结果集合并。
4. 重复步骤2和3，直到递归成员不再返回新的行

样例数据
```sql
CREATE TABLE employees (
   employee_id INT PRIMARY KEY,
   employee_name VARCHAR(100),
   manager_id INT
);
 
INSERT INTO employees (employee_id, employee_name, manager_id) VALUES
(1, 'Alice', NULL),       -- Alice 是CEO，没有上级
(2, 'Bob', 1),            -- Bob 是Alice的下属
(3, 'Charlie', 1),        -- Charlie 是Alice的下属
(4, 'David', 2),          -- David 是Bob的下属
(5, 'Eve', 3);            -- Eve 是Charlie的下属
```

递归查询-父查子
```sql
WITH RECURSIVE employeecte AS (
    -- 非递归成员
    SELECT employee_id, manager_id, employee_name
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 递归成员
    SELECT e.employee_id, e.manager_id, e.employee_name
    FROM employees e
             INNER JOIN employeecte ecte ON e.manager_id = ecte.employee_id
)
SELECT * FROM employeecte;
```

递归查询-子查父
```sql
WITH RECURSIVE employeecte AS (
    -- 非递归成员
    SELECT employee_id, manager_id, employee_name
    FROM employees
    WHERE employee_id = 5

    UNION ALL

    -- 递归成员
    SELECT e.employee_id, e.manager_id, e.employee_name
    FROM employees e
             INNER JOIN employeecte ecte ON e.employee_id = ecte.manager_id
)
SELECT * FROM employeecte;
```