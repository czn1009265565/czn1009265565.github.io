# Java 反射

Java反射给我们提供了在运行时检查甚至修改应用行为的机制。 反射是java高级的核心技术，所有有经验的程序员都应该理解。

通过反射机制，我们可以在运行时检视 类、接口、枚举，获得他们的结构、方法以及属性信息，即使在编译期类是不可访问的。   我们也可以通过反射创建类实例，调用它的方法，或者改变属性值。

## 反射缺点

但是不建议在正常编程中滥用反射技术，因为我们拥有自己编写的类的访问权限了，反射存在以下几个缺陷：

-  **性能较差**   尽管反射解决了动态类型的问题，但是也引入了在classpath 扫描类进行加载的过程，会影响性能。

-  **安全限制**  反射需要在运行时获得访问权限，但是在security manager中可能是不允许的。  这可能会导致应用运行失败。

-  **安全问题**  通过反射我们可以访问那些不建议我们访问的类，例如我们可以访问private的属性并修改其值。  这可能引发安全问题导致应用异常。

-  **较高的维护代价**  反射相关的代码难以理解以及调试，代码的错误不能在编译期展现出来，使用反射的代码灵活性不高并难以维护。

## 反射的使用

### 获得Class对象

```java
public class ReflectionTest {

    public static void main(String[] args) throws ClassNotFoundException {
        Class c1 = Object.class;
        Class c2 = new Object().getClass();
        Class c3 = Class.forName("java.lang.Object");

        // 获取原始类型和包装类型
        Class primative = boolean.class;
        Class doubleClass = Double.TYPE;
    }
}
```

### 获取类信息

```java
@NoArgsConstructor
@AllArgsConstructor
public class Human {
    public String name;
    private Double height;
    private Double weight;

    public static class Man extends Human implements Animal{
        @Override
        public void eat(Object object) {}

        private void drink(Object object) {}
    }
    public static class Woman extends Human {
    }
    public interface Animal {
        void eat(Object object);
    }

    public static void main(String[] args) throws Exception {
        // 获取类名
        String name = Human.class.getName();
        // 获取定义该class的类
        Class<?> declaringClass = Woman.class.getDeclaringClass();
        // 获取包名
        String name = Human.class.getPackage().getName();
        // 获取class实现的接口
        Class<?>[] interfaces = Man.class.getInterfaces();
        // 获取所有的public方法
        Method[] methods = Man.class.getMethods();
        // 获取所有public构造器
        Constructor<?>[] constructors = Man.class.getConstructors();
        // 获取所有public属性
        Field[] fields = Man.class.getFields();
        // 获取所有注解
        Annotation[] annotations = Man.class.getAnnotations();
        // 获取属性的类型
        Class<?> nameClass = Human.class.getField("name").getType();
        System.out.println(nameClass);
        // Get/Set私有属性 由于这里的height、weight是私有属性，因此在其他类中访问是需要取消Java 语言访问检查
        Field height = Human.class.getDeclaredField("height");
        height.setAccessible(true);
        Human human = new Human("H", 180D,180D);
        height.set(human, 185D);
        Object heightValue = height.get(human);
        System.out.println(heightValue);
        // 调用public方法
        Method eat = Man.class.getMethod("eat", Object.class);
        eat.invoke(new Man(), new Object());
        // 调用private方法
        Method drink = Man.class.getDeclaredMethod("drink", Object.class);
        drink.setAccessible(true);
        drink.invoke(new Man(), new Object());
        // 初始化对象实例
        Man man = Man.class.newInstance();
    }
}
```

