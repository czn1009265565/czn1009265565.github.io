# Spring Boot Quartz

## 体系结构
1. `JobDetail & Job` 具体任务，Job用来定义任务执行的具体逻辑，JobDetail定义JobKey唯一键以及任务描述
2. `Trigger` 触发器，定义job执行的方式以及周期
3. `Scheduler` 核心任务调度器

## 持久化

1. RAMJobStore  
   在默认情况下Quartz将任务调度的运行信息保存在内存中，这种方法提供了最佳的性能，因为内存中数据访问最快。
   不足之处是缺乏数据的持久性，当程序路途停止或系统崩溃时，所有运行的信息都会丢失。

2. JobStoreTX  
   所有的任务信息都会保存到数据库中，可以控制事物，还有就是如果应用服务器关闭或者重启，
   任务信息都不会丢失，并且可以恢复因服务器关闭或者重启而导致执行失败的任务。

## Cron 表达式
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


## Spring Boot 集成

### 引入依赖

```xml
<dependencys>
   <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-jdbc</artifactId>
   </dependency>
   
   <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-quartz</artifactId>
   </dependency>
</dependencys>

```

### application配置

#### 单体配置

```yaml
spring:
   # Quartz 的配置，对应 QuartzProperties 配置类
   quartz:
      # Job 存储器类型。默认为 memory 表示内存，可选 jdbc 使用数据库
      job-store-type: memory
      # Quartz 是否自动启动
      auto-startup: true
      # 延迟 N 秒启动
      startup-delay: 0
      # 应用关闭时，是否等待定时任务执行完成。默认为 false ，建议设置为 true
      wait-for-jobs-to-complete-on-shutdown: true
      # 是否覆盖已有 Job 的配置
      overwrite-existing-jobs: false
      # 添加 Quartz Scheduler 附加属性
      properties:
         org:
            quartz:
               threadPool:
                  # 线程池大小,默认为 10
                  threadCount: 25
                  # 线程优先级
                  threadPriority: 5
                  # 线程池类型
                  class: org.quartz.simpl.SimpleThreadPool
```

#### JDBC集群配置

```yaml
spring:
   datasource:
      url: jdbc:postgresql://127.0.0.1:5432/dbname
      driver-class-name: org.postgresql.Driver
      username: postgres
      password: postgres

   quartz:
      # Scheduler 名字。默认为 schedulerName
      scheduler-name: clusteredScheduler
      # Job 存储器类型。默认为 memory 表示内存，可选 jdbc 使用数据库
      job-store-type: jdbc
      # Quartz 是否自动启动
      auto-startup: true
      # 延迟 N 秒启动
      startup-delay: 0
      # 应用关闭时，是否等待定时任务执行完成。默认为 false ，建议设置为 true
      wait-for-jobs-to-complete-on-shutdown: true
      overwrite-existing-jobs: false # 是否覆盖已有 Job 的配置
      # 添加 Quartz Scheduler 附加属性
      properties:
         org:
            quartz:
               # JobStore 相关配置
               jobStore:
                  # 使用默认数据源
                  class: org.springframework.scheduling.quartz.LocalDataSourceJobStore
                  # 数据库方言  MySQL org.quartz.impl.jdbcjobstore.StdJDBCDelegate
                  driverDelegateClass: org.quartz.impl.jdbcjobstore.PostgreSQLDelegate
                  # Quartz 表前缀
                  tablePrefix: qrtz_
                  # 集群模式
                  isClustered: true
                  clusterCheckinInterval: 1000
                  useProperties: false
               # 线程池相关配置
               threadPool:
                  # 线程池大小,默认为10
                  threadCount: 25
                  # 线程优先级
                  threadPriority: 5
                  # 线程池类型
                  class: org.quartz.simpl.SimpleThreadPool
      # 使用 JDBC 的 JobStore 的时候，JDBC 的配置
      jdbc:
         # 是否初始化 Quartz 表结构
         # - always 服务重启删表重建
         # - never 不做操作
         initialize-schema: always
```

### 自定义Job实例

```java
@Slf4j
@Component
public class MyJob extends QuartzJobBean {

   @Override
   protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
      JobDetail jobDetail = context.getJobDetail();
      JobDataMap jobDataMap = jobDetail.getJobDataMap();
      // 获取任务相关信息
      Long jobId = jobDataMap.getLong(JobDataKeyEnum.JOB_ID.name());
      String jobName = jobDataMap.getString(JobDataKeyEnum.JOB_HANDLER_NAME.name());
      String jobParam = jobDataMap.getString(JobDataKeyEnum.JOB_HANDLER_PARAM.name());
      log.info("Job start! jobName:{}", jobName);
   }
}
```

### 调度器

```java
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
   public void addJob(Long jobId, String jobName, Class<? extends Job> jobClass, String jobParam, String cronExpression)
           throws SchedulerException {
      // 创建 JobDetail 对象
      JobDetail jobDetail = JobBuilder.newJob(jobClass)
              .usingJobData(JobDataKeyEnum.JOB_ID.name(), jobId)
              .usingJobData(JobDataKeyEnum.JOB_HANDLER_NAME.name(), jobName)
              .usingJobData(JobDataKeyEnum.JOB_HANDLER_PARAM.name(), jobParam)
              .withIdentity(jobName)
              .build();
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


#### 枚举类
```java
public enum JobDataKeyEnum {
    JOB_ID,
    JOB_HANDLER_NAME,
    JOB_HANDLER_PARAM,
}
```

#### 实体类
这里仅是一个示例，根据需求适当调整表结构字段

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@TableName(value = "biz_job", autoResultMap = true)
public class JobDO {
   @TableId
   private Long id;
   /** 任务名称 */
   private String name;
   /** 任务状态 详情查看 0-准备中 1-执行中 2-成功 3-失败 4-手动停止 */
   private Integer status;
   /** 任务参数 */
   private String jobParam;
   /** CRON 表达式 */
   private String cronExpression;
   /** 任务类别 */
   private Integer type;
   /** 最近一次任务开始时间 */
   private LocalDateTime startTime;
   /** 最近一次任务结束时间 */
   private LocalDateTime endTime;

   private LocalDateTime createTime;
   private LocalDateTime updateTime;
}
```

### 初始化启动任务

```java
@Component
public class ClusterJobInit implements ApplicationListener<ContextRefreshedEvent> {

   @Resource
   private SchedulerManager schedulerManager;

   @Override
   public void onApplicationEvent(ContextRefreshedEvent event) {
      // 初始化调度任务
      try {
         long jobId = IdUtil.getSnowflakeNextId();
         schedulerManager.addJob(jobId, "myJob", MyJob.class, "", "*/5 * * * * ?");
      } catch (SchedulerException e) {
         throw new RuntimeException(e);
      }
   }
}
```

