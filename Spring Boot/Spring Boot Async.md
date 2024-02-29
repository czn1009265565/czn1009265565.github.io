## Spring Boot Async

在执行一些耗时任务时，例如批量数据处理、发送邮件短信等情况时可以通过异步编程可以提高效率，提升接口的吞吐量。

### 开启异步支持

```java
@EnableAsync
@SpringBootApplication
public class SpringBootExamplesApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringBootExamplesApplication.class, args);
    }
}
```

新建异步方法

```java
@Slf4j
@Service
public class AsyncService {

    @Async
    public void asyncTest() {
        try {
            TimeUnit.SECONDS.sleep(2);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        log.info("异步方法内部线程名称：{}", Thread.currentThread().getName());
    }
}
```

新建测试Controller

```java
@Slf4j
@RestController
public class AsyncController {
    @Autowired
    private AsyncService asyncService;

    @GetMapping("/test")
    public String test() {
        long start = System.currentTimeMillis();
        log.info("异步方法开始");

        asyncService.asyncTest();

        log.info("异步方法结束");
        long end = System.currentTimeMillis();
        log.info("总耗时：{} ms", end - start);
        return "success";
    }
}
```

### 自定义异步线程池


```java
@Configuration
public class AsyncPoolConfig {

    @Bean
    public ThreadPoolTaskExecutor asyncThreadPoolTaskExecutor(){
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(20);
        executor.setMaxPoolSize(200);
        executor.setQueueCapacity(25);
        executor.setKeepAliveSeconds(200);
        executor.setThreadNamePrefix("asyncThread");
        // executor.setWaitForTasksToCompleteOnShutdown(true);
        // executor.setAwaitTerminationSeconds(60);

        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());

        executor.initialize();
        return executor;
    }
}
```

- corePoolSize：线程池核心线程的数量，默认值为1（这就是默认情况下的异步线程池配置使得线程不能被重用的原因）。

- maxPoolSize：线程池维护的线程的最大数量，只有当核心线程都被用完并且缓冲队列满后，才会开始申超过请核心线程数的线程，默认值为Integer.MAX_VALUE。

- queueCapacity：缓冲队列。

- keepAliveSeconds：超出核心线程数外的线程在空闲时候的最大存活时间，默认为60秒。

- threadNamePrefix：线程名前缀。

- waitForTasksToCompleteOnShutdown：是否等待所有线程执行完毕才关闭线程池，默认值为false。

- awaitTerminationSeconds：waitForTasksToCompleteOnShutdown的等待的时长，默认值为0，即不等待。

- rejectedExecutionHandler：当没有线程可以被使用时的处理策略（拒绝任务），默认策略为abortPolicy，包含下面四种策略：
	
	1. callerRunsPolicy：直接在 execute 方法的调用线程运行被拒绝的任务；如果执行程序已关闭，则会丢弃该任务。

	2. abortPolicy：直接抛出java.util.concurrent.RejectedExecutionException异常。

	3. discardOldestPolicy：当线程池中的数量等于最大线程数时、抛弃线程池中最后一个要执行的任务，并执行新传入的任务。

	4. discardPolicy：当线程池中的数量等于最大线程数时，不做任何动作。


使用线程池

```java
@Async("asyncThreadPoolTaskExecutor")
```

### 处理异步回调

```java
@Async("asyncThreadPoolTaskExecutor")
public Future<String> asyncMethod() {
    try {
        TimeUnit.SECONDS.sleep(2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    log.info("异步方法内部线程名称：{}", Thread.currentThread().getName());
    return new AsyncResult<>("hello async");
}
```

获取返回值

```java
Future<String> stringFuture = asyncService.asyncMethod();
// 阻塞
String result = stringFuture.get();
// 设置超时时间 需要自行捕获超时异常处理
String result = stringFuture.get(60, TimeUnit.SECONDS);
```