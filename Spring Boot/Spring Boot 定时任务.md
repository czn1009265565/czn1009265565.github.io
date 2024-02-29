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

# Quartz

## 体系结构

1. `Job` 表示一个工作，要执行的具体内容。
2. `JobDetail` 表示一个具体的可执行的调度程序，`Job` 是这个可执行程调度程序所要执行的内容，另外 `JobDetail` 还包含了这个任务调度的方案和策略。
3. `Trigger` 代表一个调度参数的配置，什么时候去调。
4. `Scheduler` 代表一个调度容器，一个调度容器中可以注册多个 `JobDetail` 和 `Trigger`。当 `Trigger` 与 `JobDetail` 组合，就可以被 `Scheduler` 容器调度了。

## 持久化

1. RAMJobStore

    在默认情况下Quartz将任务调度的运行信息保存在内存中，这种方法提供了最佳的性能，因为内存中数据访问最快。
    不足之处是缺乏数据的持久性，当程序路途停止或系统崩溃时，所有运行的信息都会丢失。

2. JobStoreTX

    所有的任务信息都会保存到数据库中，可以控制事物，还有就是如果应用服务器关闭或者重启，
    任务信息都不会丢失，并且可以恢复因服务器关闭或者重启而导致执行失败的任务。

## 单机模式

### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-quartz</artifactId>
</dependency>
```

### application配置

```yaml
spring:
  # Quartz 的配置，对应 QuartzProperties 配置类
  quartz:
    job-store-type: memory # Job 存储器类型。默认为 memory 表示内存，可选 jdbc 使用数据库。
    auto-startup: true # Quartz 是否自动启动
    startup-delay: 0 # 延迟 N 秒启动
    wait-for-jobs-to-complete-on-shutdown: true # 应用关闭时，是否等待定时任务执行完成。默认为 false ，建议设置为 true
    overwrite-existing-jobs: false # 是否覆盖已有 Job 的配置
    properties: # 添加 Quartz Scheduler 附加属性，更多可以看 http://www.quartz-scheduler.org/documentation/2.4.0-SNAPSHOT/configuration.html 文档
      org:
        quartz:
          threadPool:
            threadCount: 25 # 线程池大小。默认为 10 。
            threadPriority: 5 # 线程优先级
            class: org.quartz.simpl.SimpleThreadPool # 线程池类型
#    jdbc: # 这里暂时不说明，使用 JDBC 的 JobStore 的时候，才需要配置
```

### Job实例
继承 `QuartzJobBean` 抽象类，实现 `executeInternal(JobExecutionContext context)` 方法，执行自定义的定时任务的逻辑。

```java
@Slf4j
public class DemoJob extends QuartzJobBean {
    
    @Resource
    private DemoService demoService;

    @Override
    protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
        demoService.test();
        log.info("Quartz Job single");
    }
}
```

`QuartzJobBean` 实现了 `org.quartz.Job` 接口，提供了 `Quartz` 每次创建 `Job` 执行定时逻辑时，将该 `Job Bean` 的依赖属性注入，对应上文的 `DemoService` 

### ScheduleConfiguration

```java
@Configuration
public class ScheduleConfiguration {

    public static class DemoJobConfiguration {

        @Bean
        public JobDetail demoJob() {
            return JobBuilder.newJob(DemoJob.class)
                    .withIdentity("demoJob") // 名字为 demoJob
                    .storeDurably() // 没有 Trigger 关联的时候任务是否被保留。因为创建 JobDetail 时，还没 Trigger 指向它，所以需要设置为 true ，表示保留。
                    .build();
        }

        @Bean
        public Trigger demoJobTrigger() {
            // 简单的调度计划的构造器
            SimpleScheduleBuilder scheduleBuilder = SimpleScheduleBuilder.simpleSchedule()
                    .withIntervalInSeconds(5) // 频率。
                    .repeatForever(); // 次数。
            // Trigger 构造器
            return TriggerBuilder.newTrigger()
                    .forJob(demoJob()) // 对应 Job 为 demoJob
                    .withIdentity("demoJobTrigger") // 名字为 demoJobTrigger
                    .withSchedule(scheduleBuilder) // 对应 Schedule 为 scheduleBuilder
                    .build();
        }
    }
}
```

## 集群模式

### 引入依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-quartz</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>

    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>8.0.28</version>
    </dependency>
</dependencies>
```

### application配置

```yaml
spring:
  datasource:
    user:
      url: jdbc:mysql://127.0.0.1:3306/bussiness?useSSL=false&useUnicode=true&characterEncoding=UTF-8
      driver-class-name: com.mysql.jdbc.Driver
      username: root
      password: Admin123.
    quartz:
      url: jdbc:mysql://127.0.0.1:3306/quartz?useSSL=false&useUnicode=true&characterEncoding=UTF-8
      driver-class-name: com.mysql.jdbc.Driver
      username: root
      password: Admin123.

  # Quartz 的配置，对应 QuartzProperties 配置类
  quartz:
    scheduler-name: clusteredScheduler # Scheduler 名字。默认为 schedulerName
    job-store-type: jdbc # Job 存储器类型。默认为 memory 表示内存，可选 jdbc 使用数据库。
    auto-startup: true # Quartz 是否自动启动
    startup-delay: 0 # 延迟 N 秒启动
    wait-for-jobs-to-complete-on-shutdown: true # 应用关闭时，是否等待定时任务执行完成。默认为 false ，建议设置为 true
    overwrite-existing-jobs: false # 是否覆盖已有 Job 的配置
    properties: # 添加 Quartz Scheduler 附加属性，更多可以看 http://www.quartz-scheduler.org/documentation/2.4.0-SNAPSHOT/configuration.html 文档
      org:
        quartz:
          # JobStore 相关配置
          jobStore:
            # 数据源名称
            dataSource: quartzDataSource # 使用的数据源
            class: org.quartz.impl.jdbcjobstore.JobStoreTX # JobStore 实现类
            driverDelegateClass: org.quartz.impl.jdbcjobstore.StdJDBCDelegate
            tablePrefix: QRTZ_ # Quartz 表前缀
            isClustered: true # 是集群模式
            clusterCheckinInterval: 1000
            useProperties: false
          # 线程池相关配置
          threadPool:
            threadCount: 25 # 线程池大小。默认为 10 。
            threadPriority: 5 # 线程优先级
            class: org.quartz.simpl.SimpleThreadPool # 线程池类型
    jdbc: # 使用 JDBC 的 JobStore 的时候，JDBC 的配置
      initialize-schema: never # 是否自动使用 SQL 初始化 Quartz 表结构。这里设置成 never ，我们手动创建表结构。
```

### 初始化Quartz表结构
在 [Quartz Download](http://www.quartz-scheduler.org/downloads/) 地址，下载对应版本的发布包。
解压后，我们可以在 `src/org/quartz/impl/jdbcjobstore/` 目录，看到各种数据库的 `Quartz` 表结构的初始化脚本。
这里，因为我们使用 MySQL ，所以使用 `tables_mysql_innodb.sql` 脚本。

### Job实例
相较单机模式多了 `@DisallowConcurrentExecution` 注解，保证相同 JobDetail 在多个 JVM 进程中，有且仅有一个节点在执行。
```java
@Slf4j
@DisallowConcurrentExecution
public class ClusterJob extends QuartzJobBean {

    @Resource
    private DemoService demoService;

    @Override
    protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
        demoService.test();
        log.info("Quartz Job cluster");
    }
}
```

### 初始化任务启动

```java
@Component
public class ClusterJobInit implements ApplicationListener<ContextRefreshedEvent> {

    @Resource
    private Scheduler scheduler;

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        // 创建 JobDetail
        JobDetail jobDetail = JobBuilder.newJob(ClusterJob.class)
                .withIdentity("clusterJob") // 名字为 clusterJob
                .storeDurably() // 没有 Trigger 关联的时候任务是否被保留。因为创建 JobDetail 时，还没 Trigger 指向它，所以需要设置为 true ，表示保留。
                .build();
        // 创建 Trigger
        SimpleScheduleBuilder scheduleBuilder = SimpleScheduleBuilder.simpleSchedule()
                .withIntervalInSeconds(5) // 频率。
                .repeatForever(); // 次数。
        Trigger trigger = TriggerBuilder.newTrigger()
                .forJob(jobDetail) // 对应 Job 为 ClusterJob
                .withIdentity("clusterJobTrigger") // 名字为 clusterJobTrigger
                .withSchedule(scheduleBuilder) // 对应 Schedule 为 scheduleBuilder
                .build();
        // 添加调度任务
        try {
            scheduler.scheduleJob(jobDetail, trigger);
        } catch (SchedulerException e) {
            throw new RuntimeException(e);
        }
    }
}
```

### SchedulerManager

```java
/**
 * {@link org.quartz.Scheduler} 的管理器，负责创建任务
 *
 * 考虑到实现的简洁性，我们使用 jobName 作为唯一标识，即：
 * 1. Job 的 {@link JobDetail#getKey()}
 * 2. Trigger 的 {@link Trigger#getKey()}
 *
 * 另外，jobName 对应到 Class.getSimpleName() 直接调用
 */
@Service
public class SchedulerManager {

    @Resource
    private Scheduler scheduler;

    /**
     * 添加 Job 到 Quartz 中
     *
     * @param jobId 任务编号
     * @param jobClass 任务名字
     * @param jobParam 任务参数
     * @param cronExpression CRON 表达式
     * @throws SchedulerException 添加异常
     */
    public void addJob(Long jobId, Class<? extends Job> jobClass, String jobParam, String cronExpression)
            throws SchedulerException {
        String jobName = jobClass.getSimpleName();
        // 创建 JobDetail 对象
        JobDetail jobDetail = JobBuilder.newJob(jobClass)
                .usingJobData(JobDataKeyEnum.JOB_ID.name(), jobId)
                .usingJobData(JobDataKeyEnum.JOB_HANDLER_NAME.name(), jobParam)
                .withIdentity(jobName).build();
        // 创建 Trigger 对象
        Trigger trigger = this.buildTrigger(jobName, jobParam, cronExpression);
        // 新增调度
        scheduler.scheduleJob(jobDetail, trigger);
    }

    /**
     * 更新 Job 到 Quartz
     *
     * @param jobName 任务处理器的名字
     * @param jobParam 任务处理器的参数
     * @param cronExpression CRON 表达式
     * @throws SchedulerException 更新异常
     */
    public void updateJob(String jobName, String jobParam, String cronExpression)
            throws SchedulerException {
        // 创建新 Trigger 对象
        Trigger newTrigger = this.buildTrigger(jobName, jobParam, cronExpression);
        // 修改调度
        scheduler.rescheduleJob(new TriggerKey(jobName), newTrigger);
    }

    /**
     * 删除 Quartz 中的 Job
     *
     * @param jobName 任务处理器的名字
     * @throws SchedulerException 删除异常
     */
    public void deleteJob(String jobName) throws SchedulerException {
        scheduler.deleteJob(new JobKey(jobName));
    }

    /**
     * 暂停 Quartz 中的 Job
     *
     * @param jobName 任务处理器的名字
     * @throws SchedulerException 暂停异常
     */
    public void pauseJob(String jobName) throws SchedulerException {
        scheduler.pauseJob(new JobKey(jobName));
    }

    /**
     * 启动 Quartz 中的 Job
     *
     * @param jobName 任务处理器的名字
     * @throws SchedulerException 启动异常
     */
    public void resumeJob(String jobName) throws SchedulerException {
        scheduler.resumeJob(new JobKey(jobName));
        scheduler.resumeTrigger(new TriggerKey(jobName));
    }

    /**
     * 立即触发一次 Quartz 中的 Job
     *
     * @param jobId 任务编号
     * @param jobName 任务处理器的名字
     * @param jobParam 任务处理器的参数
     * @throws SchedulerException 触发异常
     */
    public void triggerJob(Long jobId, String jobName, String jobParam)
            throws SchedulerException {
        JobDataMap data = new JobDataMap();
        data.put(JobDataKeyEnum.JOB_ID.name(), jobId);
        data.put(JobDataKeyEnum.JOB_HANDLER_NAME.name(), jobName);
        data.put(JobDataKeyEnum.JOB_HANDLER_PARAM.name(), jobParam);
        // 触发任务
        scheduler.triggerJob(new JobKey(jobName), data);
    }

    private Trigger buildTrigger(String jobName, String jobParam, String cronExpression) {
        return TriggerBuilder.newTrigger()
                .withIdentity(jobName)
                .withSchedule(CronScheduleBuilder.cronSchedule(cronExpression))
                .usingJobData(JobDataKeyEnum.JOB_HANDLER_PARAM.name(), jobParam)
                .build();
    }
}
```

枚举类

```java
public enum JobDataKeyEnum {
    JOB_ID,
    JOB_HANDLER_NAME,
    JOB_HANDLER_PARAM,
}
```

### Job表结构参考

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobDO {
    private Long id;
    /** 任务名称 */
    private String name;
    /** 任务状态 0-初始化 1-开启 2-暂停 */
    private Integer status;
    /** 任务参数 */
    private String jobParam;
    /** CRON 表达式 */
    private String cronExpression;
    /** 最近一次任务开始时间 */
    private LocalDateTime startTime;
    /** 最近一次任务结束时间 */
    private LocalDateTime endTime;
}
```

