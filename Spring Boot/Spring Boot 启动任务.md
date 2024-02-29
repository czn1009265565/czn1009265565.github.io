# Spring Boot 启动任务

Spring Boot 实现启动任务主要有五种方式:

- ApplicationListener
- ApplicationRunner
- CommandLineRunner
- @PostConstruct
- @Scheduled

执行顺序 PostConstruct>ApplicationListener>ApplicationRunner>CommandLineRunner

## ApplicationListener

```java
@Component
public class Bootstrap1 implements ApplicationListener<ContextRefreshedEvent> {
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        System.out.println("start ApplicationListener");
    }
}
```


## ApplicationRunner

```java
@Component
public class Bootstrap1 implements ApplicationListener<ContextRefreshedEvent> {
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        System.out.println("start ApplicationListener");
    }
}
```

## CommandLineRunner

```java
@Component
public class Bootstrap3 implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("start CommandLineRunner");
    }
}
```

## PostConstruct

```java
@Component
public class Bootstrap4 {

    @PostConstruct
    public void start() {
        System.out.println("start PostConstruct");
    }
}
```

## Scheduler

```java
@Component
@EnableScheduling
public class Bootstrap5 {
    private static int atomic = 0;

    @Scheduled(initialDelay = 1000, fixedRate = 1000 * 3600)
    public void runScheduled() {
        if (atomic != 0) {
            return;
        }
        System.out.println("start scheduled");
        atomic ++;
    }
}
```