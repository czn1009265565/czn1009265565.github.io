# Java BigDecimal

一般情况下，对于那些不需要准确计算精度的数字，我们可以直接使用Float和Double处理，但是Double.valueOf(String) 和Float.valueOf(String)会丢失精度。所以开发中，如果我们需要精确计算的结果，则必须使用BigDecimal类来操作。

## 常用构造函数

- BigDecimal(int)
- BigDecimal(long)
- BigDecimal(double)
- BigDecimal(String)

#### 存在的问题

```
BigDecimal num1 = new BigDecimal(0.1);
BigDecimal num2 = new BigDecimal("0.1");

System.out.println(num1);
System.out.println(num2);

0.1000000000000000055511151231257827021181583404541015625
0.1
```

1. 参数类型为double的构造方法的结果有一定的不可预知性
2. String 构造方法是完全可预知的
3. 当double必须用作BigDecimal的源时,建议使用`BigDecimal.valueOf(double)`


## 常用方法

- add(BigDecimal)

BigDecimal对象中的值相加，返回BigDecimal对象

- subtract(BigDecimal)

BigDecimal对象中的值相减，返回BigDecimal对象

- multiply(BigDecimal)

BigDecimal对象中的值相乘，返回BigDecimal对象

- divide(BigDecimal)

BigDecimal对象中的值相除，返回BigDecimal对象,若存在除不尽的情况则抛出 `no exact representable decimal result`异常

- divide(BigDecimal divisor, int scale, int roundingMode)

BigDecimal对象中的值相除，返回BigDecimal对象,并保留scale位小数,roundingMode比较常用的是`BigDecimal.ROUND_HALF_UP`表示四舍五入

- toString()

将BigDecimal对象中的值转换成字符串

- doubleValue()

将BigDecimal对象中的值转换成双精度数

- floatValue()

将BigDecimal对象中的值转换成单精度数

- longValue()

将BigDecimal对象中的值转换成长整数

- intValue()

将BigDecimal对象中的值转换成整数

## 大小比较

BigDecimal比较大小推荐使用bigdemical的compareTo方法，

equals方法会比较两部分内容，分别是值（value）和精度（scale），compareTo则忽略精度

| 返回值 | 	含义                  |
|-----|----------------------|
| -1  | 	当前 BigDecimal 小于参数值 |
| 0   | 	当前 BigDecimal 等于参数值 |
| 1   | 	当前 BigDecimal 大于参数值 |

## 格式化

- setScale(int newScale, int roundingMode)

```
BigDecimal a = BigDecimal.valueOf(0.725);
BigDecimal b = a.setScale(2, RoundingMode.HALF_UP);
System.out.println(a);
System.out.println(b);
```

