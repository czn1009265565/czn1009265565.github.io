# Java 集合
集合主要包括 `Collection` 和 `Map` 两种，`Collection` 存储着对象的集合，而 `Map` 存储着键值对(两个对象)的映射表

## Collection

哈希表: 哈希函数+数组+链表/红黑树

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
