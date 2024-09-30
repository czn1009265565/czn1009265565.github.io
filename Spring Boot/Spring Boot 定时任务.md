# Spring Task

`@Scheduled`注解是Spring Boot提供的用于定时任务控制的注解，主要用于控制任务在某个指定时间执行，或者每隔一段时间执行。

## 常用属性

- `cron`
- `fixedRate`
- `fixedDelay`
- `initialDelay`

### Cron 表达式
`cron`是`@Scheduled`的一个参数，是一个字符串，以5个空格隔开，只允许6个域（注意不是7个，7个直接会报错），分别表示秒、分、时、日、月、周。

| 域  | 是否必须 | 取值范围                                            | 特殊字符          |
|----|------|-------------------------------------------------|---------------|
| 秒  | 是    | [0, 59]                                         | * , - /       |
| 分钟 | 是    | [0, 59]                                         | * , - /       |
| 小时 | 是    | [0, 23]                                         | * , - /       |
| 日期 | 是    | [1, 31]                                         | * , - / ? L W |
| 月份 | 是    | [1, 12]或[JAN, DEC]                              | * , - /       |
| 星期 | 是    | [1, 7]或[MON, SUN]。若您使用[1, 7]表达方式，1代表星期一，7代表星期日。 | * , - / ? L # |
| 年  | 否    | [当前年份，2099]                                     | * , - /       |

### fixedRate

fixedRate表示自上一次执行时间之后多长时间执行，以毫秒为单位。

```java
// fixedRate 即使上一次调用还在运行，也使Spring运行任务
@Scheduled(fixedRate=1000 * 2)
```

### fixedDelay
fixedDelay与fixedRate有点类似，不过fixedRate是上一次开始之后计时，fixedDelay是上一次结束之后计时，也就是说，fixedDelay表示上一次执行完毕之后多长时间执行，单位也是毫秒。

```java
// fixedDelay 距离上一次任务执行完成间隔时间
@Scheduled(fixedDelay=1000 * 2)
```

### initialDelay

initialDelay表示首次延迟多长时间后执行，单位毫秒，之后按照fixedRate/fixedDelay指定的规则执行，需要指定其中一个规则。

```java
//首次运行延迟1s
@Scheduled(initialDelay=1000,fixedRate=1000)
```

## ScheduleConfiguration

```java
@Configuration
@EnableScheduling
public class ScheduleConfiguration {
}
```

## @Scheduled

```java
@Slf4j
@Component
public class JobScheduler {

    @Scheduled(cron="${scheduler.cron:0 0 0 * * ?}")
    public void cronJob() {
        log.info("cron job");
    }

    @Scheduled(fixedRate = 3000)
    public void fixedRateJob() {
        log.info("fixedRate job");
    }

    @Scheduled(fixedDelay = 3000)
    public void fixedDelayJob() {
        log.info("fixedDelay job");
    }
}
```
