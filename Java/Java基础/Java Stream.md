# Stream流

### 流的创建
1. Collection接口的的stream方法，可以将任何集合转换为一个流,其中Map的stream流为(k,v)的形式
2. Stream.of()方法，支持可变长参数，也支持数组
3. Arrays.stream(array,from,to) 包括from,不包括to的元素中创建一个流
4. Arrays.steram(array)整个数组转换为一个流

### filter、map、flatMap、sorted
流的转换产生一个新的流，新流的元素派生自另一个流中的元素。
```
List<String> wordList = Arrays.asList("i", "love", "Python", "and", "Java");
// filter
Stream<String> longWords = wordList.stream().filter(s -> s.length() > 1);

// map
Stream<String> lowWords = wordList.stream().map(i -> i.toLowerCase());

// flatMap
Stream<Stream<String>> result = wordList.stream().map(i->letters(i));
Stream<String> result = wordList.stream().flatMap(i->letters(i));

// sorted
wordList.stream().sorted(Comparator.comparingInt(String::length)).forEach(System.out::println);
```

### 条件判断
1. anyMatch表示，判断的条件里，任意一个元素成功，返回true

2. allMatch表示，判断条件里的元素，所有的都是，返回true

3. noneMatch跟allMatch相反，判断条件里的元素，所有的都不是，返回true


### 抽取子流和连接流

`stream.limit(n)`返回一个新的流，在n个元素之后结束

### distinct

`distinct`会返回一个流，元素从原有流产生，按照同样顺序剔除重复数据后得到。 比较操作调用的是对象的equals方法


### 约简操作
将流约简为可以在程序中使用的非流值

1.count()返回流中元素的数量

2.min,max

```
List<String> wordList = Arrays.asList("i", "love", "Python", "and", "Java");
Optional<String> result = wordList.stream().max(Comparator.comparingInt(i->i.length()));
// System.out.println(result.get());
System.out.println(result.orElse("")); // 解决空流返回null的问题
```

3.reduce

```
List<Integer> values = Arrays.asList(1,2,3,4,5);
int length = values.stream().reduce((x,y)->x+y).orElse(0);
```

### 收集结果
我们往往需要将返回的结果收集到数据结构中，这里介绍forEach和collect

**注意点forEach传入action(没有返回值的函数或者lambda表达式)**

```
List<String> wordList = Arrays.asList("i", "love", "Python", "and", "Java");

List<String> result = new ArrayList<>();
wordList.stream().filter(i->i.length()>3).forEach(i->result.add(i));

// 等价
List<String> result2 = wordList.stream().filter(i->i.length()>3).collect(Collectors.toList());
```

数组、集合、映射表
```
wordList.stream().filter(i->i.length()>3).collect(Collectors.toList());
wordList.stream().filter(i->i.length()>3).collect(Collectors.toSet());
Map<String,Integer> map = wordList.stream().filter(i->i.length()>3).collect(Collectors.toMap(i->i, i->i.length()));

// 关于toMap key重复问题的补充
Map<Long, String> map = userList.stream().collect(Collectors.toMap(User::getId, User::getUsername, (v1, v2) -> v1));
```
注意点: 在toMap中，key可以为null,但是value不能为null,因此最好增加filter过滤，过滤value为空数据

groupBy 聚合
```
List<String> arrs = Arrays.asList("a", "b", "c", "d", "a");
Map<String, Long> r1 = arrs.stream().collect(Collectors.groupingBy(i -> i, Collectors.counting()));
Map<String, List<String>> r2 = arrs.stream().collect(Collectors.groupingBy(i -> i, Collectors.toList()));
Map<String, List<String>> r2 = arrs.stream().collect(Collectors.groupingBy(i -> i, Collectors.mapping(i -> i + "i", Collectors.toList())));
```
