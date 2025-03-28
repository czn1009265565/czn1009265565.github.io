# Java 正则表达式

正则表达式用于文本内容的查找和替换

## Pattern与Matcher
Pattern和Matcher类是Java中用于处理正则表达式的两个核心类


Pattern类用于定义正则表达式模式

- `compile(String regex)`: 编译一个正则表达式
- `matches(String regex, CharSequence input)`: 在输入字符串中进行匹配操作
- `split(CharSequence input)`: 根据正则表达式分割输入字符串
- `pattern()`: 返回正则表达式的字符串表示‌

Matcher类用于在给定的输入字符串中进行匹配操作

- `matches()`: 判断整个输入字符串是否匹配正则表达式
- `find()`: 在输入字符串中查找与正则表达式匹配的子串
- `group()`: 返回上一次匹配的子串，等同于`group(0)`默认返回匹配到的整个字符串
- `start()`: 返回上一次匹配子串在输入字符串中的开始位置
- `end()`: 返回上一次匹配子串在输入字符串中的结束位置加1
- `reset(CharSequence input)`: 重置Matcher对象，使其在新的输入字符串上重新进行匹配操作‌


## 正则表达式语法

```
\ 转义字符。例如，\\n匹配\n，\n匹配换行符，\(匹配(
^匹配输入字符串的开始位置。如果设置了RegExp对象的Multiline属性，^也匹配“\n”或“\r”之后的位置。
$匹配输入字符串的结束位置。如果设置了RegExp对象的Multiline属性，$也匹配“\n”或“\r”之前的位置。
*匹配前面的子表达式任意次。例如，zo*能匹配“z”，“zo”以及“zoo”。*等价于{0,}
+匹配前面的子表达式一次或多次(大于等于1次)。例如，“zo+”能匹配“zo”以及“zoo”，但不能匹配“z”。+等价于{1,}。
?匹配前面的子表达式零次或一次。例如，“do(es)?”可以匹配“do”或“does”中的“do”。?等价于{0,1}。
{n}n是一个非负整数。匹配确定的n次。例如，“o{2}”不能匹配“Bob”中的“o”，但是能匹配“food”中的两个o。
{n,}n是一个非负整数。至少匹配n次。例如，“o{2,}”不能匹配“Bob”中的“o”，但能匹配“foooood”中的所有o。“o{1,}”等价于“o+”。“o{0,}”则等价于“o*”。
{n,m}m和n均为非负整数，其中n<=m。最少匹配n次且最多匹配m次。例如，“o{1,3}”将匹配“fooooood”中的前三个o。“o{0,1}”等价于“o?”。请注意在逗号和两个数之间不能有空格。
x|y匹配x或y
[xyz]字符集合。匹配所包含的任意一个字符。
[^xyz]负值字符集合。匹配未包含的任意字符。
[a-z]字符范围。匹配指定范围内的任意字符。例如，“[a-z]”可以匹配“a”到“z”范围内的任意小写字母字符。
[^a-z]负值字符范围。匹配任何不在指定范围内的任意字符。例如，“[^a-z]”可以匹配任何不在“a”到“z”范围内的任意字符。
.可以匹配任何字符
\d匹配一个数字字符。等价于[0-9]
\D匹配一个非数字字符。等价于[^0-9]
\s匹配所有的空白字符，包括空格、制表符、换页符、换行符、回车符 等等。等价于[ \f\n\r\t\v]。
\S匹配所有的非空白字符
\w匹配一个任何字母(包括大写和小写字母)和数字字符
\W匹配一个非字母，即非大小写、数字
```

## 最佳实践

```java
public class RegexTest {

    public static void main(String[] args) {
        // 格式校验
        Pattern pattern = Pattern.compile("^1[3-9]\\d{9}$");
        Matcher m1 = pattern.matcher("12345678910");
        Matcher m2 = pattern.matcher("13456789101");
        System.out.println(m1.matches());
        System.out.println(m2.matches());

        // 查找匹配字符串
        pattern = Pattern.compile("Java\\d{1,2}");
        Matcher matcher = pattern.matcher("Java8和Java11是长期支持版本");
        while (matcher.find()) {
            String content = matcher.group(0);
            System.out.println(content);
        }

        // 替换
        Pattern p = Pattern.compile("cat");
        Matcher m = p.matcher("one cat two cats in the yard");

        // 追加替换
        StringBuilder sb = new StringBuilder();
        while (m.find()) {
            m.appendReplacement(sb, "dog");
        }
        m.appendTail(sb);
        System.out.println("appendReplacement: " + sb.toString());

        // 替换第一个
        String replaceFirst = m.replaceFirst("dog");
        System.out.println("replaceFirst: " + replaceFirst);
        // 替换所有
        String replaceAll = m.replaceAll("dog");
        System.out.println("replaceAll: "+ replaceAll);
    }
}
```

