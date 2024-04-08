# Numpy

### 数据类型

- 布尔型（bool_）。用于表示逻辑值，可以是True或False
- 整型。包括int8、int16、int32、int64等，表示有符号整数。这些类型分别代表不同大小的整数，例如，int8的值的范围是-128到127
- 无符号整型。包括uint8、uint16、uint32、uint64等，用于表示无符号整数，例如，uint8的值的范围是0到255
- 浮点型。包括float16、float32、float64等，用于表示浮点数值，这些类型的精度和表示范围不同
- 复数型。包括complex64和complex128等，用于表示复数值
- 字符串型。包括str_和unicode_等，用于表示字符串数据
- 日期时间类型。datetime64，用于表示日期和时间
- 时间间隔类型。timedelta64，表示两个时间点之间的间隔

对于每种类型都有同名的转换函数可以将数据转为对应数据类型的数据:  
```python
import numpy as np

np.bool_(True)
np.int32(1)
np.float32(1.0)
np.datetime64('2024-04-08 19:58:00')
```

### 数组创建


### 数学与统计函数

np.abs()/np.fabs()	计算数组各元素的绝对值
np.sqrt()	计算数组各元素的平方根
np.square()	计算数组各元素的平方
np.log(x)/np.log10(x)/np.log2(x)	计算数组各元素的自然对数、10底对数和2底对数
np.ceil(x),np.floor(x)	计算数组各元素的ceiling值或floor值
np.rint(x)	计算数组各元素的四舍五入值
np.modf(x)	将数据各元素的整数和小数部分以两个独立的数组形式返回
np.cos/cosh/sin/sinh/tan/tanh	计算数据各元素的普通型和双典型的三角函数
np.exp(x)	计算数组各元素的指数值