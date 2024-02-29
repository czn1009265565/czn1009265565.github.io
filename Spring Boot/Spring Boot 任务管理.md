# Spring Boot 任务管理

本文主要介绍项目开发过程中耗时任务的管理，例如Excel导入等，非定时任务。

## 单体服务

通过线程池和内存实现任务执行、关闭、进度查询、结果获取

### 任务线程池

```java
public final class JobPoolManager {

    private static JobPoolManager sJobPoolManager = new JobPoolManager();

    // 线程池维护线程的最少数量
    private static final int SIZE_CORE_POOL = 0;

    // 线程池维护线程的最大数量
    private static final int SIZE_MAX_POOL = 4;

    // 线程池维护线程所允许的空闲时间
    private static final int TIME_KEEP_ALIVE = 5000;

    // 线程池所使用的缓冲队列大小
    private static final int SIZE_WORK_QUEUE = 500;

    /*
     * 线程池单例创建方法
     */
    public static JobPoolManager newInstance() {
        return sJobPoolManager;
    }

    /*
     * 线程池
     */
    private final ThreadPoolExecutor mThreadPool = new ThreadPoolExecutor(SIZE_CORE_POOL, SIZE_MAX_POOL,
            TIME_KEEP_ALIVE, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(SIZE_WORK_QUEUE));

    /*
     * 将构造方法访问修饰符设为私有，禁止任意实例化。
     */
    private JobPoolManager() {
    }

    /*
     * 执行Runnable任务
     */
    public void execute(Runnable task) {
        if (task == null) throw new NullPointerException();
        mThreadPool.execute(task);
    }

    private final ConcurrentMap<String, JobCallable> callableRepository = new ConcurrentHashMap<>();

    /**
     * 执行callable任务
     */
    public <V> void submit(JobCallable<V> jobCallable) {
        if (jobCallable == null) throw new NullPointerException();
        jobCallable.setFuture(mThreadPool.submit(jobCallable));
        callableRepository.put(jobCallable.getJobId(), jobCallable);
    }

    /**
     * 获取任务执行结果
     */
    public Object getResult(String jobId)  {
        if (jobId == null || jobId.equals("")) throw new NullPointerException();
        JobCallable jobCallable = callableRepository.get(jobId);
        if (jobCallable == null || jobCallable.getFuture() == null) {
            return null;
        }
        Object result = null;
        try {
            result = jobCallable.getFuture().get();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    /**
     * 取消任务
     * 只支持终止线程的阻塞状态(wait、join、sleep)
     * 因此需要任务中结合Thread.isInterrupted()判断
     */
    public void cancel(String jobId) {
        if (jobId == null || jobId.equals("")) throw new NullPointerException();
        JobCallable jobCallable = callableRepository.get(jobId);
        if (jobCallable == null || jobCallable.getFuture() == null) {
            return;
        }
        jobCallable.getFuture().cancel(true);
        callableRepository.remove(jobCallable.getJobId());
    }

    /**
     * 获取任务执行进度
     * @param jobId 任务ID
     * @return 任务进度
     */
    public BigDecimal getProgress(String jobId) {
        if (jobId == null || jobId.equals("")) throw new NullPointerException();
        JobCallable jobCallable = callableRepository.get(jobId);
        if (jobCallable == null) {
            return BigDecimal.ONE;
        }
        Future future = jobCallable.getFuture();
        if (future == null || future.isDone()) {
            return BigDecimal.ONE;
        }
        return jobCallable.getProgress();
    }

    public void shutdown() {
        mThreadPool.shutdown();
    }
}
```

### 任务抽象类

```java
@Data
public abstract class JobCallable<V> implements Callable<V> {

    public JobCallable() {
        jobId = String.valueOf(System.currentTimeMillis());
        progress = BigDecimal.ZERO;
        startTime = System.currentTimeMillis();
    }

    public JobCallable(String jobId) {
        this.jobId = jobId;
        progress = BigDecimal.ZERO;
        startTime = System.currentTimeMillis();
    }

    /** 任务ID */
    private String jobId;
    /** 任务进度 */
    private BigDecimal progress;
    /** 任务启动时间 */
    private Long startTime;
    /** 任务执行结果 */
    private Future<V> future;
}
```

### 任务示例

```java
public class SampleJobCallable extends JobCallable<SampleJobResult>{

    public SampleJobCallable() {
    }

    @Override
    public SampleJobResult call() throws Exception {
        int total = 100;
        int progressed = 0;
        while (progressed < total) {
            // 任务终止判断
            if (Thread.interrupted()) {
                return new SampleJobResult();
            }
            // 更新进度
            setProgress(BigDecimal.valueOf(progressed).divide(BigDecimal.valueOf(total), 2, RoundingMode.HALF_UP));
            // 模拟IO阻塞
            Thread.sleep(1000);
            progressed ++;
        }

        return new SampleJobResult();
    }
}

class SampleJobResult {
}
```

### 主线程

```java
public class Main {
    public static void main(String[] args) throws InterruptedException {
        JobPoolManager jobPoolManager = JobPoolManager.newInstance();
        // 提交任务
        SampleJobCallable jobCallable = new SampleJobCallable();
        jobPoolManager.submit(jobCallable);
        Thread.sleep(3000);
        String jobId = jobCallable.getJobId();
        // 获取任务进度
        System.out.println(jobPoolManager.getProgress(jobId));
        // 取消任务
        jobPoolManager.cancel(jobId);
        // 获取任务进度
        System.out.println(jobPoolManager.getProgress(jobId));
        // 关闭线程池
        jobPoolManager.shutdown();
    }
}
```

### 思考

ConcurrentHashMap内存随着任务增加存在内存溢出风险，因此需要一个线程定期删除过期任务数据


```java
@Slf4j
public final class JobPoolManager {
    public static final int CACHE_DURATION = 3600 * 1000;

    /*
     * 创建一个调度线程池
     */
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);


    private Runnable memoryClear() {
        return () -> {
            log.info("Clean expired tasks!");
            for (String key : callableRepository.keySet()) {
                JobCallable jobCallable = callableRepository.get(key);
                if (System.currentTimeMillis() - jobCallable.getStartTime() > CACHE_DURATION) {
                    callableRepository.remove(key);
                }
            }
        };
    }

    /*
     * 通过调度线程周期性的删除过期任务
     */
    protected final ScheduledFuture<?> mTaskHandler = scheduler.scheduleAtFixedRate(memoryClear(), 0,
            CACHE_DURATION, TimeUnit.MILLISECONDS);
}    
```
