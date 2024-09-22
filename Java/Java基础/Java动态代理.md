# Java动态代理

代理类在程序运行时创建的代理方式被成为动态代理。在静态代理中，代理类（RenterProxy）是自己已经定义好了的，在程序运行之前就已经编译完成。而动态代理是在运行时根据我们在Java代码中的“指示”动态生成的。动态代理相较于静态代理的优势在于可以很方便的对代理类的所有函数进行统一管理，如果我们想在每个代理方法前都加一个方法，如果代理方法很多，我们需要在每个代理方法都要写一遍，很麻烦。而动态代理则不需要。

- JDK动态代理: 利用反射原理,动态的生成代理类,将类的载入延迟到程序执行之中,解耦了代理类和被代理类的联系.主要要实现InvationHandler接口.

- CGLIB动态代理:原理是继承,把被代理类作为父类,动态生成被代理类的子类,三个步骤,设置父类,设置回调函数,创建子类.实现MethodInterceptor 接口,拦截调用父类方法时,会处理回调方法,处理自己的增强方法.

## 应用场景

1. 方法性能监测，看一个方法的调用执行时间
2. 日志管理，记录一个方法的前后执行情况
3. 缓存，在一个方法执行前读取缓存

## JDK动态代理实例

将车站的售票服务抽象出一个接口`TicketService`,包含问询，卖票，退票功能,
车站类`Station`实现了`TicketService`接口，车票代售点`StationProxy`则实现了代理角色的功能。
从静态代理与动态代理两种实现方式进行对比：

TicketService
```java
public interface TicketService {
    //售票
    void sellTicket();
    //问询
    void inquire();
    //退票
    void withdraw();
}
```

Station
```java
public class Station implements TicketService{
        @Override
        public void sellTicket() {
            System.out.println("售票......");
        }
        @Override
        public void inquire() {
            System.out.println("问询......");
        }
        @Override
        public void withdraw() {
            System.out.println("退票......");
        }
}

```

### 静态代理
```java
public class StationStaticProxy implements TicketService {

    private Station station;

    public StationStaticProxy(Station station){
        this.station = station;
    }

    @Override
    public void sellTicket() {
        hi();
        station.sellTicket();
        bye();
    }

    @Override
    public void inquire() {
        hi();
        station.inquire();
        bye();
    }

    @Override
    public void withdraw() {
        hi();
        station.withdraw();
        bye();
    }

    private void hi() {
        System.out.println("欢迎光临");
    }

    private void bye() {
        System.out.println("bye~");
    }

    public static void main(String[] args) {
        StationStaticProxy stationStaticProxy = new StationStaticProxy(new Station());
        stationStaticProxy.inquire();
        stationStaticProxy.sellTicket();
        stationStaticProxy.withdraw();
    }
}
```

### 动态代理

```java
public class StationDynamicProxy implements InvocationHandler {

    private Object subject;

    public StationDynamicProxy(Object subject) {
        this.subject = subject;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("hi");
        Object invoke = method.invoke(subject, args);
        System.out.println("bye~");
        return invoke;
    }

    public static void main(String[] args) {
        Station station = new Station();
        TicketService stationProxy = (TicketService) Proxy.newProxyInstance(StationDynamicProxy.class.getClassLoader(), station.getClass().getInterfaces(), new StationDynamicProxy(station));
        stationProxy.inquire();
        stationProxy.sellTicket();
        stationProxy.withdraw();
    }
}
```

### Spring Boot 集成

统计方法执行时长
```java
@Slf4j
@AllArgsConstructor
public class TimeDynamicProxy implements InvocationHandler {

    private Object subject;

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        long start = System.currentTimeMillis();
        Object invoke = method.invoke(subject, args);
        long end = System.currentTimeMillis();
        log.info(subject.getClass().getSimpleName() + "." + method.getName() + "耗时:{}", end-start);
        return invoke;
    }
}

```

```java
@RestController
public class ProductController {

    private ProductService productService;

    @Autowired
    public ProductController(ProductService productService) {
        this.productService = (ProductService) Proxy.newProxyInstance(TimeDynamicProxy.class.getClassLoader(),
                new Class[]{ProductService.class}, new TimeDynamicProxy(productService));
    }

    @GetMapping("add")
    public String add() {
        productService.add();
        return "success";
    }
}
```