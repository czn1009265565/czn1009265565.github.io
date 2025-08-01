# Python字符串
Python 内置的字符串方法提供了丰富的文本处理功能

## 大小写转换

| 方法            | 描述        |
|---------------|-----------|
| `str.lower()` | 将字符串转换为小写 |
| `str.upper()` | 将字符串转换为大写 |

## 字符串格式化

| 方法                  | 描述         | 示例                                                   |
|---------------------|------------|------------------------------------------------------|
| `str.format()`      | 格式化字符串（推荐） | `"{} {}".format("hello", "world")` → `'hello world'` |
| `str.zfill(width)`  | 左侧填充0到指定宽度 | `"1".zfill(5)` → `'00001'`                           |
| `str.center(width)` | 居中并用空格填充   | `"hi".center(5)` → `' hi  '`                         |
| `str.ljust(width)`  | 左对齐并填充     | `"hi".ljust(4)` → `'hi  '`                           |
| `str.rjust(width)`  | 右对齐并填充     | `"hi".rjust(4)` → `'  hi'`                           |

## 字符串修改

| 方法                      | 描述                    | 示例                                       |
|-------------------------|-----------------------|------------------------------------------|
| `str.strip()`           | 移除两端空白符（含`\n`, `\t`等） | `"  hi  ".strip()` → `'hi'`              |
| `str.lstrip()`          | 移除左端空白符               | `"  hi  ".lstrip()` → `'hi  '`           |
| `str.rstrip()`          | 移除右端空白符               | `"  hi  ".rstrip()` → `'  hi'`           |
| `str.replace(old, new)` | 替换子串                  | `"hello".replace("l", "L")` → `'heLLo'`  |
| `str.join(iterable)`    | 用字符串连接可迭代对象           | `",".join(["a", "b"])` → `'a,b'`         |
| `str.split(sep=None)`   | 按分隔符分割为列表（默认按空白符分割）   | `"a,b,c".split(",")` → `['a', 'b', 'c']` |

## 字符串查找与判断

| 方法                       | 描述                            | 示例                                  |
|--------------------------|-------------------------------|-------------------------------------|
| `str.find(sub)`          | 返回子串首次出现的索引（未找到返回-1）          | `"python".find("th")` → `2`         |
| `str.index(sub)`         | 类似`find()`，但未找到抛出`ValueError` | `"python".index("py")` → `0`        |
| `str.startswith(prefix)` | 检查是否以指定前缀开头                   | `"hello".startswith("he")` → `True` |
| `str.endswith(suffix)`   | 检查是否以指定后缀结尾                   | `"world".endswith("ld")` → `True`   |
| `str.count(sub)`         | 统计子串出现次数                      | `"banana".count("a")` → `3`         |
| `str.isalpha()`          | 检查是否全为字母                      | `"abc".isalpha()` → `True`          |
| `str.isdigit()`          | 检查是否全为数字                      | `"123".isdigit()` → `True`          |
| `str.isalnum()`          | 检查是否由字母或数字组成                  | `"a1b2".isalnum()` → `'True'`       |