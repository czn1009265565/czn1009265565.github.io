# Java 线程池

## 背景
线程池能够对线程进行统一分配，调优和监控:

- 降低资源消耗(线程无限制地创建，然后使用完毕后销毁)
- 提高响应速度(无须创建线程)
- 提高线程的可管理性

## ThreadPoolExecutor
- corePoolSize: 核心线程数线程数定义了最小可以同时运行的线程数量
- maximumPoolSize: 当队列中存放的任务达到队列容量的时候，当前可以同时运行的线程数量变为最大线程数。
- workQueue: 当新任务来的时候会先判断当前运行的线程数量是否达到核心线程数，如果达到的话，新任务就会被存放在队列中。
- keepAliveTime: 保持存活时间
- unit: keepAliveTime的单位时间
- handler: 拒绝策略

## 任务运行机制
1. 首先检测线程池运行状态，如果不是RUNNING，则直接拒绝，线程池要保证在RUNNING的状态下执行任务。
2. 如果workerCount < corePoolSize，则创建并启动一个线程来执行新提交的任务。
3. 如果workerCount >= corePoolSize，且线程池内的阻塞队列未满，则将任务添加到该阻塞队列中。
4. 如果workerCount >= corePoolSize && workerCount < maximumPoolSize，且线程池内的阻塞队列已满，则创建并启动一个线程来执行新提交的任务。
5. 如果workerCount >= maximumPoolSize，并且线程池内的阻塞队列已满, 则根据拒绝策略来处理该任务, 默认的处理方式是直接抛异常。

## 线程池大小确定
- CPU 密集型任务(N+1): 这种任务消耗的主要是 CPU 资源，可以将线程数设置为 `N（CPU 核心数）+1`，
  比 CPU 核心数多出来的一个线程是为了防止线程偶发的缺页中断，或者其它原因导致的任务暂停而带来的影响。
  一旦任务暂停，CPU 就会处于空闲状态，而在这种情况下多出来的一个线程就可以充分利用 CPU 的空闲时间。
- I/O 密集型任务(2N): 这种任务应用起来，系统会用大部分的时间来处理 I/O 交互，
  而线程在处理 I/O 的时间段内不会占用 CPU 来处理，这时就可以将 CPU 交出给其它线程使用。
  因此在 I/O 密集型任务的应用中，我们可以多配置一些线程，具体的计算方法是 `2N`。

## 创建线程池

```java
public final class ThreadPoolManager {

    private static ThreadPoolManager sThreadPoolManager = new ThreadPoolManager();

    // 线程池维护线程的最少数量
    private static final int SIZE_CORE_POOL = 3;

    // 线程池维护线程的最大数量
    private static final int SIZE_MAX_POOL = 4;

    // 线程池维护线程所允许的空闲时间
    private static final int TIME_KEEP_ALIVE = 5000;

    // 线程池所使用的缓冲队列大小
    private static final int SIZE_WORK_QUEUE = 500;

    // 任务调度周期
    private static final int PERIOD_TASK_QOS = 1000;

    /*
     * 线程池单例创建方法
     */
    public static ThreadPoolManager newInstance() {
        return sThreadPoolManager;
    }

    // 任务缓冲队列
    private final Queue<Runnable> mTaskQueue = new LinkedList<Runnable>();

    /*
     * 线程池超出界线时将任务加入缓冲队列
     */
    private final RejectedExecutionHandler mHandler = new RejectedExecutionHandler() {
        @Override
        public void rejectedExecution(Runnable task, ThreadPoolExecutor executor) {
            mTaskQueue.offer(task);
        }
    };

    /*
     * 将缓冲队列中的任务重新加载到线程池
     */
    private final Runnable mAccessBufferThread = new Runnable() {
        @Override
        public void run() {
            if (hasMoreAcquire()) {
                mThreadPool.execute(mTaskQueue.poll());
            }
        }
    };

    /*
     * 创建一个调度线程池
     */
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

    /*
     * 通过调度线程周期性的执行缓冲队列中任务
     */
    protected final ScheduledFuture<?> mTaskHandler = scheduler.scheduleAtFixedRate(mAccessBufferThread, 0,
            PERIOD_TASK_QOS, TimeUnit.MILLISECONDS);

    /*
     * 线程池
     */
    private final ThreadPoolExecutor mThreadPool = new ThreadPoolExecutor(SIZE_CORE_POOL, SIZE_MAX_POOL,
            TIME_KEEP_ALIVE, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(SIZE_WORK_QUEUE), mHandler);

    /*
     * 将构造方法访问修饰符设为私有，禁止任意实例化。
     */
    private ThreadPoolManager() {
    }

    public void perpare() {
        if (mThreadPool.isShutdown() && !mThreadPool.prestartCoreThread()) {
            @SuppressWarnings("unused")
            int startThread = mThreadPool.prestartAllCoreThreads();
        }
    }

    /*
     * 消息队列检查方法
     */
    private boolean hasMoreAcquire() {
        return !mTaskQueue.isEmpty();
    }

    /*
     * 向线程池中添加任务方法
     */
    public void addExecuteTask(Runnable task) {
        if (task == null) throw new NullPointerException();
        mThreadPool.execute(task);
    }

    public <V> Future<V> submit(Callable<V> callable) {
        if (callable == null) throw new NullPointerException();
        return mThreadPool.submit(callable);
    }

    protected boolean isTaskEnd() {
        return mThreadPool.getActiveCount() == 0;
    }

    public void shutdown() {
        mTaskQueue.clear();
        mThreadPool.shutdown();
    }
}
```
