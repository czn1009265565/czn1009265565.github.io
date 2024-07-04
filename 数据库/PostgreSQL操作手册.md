# PostgreSQL操作手册

## 登录

运行PostgreSQL的交互式终端程序，它被称为psql， 它允许你交互地输入、编辑和执行SQL命令。

```shell
# 查看版本
psql --version

# 连接数据库
psql -U postgre -d postgres
```

**连接参数介绍**

- -h, --host=HOSTNAME
- -p, --port=PORT
- -U, --username=USERNAME
- -w, --no-password
- -W, --password
- -d, --dbname=DBNAME
- -c, --command=COMMAND

## 基本数据类型

### 数值类型

| 类型            | 存储大小 | 描述           | 范围                                         |
|---------------|------|--------------|--------------------------------------------|
| smallint/int2 | 2字节  | 小范围整数        | -32768 ～ +32767                            |
| integer/int4	 | 4字节	 | 整数的典型存储	     | -2147483648 ～ +2147483647                  |
| bigint/int8	  | 8字节	 | 大范围整数	       | -9223372036854775808 ～ 9223372036854775807 |
| decimal	      | 可变	  | 用户指定的精度，精确	  | 小数点前最多为131072个数字; 小数点后最多为16383个数字。         |
| numeric       | 	可变  | 	用户指定的精度，精确	 | 小数点前最多为131072个数字; 小数点后最多为16383个数字。         |
| smallserial	  | 2字节	 | 自动增加的小整数     | 	1～32767                                   |
| serial	       | 4字节  | 	自动增加的整数     | 	1～2147483647                              |
| bigserial	    | 8字节	 | 自动增加的大整数     | 	1～9223372036854775807                     |

### 字符串类型

| 类型                                     | 描述                                    |
|----------------------------------------|---------------------------------------|
| char(size)/character(size)	            | size是要存储的字符数。固定长度字符串，右边的空格填充到相等大小的字符。 |
| varchar(size)/character varying(size)	 | size是要存储的字符数。 可变长度字符串。                |
| text                                   | 可变长度字符串。                              |

### 日期类型

| 类型	                          | 存储大小	 | 描述	           |
|------------------------------|-------|---------------|
| timestamp                    | 	8字节  | 	日期和时间(无时区)   |
| timestamp with time zone	    | 8字节   | 	包括日期和时间，带时区	 |	 
| date	                        | 4字节	  | 日期(没有时间)      |

### 布尔类型
| 类型	     | 存储大小	 | 描述	         |
|---------|-------|-------------|
| boolean | 	1字节  | 	true/false |

## 复杂数据类型

### 枚举类型
枚举类型是一个包含静态和值的有序集合的数据类型
```sql
-- 创建枚举类型
create type weeks as enum('Mon','Tue','Wed','Thu','Fri','Sat','Sun');
-- 建表字段使用枚举类型
create table user_schedule (
    user_name varchar(100),
    available_day weeks
);
-- 插入数据
insert into user_schedule (user_name, available_day) values ('Alice', 'Mon');
```

### 几何类型
几何数据类型表示二维的平面物体  

| 类型	      | 大小	       | 描述	        | 表现形式              |
|----------|-----------|------------|-------------------|
| point	   | 16字节	     | 平面中的点      | 	(x,y)            |
| line	    | 32字节	     | 直线	        | ((x1,y1),(x2,y2)) |
| lseg	    | 32字节	     | 线段	        | ((x1,y1),(x2,y2)) |
| box	     | 32字节	     | 矩形	        | ((x1,y1),(x2,y2)) |
| path	    | 16+16n字节	 | 路径（与多边形相似） | 	((x1,y1),...)    |
| polygon	 | 40+16n字节	 | 多边形        | 	((x1,y1),...)    |
| circle	  | 24字节	     | 圆	         | <(x,y),r> (圆心和半径) |

```sql
-- 建表 创建一个表 geometric_shapes，它包含点、线和多边形类型的列。
create table geometric_shapes (
    id serial primary key,
    point_col point,
    lseg_col lseg,
    polygon_col polygon
);

-- 插入数据
insert into geometric_shapes (point_col, lseg_col, polygon_col)
values
(point(1, 2), lseg '[(0,0),(1,1)]', polygon '((0,0),(1,0),(1,1),(0,1))');
```

### JSON类型

```sql
-- 创建一个新表，名为 json_demo，包含一个 json 类型的列
create table json_demo (
    id serial primary key,
    data json
);

-- 向 json_demo 表插入 json 数据，注意 json 数据必须是单引号的字符串
-- 并且遵循 json 格式
insert into json_demo (data) values ('{"name": "张三", "age": 28, "city": "北京"}');

-- 使用 ->> 运算符来提取 json 对象中的 name 字段
select data->>'name' as name from json_demo;
```

### 数组类型

```sql
-- 创建一个新表，名为 array_demo，包含一个 int 类型的数组列
create table array_demo (
    id serial primary key,
    numbers int[]  -- int 数组类型列
);

-- 向 array_demo 表插入数组数据
-- 数组使用花括号{}并且元素由逗号分隔
insert into array_demo (numbers) values ('{1,2,3,4,5}');

-- 使用 unnest 函数来展开数组为一系列行
select unnest(numbers) as expanded_numbers from array_demo;
```

### 复合类型

```sql
-- 定义一个复合类型，名为 person_type，包含姓名、年龄和城市
create type person_type as (
    name text,
    age int,
    city text
);

-- 创建一个新表，名为 composite_demo，包含一个复合类型的列
create table composite_demo (
    id serial primary key,
    person_info person_type  -- 使用之前定义的复合类型作为列类型
);

-- 向 composite_demo 表插入复合类型数据
-- 复合类型数据使用括号，并且属性值由逗号分隔
insert into composite_demo (person_info) values (ROW('张三', 28, '北京'));
```


## DDL

### 数据库

#### schema
schema是数据库内部的一个"文件夹"或"命名空间"，用于逻辑上组织和隔离数据，以实现更好的数据管理和安全控制

#### 查询数据库
```
-- 仅命令行客户端支持
-- 查看所有数据库
\l
-- 查看所有schema
\dn

-- 可视化客户端
-- 查看所有数据库名称
select datname from pg_database;

-- 查看数据库大小
select
	pg_database.datname,
	pg_size_pretty(pg_database_size(pg_database.datname)) as size
from
	pg_database
order by
	pg_database_size(pg_database.datname) desc;
	

-- 查询schema 
SELECT schema_name FROM information_schema.schemata;
```

#### 创建数据库

```sql
-- 创建数据库
CREATE DATABASE dbname;
       
-- 创建schema
CREATE SCHEMA schema_name;
```

#### 切换数据库

```
-- 仅命令行客户端支持
\c dbname
```

#### 删除数据库

```sql
DROP DATABASE IF EXISTS dbname;
```

### 表

#### 查询表

```
-- 仅命令行客户端支持
-- 查看所有表
\d

-- 可视化客户端
-- 查看当前数据库下所有表名称
select
	tablename
from
	pg_catalog.pg_tables
where
	schemaname != 'pg_catalog'
	and schemaname != 'information_schema';
	
-- 查看表大小
select
	table_schema || '.' || table_name as table_name,
	pg_size_pretty(pg_total_relation_size('"' || table_schema || '"."' || table_name || '"')) as size
from
	information_schema.tables
order by
	pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') desc
```

#### 创建表

```sql
CREATE TABLE table_name(
   column1 datatype NOT NULL PRIMRAY KEY,
   column2 datatype,
   column3 datatype,
   columnN datatype
);
```

#### 修改表

```sql
-- 重命名表名
ALTER TABLE table_name RENAME TO new_table_name;

-- 新增列
ALTER TABLE table_name ADD COLUMN column_name [column_type];
-- 删除列
ALTER TABLE table_name DROP COLUMN column_name;
-- 修改列名
ALTER TABLE table_name RENAME column_name TO new_column_name;
-- 修改列类型
ALTER TABLE table_name ALTER COLUMN column_name TYPE column_type;
```

#### 删除表

```sql
DROP TABLE table_name;
```

#### 清除表

```sql
TRUNCATE TABLE table_name;
```

## DML

### 导入导出

```shell
# 备份数据库
pg_dump -U username -h localhost -p 5432 -d dbname -f dbname.bak

# 恢复数据库
psql -U username -h localhost -p 5432 -d dbname -f dbname.bak

# 备份表数据
pg_dump -U username -h localhost  -p 5432 -d dbname -t table_name -a -f table_name.sql
# 恢复表数据
psql -U username -h localhost -p 5432 -d dbname -f table_name.sql
```

参数说明:

1. -t 参数指定要导出的表名
2. -d 参数指定要导出的数据库名
3. -a 参数指定只导出数据而不导出表结构
4. -f 参数指定导出数据的文件名

注意点：在还原中往往会遇到异常，例如缺少postgis插件，缺少函数方法等，根据报错日志配置环境即可。

## 存储过程

### 优点

- 减少应用和数据库之间的网络传输。所有的 SQL 语句都存储在数据库服务器中，应用程序只需要发送函数调用并获取除了结果，避免了发送多个
  SQL 语句并等待结果。
- 提高应用的性能。因为自定义函数和存储过程进行了预编译并存储在数据库服务器中。
- 可重用性。存储过程和函数的功能可以被多个应用同时使用。

### 缺点

- 调试麻烦，问题不容易排查
- 移植问题，数据库端代码与数据库相关，不同的数据库语法有所不同
- 维护问题，如果在一个程序系统中大量的使用存储过程，到程序交付使用的时候随着用户需求的增加会导致数据结构的变化，这时涉及到存储过程修改和维护

### 代码块示例

```plpgsql
DO $$ 
DECLARE
  name text;
BEGIN 
  name := 'PL/pgSQL';
  RAISE NOTICE 'Hello %!', name;
END $$;
```

以上是一个匿名块，与此相对的是命名块（也就是存储过程和函数）。其中，DO 语句用于执行匿名块；我们定义了一个字符串变量
name，然后给它赋值并输出一个信息；RAISE NOTICE 用于输出通知消息。

### 变量

```
-- 变量申明
variable_name data_type [ NOT NULL ] [ { DEFAULT | := | = } expression ];

-- 示例
user_id integer;
quantity numeric(5) DEFAULT 0;
url varchar := 'http://mysite.com';
```

### 常量

如果在定义变量时指定了 CONSTANT 关键字，意味着定义的是常量。常量的值需要在声明时初始化，并且不能修改。

```
PI CONSTANT NUMERIC := 3.14159265;
```

### 控制结构

#### IF语句

IF 语句可以基于条件选择性执行操作， PL/pgSQL 提供了三种形式的 IF 语句。

- IF ... THEN ... END IF
- IF ... THEN ... ELSE ... END IF
- IF ... THEN ... ELSIF ... THEN ... ELSE ... END IF

```
-- 初始化字典表
DO $$
BEGIN
    if (select count(*) from sys_dict_data)<1
    then insert into sys_dict_data(dict_code,dict_sort,dict_label,dict_value,status,create_time,update_time,remark) values(1,0,'city','china',0,'2022-10-19','2022-10-19','remark');
    end if;
END $$;
```

#### 循环语句

```
-- 
DO $$
DECLARE
  i integer := 0;
BEGIN 
  LOOP
    EXIT WHEN i = 10;
    i := i + 1;
    CONTINUE WHEN mod(i, 2) = 1;
    RAISE NOTICE 'Loop: %', i;
  END LOOP;
END $$;
```

### 错误处理

PL/pgSQL 提供了 RAISE 语句，用于打印消息或者抛出错误：

```
RAISE level format;
```

不同的 level 代表了错误的不同严重级别，包括：

- DEBUG
- LOG
- NOTICE
- INFO
- WARNING
- EXCEPTION

### 自定义函数

```
-- 定义求和函数
CREATE OR REPLACE FUNCTION sum_num(
  VARIADIC nums numeric[])
  RETURNS numeric
AS $$
DECLARE ln_total numeric;
BEGIN
  SELECT SUM(nums[i]) INTO ln_total
  FROM generate_subscripts(nums, 1) t(i);

  RETURN ln_total;
END; $$
LANGUAGE plpgsql;

-- 调用
select sum_num(1,2,3);
```

如果函数不需要返回结果，可以返回 void 类型；或者直接使用存储过程

### 存储过程

存储过程使用 CREATE PROCEDURE 语句创建

存储过程的定义和函数主要的区别在于没有返回值，其他内容都类似。

在存储过程内部，可以使用 COMMIT 或者 ROLLBACK 语句提交或者回滚事务。

```
CREATE OR REPLACE PROCEDURE update_emp(
  p_empid in integer,
  p_salary in numeric,
  p_phone in varchar)
AS $$
BEGIN
  update employees 
  set salary = p_salary,
      phone_number = p_phone
  where employee_id = p_empid;
END; $$
LANGUAGE plpgsql;
```


