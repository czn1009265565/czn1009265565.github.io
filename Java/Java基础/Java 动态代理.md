# Java 动态代理

## 背景
动态代理提供了一种灵活且非侵入式的方式，可以对对象的行为进行定制和扩展。它在代码重用、解耦和业务逻辑分离、性能优化以及系统架构中起到了重要的作用。

- 增强对象的功能: 通过动态代理，可以在不修改原始对象的情况下，对其方法进行增强或添加额外的行为。
  可以在方法执行前后进行一些操作，比如日志记录、性能监测、事务管理等。
- 解耦和业务逻辑分离: 动态代理可以将对象的特定操作从业务逻辑中解耦，使得代码更加模块化和可维护。
  代理对象可以负责处理一些通用的横切关注点，而业务对象可以专注于核心业务逻辑。
- 实现懒加载: 通过动态代理，可以延迟加载对象，只有在真正需要使用对象时才会进行创建和初始化，从而提高性能和资源利用效率。
- 实现远程方法调用: 动态代理可以用于实现远程方法调用(RPC)和分布式系统中的服务代理。客户端通过代理对象调用远程服务，并隐藏了底层网络通信的细节。
- 实现AOP编程: 动态代理是实现面向切面编程(AOP)的基础。通过代理对象，可以将横切关注点（如日志、事务、安全性）与业务逻辑进行解耦，
  提供更高层次的模块化和可重用性。


在Java中，实现动态代理主要有JDK动态代理与CGLIB动态代理，相较性能来说，JDK动态代理更优秀，随着 `JDK` 版本的升级，这个优势更加明显。

## JDK动态代理
基于Java的反射机制实现。JDK动态代理要求目标对象必须实现一个或多个接口，
因为代理类是通过继承java.lang.reflect.Proxy类并实现与目标对象相同的接口来创建的。
因此，JDK动态代理主要用于对接口进行代理。

这里以短信接口为例

定义短信接口

```java
public interface SmsService {
    String send(String message);
}
```
短信实现类

```java
public class SmsServiceImpl implements SmsService {
    public String send(String message) {
        System.out.println("send message:" + message);
        return message;
    }
}
```

代理类及使用

```java
public class JDKInvocationHandler implements InvocationHandler {
    /**
     * 代理类中的真实对象
     */
    private final Object target;

    public JDKInvocationHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws InvocationTargetException, IllegalAccessException {
        //调用方法之前，我们可以添加自己的操作
        System.out.println("before method " + method.getName());
        Object result = method.invoke(target, args);
        //调用方法之后，我们同样可以添加自己的操作
        System.out.println("after method " + method.getName());
        return result;
    }

    public static void main(String[] args) {
        // 初始化被代理对象
        SmsService smsService = new SmsServiceImpl();
        // 创建代理对象对象
        SmsService proxyInstance = (SmsService) Proxy.newProxyInstance(
                smsService.getClass().getClassLoader(), // 目标类的类加载器
                smsService.getClass().getInterfaces(),  // 代理需要实现的接口，可指定多个
                new JDKInvocationHandler(smsService));
        // 方法调用
        proxyInstance.send("message");
    }
}
```

## CGLIB动态代理
基于ASM（一个通用的Java字节码操作和分析框架）库实现对类的字节码操作。
与JDK动态代理不同，CGLIB动态代理是通过继承目标类来创建代理类的，因此它主要用于对没有实现接口的类进行代理。
由于CGLIB是通过继承目标类来创建代理的，因此不能代理final类（因为final类不能被继承），同时目标类中的final方法也会被忽略（因为final方法不能被重写）。

引入依赖  
```xml
<dependency>
    <groupId>cglib</groupId>
    <artifactId>cglib</artifactId>
    <version>3.3.0</version>
</dependency>
```

定义短信发送类

```java
public class SmsSender {
    public String send(String message) {
        System.out.println("send message:" + message);
        return message;
    }
}
```

代理类及使用

```java
public class CglibInvocationHandler implements MethodInterceptor {
    /**
     * @param o           被代理的对象（需要增强的对象）
     * @param method      被拦截的方法（需要增强的方法）
     * @param args        方法入参
     * @param methodProxy 用于调用原始方法
     */
    @Override
    public Object intercept(Object o, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
        //调用方法之前，我们可以添加自己的操作
        System.out.println("before method " + method.getName());
        Object object = methodProxy.invokeSuper(o, args);
        //调用方法之后，我们同样可以添加自己的操作
        System.out.println("after method " + method.getName());
        return object;
    }

    public static void main(String[] args) {
        // 创建动态代理增强类
        Enhancer enhancer = new Enhancer();
        // 设置类加载器
        enhancer.setClassLoader(SmsSender.class.getClassLoader());
        // 设置被代理类
        enhancer.setSuperclass(SmsSender.class);
        // 设置方法拦截器
        enhancer.setCallback(new CglibInvocationHandler());
        // 创建代理类
        SmsSender smsSender = (SmsSender) enhancer.create();
        smsSender.send("message");
    }
}
```