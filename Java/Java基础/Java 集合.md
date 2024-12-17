# Java 集合
集合(也可以叫容器)主要包括 `Collection` 和 `Map` 两种，`Collection` 存储着对象的集合，而 `Map` 存储着键值对(两个对象)的映射表

## Collection
这里先介绍下一些术语:  
- 哈希表: 哈希函数+数组+链表/红黑树

### Set

- TreeSet: 基于红黑树实现，支持有序性操作
- HashSet: 基于哈希表实现，支持快速查找，但不支持有序性操作
- LinkedHashSet: 基于哈希表+双向链表实现，具有 `HashSet` 的查找效率，且内部使用双向链表维护元素的插入顺序

### List

- ArrayList: 基于动态数组实现，支持下标随机访问
- LinkedList: 基于双向链表实现，只能顺序访问，但是可以快速地在链表中间插入和删除元素。不仅如此，LinkedList 还可以用作栈、队列和双向队列

### Map

- TreeMap: 基于红黑树实现
- HashMap: 基于哈希表实现
- HashTable: 和 `HashMap` 类似，但它是线程安全的，这意味着同一时刻多个线程可以同时写入 `HashTable` 并且不会导致数据不一致。它是遗留类，不应该去使用它。现在可以使用 `ConcurrentHashMap` 来支持线程安全，并且 `ConcurrentHashMap` 的效率会更高，因为 `ConcurrentHashMap` 引入了分段锁
- LinkedHashMap: 基于哈希表+双向链表实现，使用双向链表来维护元素的顺序


## ArrayList
底层通过数组实现，每个ArrayList都有一个容量(capacity)，表示底层数组的实际大小，
容器内存储元素的个数不能多于当前容量。当向容器中添加元素时，如果容量不足，容器会触发自动扩容。

### 数据结构  
```
transient Object[] elementData;

private int size;
```

### 基础API  
```java
public class ArrayListTest {

    public static void main(String[] args) {
        // 初始化
        List<String> arrayList = new ArrayList<>();
        List<String> arrayList2 = new ArrayList<>(10);
        List<String> arrayList3 = new ArrayList<>(Collections.emptyList());

        // 添加元素
        arrayList.add("A");
        arrayList.addAll(Arrays.asList("B", "C"));
        arrayList.addAll(3, Arrays.asList("D", "E"));

        // 基于下标设置元素
        arrayList.set(0, "A1");

        // 基于下标获取元素
        String value = arrayList.get(0);

        // 移除指定下标元素
        arrayList.remove(0);
        // 移除第一个满足Object.equals的元素
        arrayList.remove("A");

        // 获取元素第一次出现的下标，不存在则返回-1
        int index = arrayList.indexOf("A");
        // 获取元素最后一次出现的下标，不存在则返回-1
        int lastIndex = arrayList.lastIndexOf("A");
    }
}
```

## LinkedList
底层通过双向链表实现，实现了List和Deque接口，既可以看作一个顺序容器，也可以看作一个队列(Queue)，同时又可以看作一个栈(Stack)。
当你需要使用栈或者队列时，可以考虑使用LinkedList。
关于栈或队列，现在的首选是ArrayDeque，它有着比LinkedList(当作栈或队列使用时)有着更好的性能。

### 数据结构
双向链表的每个节点用内部类Node表示。LinkedList通过first和last引用分别指向链表的第一个和最后一个元素。

```
transient int size = 0;

transient Node<E> first;

transient Node<E> last;
```

### 基础API

```java
public class LinkedListTest {
    public static void main(String[] args) {
        // 初始化
        LinkedList<String> linkedList = new LinkedList<>();
        LinkedList<String> linkedList2 = new LinkedList<>(Collections.emptyList());

        // 添加元素
        linkedList.add("A");
        linkedList.add(1, "B");
        linkedList.addAll(Arrays.asList("C","D"));
        linkedList.addAll(4, Arrays.asList("E","F"));
        linkedList.addFirst("A1");
        linkedList.addLast("G");

        // 获取第一个与最后一个元素
        String first = linkedList.getFirst();
        String last = linkedList.getLast();

        // 移除第一个与最后一个元素
        linkedList.removeFirst();
        linkedList.removeLast();
        // 移除指定下标元素
        linkedList.remove(0);
        // 移除第一个满足Object.equals的元素
        linkedList.remove("A");

        // 基于下标获取元素
        String value = linkedList.get(0);
        // 基于下标设置元素
        linkedList.set(0, "A0");

        // 快速清空(设置引用关系与节点值为null)
        linkedList.clear();
        
        // Deque、Queue接口...
        
    }
}
```


## HashMap
在Java7中，HashMap底层基于 `哈希函数+数组+链表` 实现，
Java8 对 `HashMap` 进行了一些优化，最大的不同就是引入了红黑树，所以其由 `哈希函数+数组+链表+红黑树` 组成。

Java7中HashMap的查找是根据 hash 值快速定位到数组的具体下标，但是相同下标下存在多个值时，需要顺着链表一个个比较下去才能找到我们需要的，
时间复杂度取决于链表的长度，为 O(n)。为了降低这部分的开销，在 Java8 中，当链表中的元素达到了 8 个时，会将链表转换为红黑树，
在这些位置进行查找的时候可以降低时间复杂度为 O(logN)。

### put过程

1. 计算key的hash值
2. 根据hash值定位到bucket位置，如果该bucket为空，则直接放入
3. 如果bucket不为空，且key已存在，则替换其value
4. 如果bucket不为空，且key不存在，则链接到链表的尾部
5. 如果链表长度超过阈值(TREEIFY_THRESHOLD, 默认为8)，则将链表转换为红黑树
6. 如果HashMap的size超过了load factor (加载因子的乘积) 且map进行了resize操作，则需要rehash


### get过程
1. 计算key的hash值
2. 定位到bucket位置
3. 如果bucket为空，则返回null
4. 如果bucket不为空，则查找对应的entry
5. 如果entry在红黑树中，则进行红黑树的查找
6. 如果entry在链表中，则进行链表的查找

### 基本API

```java
public class HashMapTest {
    public static void main(String[] args) {
        // 初始化
        Map<String, String> map = new HashMap<>();
        Map<String, String> map2 = new HashMap<>(16);
        Map<String, String> map3 = new HashMap<>(Collections.emptyMap());

        // put
        map.put("key", "value");
    
        // get
        String value = map.get("key");
        String defaultValue = map.getOrDefault("key", "default");
    }
}
```