## Java 单例


### 饿汉式

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


### 懒汉式
线程不安全

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


线程安全

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
