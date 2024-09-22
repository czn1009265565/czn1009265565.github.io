## Java 单例
单例模式是一种创建型设计模式，它确保一个类只有一个实例，并提供了一个全局访问点来访问该实例

1. 单例类只能有一个实例
2. 单例类必须自己创建自己的唯一实例
3. 单例类必须给所有其他对象提供这一实例

### 饿汉式
- 优点：没有加锁，执行效率会提高
- 缺点：类加载时就初始化，浪费内存

```java
public class Singleton {
    private Singleton() {
    }

    public static final Singleton instance = new Singleton();

    public static Singleton getInstance() {
        return instance;
    }
}
```


### 懒汉式(线程不安全)
这种方式是最基本的实现方式，这种实现最大的问题就是不支持多线程。因为没有加锁 synchronized，所以严格意义上它并不算单例模式。

```java
public class Singleton {
    private Singleton() {}
    private static Singleton single=null;
    //静态工厂方法 
    public static Singleton getInstance() {
        if (single == null) {
            single = new Singleton();
        }
        return single;
    }
}
```


### 懒汉式(线程安全)

```java
class SingletonLazy {
    private SingletonLazy() {
    }

    private static class LazyHolder{
        public static final SingletonLazy instance = new SingletonLazy();
    }

    public static SingletonLazy getInstance() {
        return LazyHolder.instance;
    }
}
```

一般情况下建议使用饿汉式。只有在要明确实现 lazy loading 效果时，才会采用该静态内部类方式。