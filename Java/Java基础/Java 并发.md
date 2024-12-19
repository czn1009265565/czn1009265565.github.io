# Java 并发

## 为什么需要多线程
- 提高运行效率:  
  在单核处理器的环境下，多线程程序可以在一个线程等待时，如等待输入/输出操作时，自动切换到其他线程执行，这样就提高了CPU的利用率。

- 提高资源利用率:  
  在多核处理器的环境下，多线程程序可以同时在多个核上运行，每个线程运行在一个独立的核上，这样就可以同时利用多个处理器核心。

- 改善程序的响应性:  
  对于图形界面的应用程序，多线程可以使得在处理耗时的任务时，界面仍然保持响应用户的操作。

- 提高程序的扩展性:  
  多线程可以使得程序模块化，各个线程可以独立运行，相互之间影响较小，便于程序的扩展和维护。

尽管多线程带来了很多好处，但也需要注意一些问题，例如线程安全性、死锁、上下文切换消耗等。

## 线程安全

```java
public class Bank implements Runnable{
    private int count = 0;
    public static void main(String[] args) throws InterruptedException {
        Bank bank = new Bank();
        ArrayList<Thread> list = new ArrayList<>();
        for (int i =0;i<10;i++){
            Thread t = new Thread(bank);
            t.start();
            list.add(t);
        }
        for(Thread i:list)i.join();
        System.out.println(bank.getCount());
    }

    public int getCount(){
        return this.count;
    }

    @Override
    public void run() {
        for (int i=0;i<100;i++){
            try {
                this.count += 1;
                Thread.sleep(10);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```
上述代码正确输出结果应该为1000,但实际情况却不是这样，答案往往小于1000。
真正的问题在于run方法的执行过程中可能会被中断。如果能够确保线程失去控制之前方法运行完成，则数据累加和永远不会讹误。

## 线程使用
有三种使用线程的方法:

- 实现 Runnable 接口
- 实现 Callable 接口
- 继承 Thread 类

相较而言更推荐实现接口的方式，因为 `Java` 不支持多重继承，因此继承了 `Thread` 类就无法继承其它类，但是可以实现多个接口。
其次类可能只要求可执行，继承整个 `Thread` 类开销过大。

### 实现Runnable接口
需要实现 `run()` 方法

```java
public class MyRunnable implements Runnable{
    @Override
    public void run() {
        // 具体实现
        System.out.printf("ThreadName:%s", Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        MyRunnable myRunnable = new MyRunnable();
        Thread thread = new Thread(myRunnable);
        thread.start();
    }
}
```

### 实现Callable
与 `Runnable` 相比，`Callable` 可以有返回值，返回值通过 `FutureTask` 进行封装。

```java
public class MyCallable implements Callable<Long> {
    @Override
    public Long call() throws Exception {
        long num = 0;
        for (int i = 1; i < 101; i++) {
            num += i;
        }
        return num;
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        MyCallable mc = new MyCallable();
        FutureTask<Long> ft = new FutureTask<>(mc);
        Thread thread = new Thread(ft);
        thread.start();
        System.out.println(ft.get());
    }
}
```

### 继承Thread
同样也是需要实现 `run()` 方法，因为 `Thread` 类也实现了 `Runnable` 接口。

```java
public class MyThread extends Thread{

    public void run() {
        System.out.printf("ThreadName:%s", Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        MyThread myThread = new MyThread();
        myThread.start();
    }
}
```

## 线程中断
在Java中，线程的中断并不是直接停止线程，而是给线程发送一个信号，告知线程应该中断当前的操作。
线程可以在适当的时候检查这个信号并相应地中断自己的操作。

线程中断的核心方法  
- interrupt(): 用于中断目标线程，将目标线程的中断标志位置为true。`Thread.currentThread().interrupt()` 或 `myThread.interrupt()`
- interrupted(): 返回调用线程的中断状态，并清除中断标志（静态方法）。`Thread.interrupted()`
- isInterrupted(): 返回调用线程的中断状态，不会清除中断标志。`Thread.currentThread().isInterrupted()` 或 `myThread.isInterrupted()`

### interrupt
通过调用一个线程的 `interrupt()` 来中断该线程，如果该线程处于阻塞、限期等待或者无限期等待状态，
那么就会抛出 `InterruptedException`，从而提前结束该线程。但是不能中断 `I/O` 阻塞和 `synchronized` 锁阻塞。

```java
public class ThreadInterrupted implements Runnable {

    @Override
    public void run() {
        try {
            while (true) {
                Thread.sleep(2000);
                System.out.printf("ThreadName:%s date:%s \n", Thread.currentThread().getName(), new Date());
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(new ThreadInterrupted());
        thread.start();

        Thread.sleep(5000);
        // 中断线程
        thread.interrupt();
        System.out.printf("ThreadName:%s ending! \n", Thread.currentThread().getName());
    }
}
```

### interrupted
如果一个线程的 `run()` 方法执行一个无限循环，并且没有执行 `sleep()` 等会抛出 `InterruptedException` 的操作，
那么调用线程的 `interrupt()` 方法就无法使线程提前结束。

但是调用 `interrupt()` 方法会设置线程的中断标记，此时调用 `interrupted()` 方法会返回 true。
因此可以在循环体中使用 `interrupted()` 方法来判断线程是否处于中断状态，从而提前结束线程。

```java
public class ThreadInterrupted implements Runnable {

    @Override
    public void run() {
        while (!Thread.interrupted()) {
            System.out.printf("ThreadName:%s date:%s \n", Thread.currentThread().getName(), new Date());
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(new ThreadInterrupted());
        thread.start();

        Thread.sleep(10);
        // 中断线程
        thread.interrupt();
        System.out.printf("ThreadName:%s ending! \n", Thread.currentThread().getName());
    }
}
```

### Executor 的中断操作
调用 `Executor` 的 `shutdown()` 方法会等待线程都执行完毕之后再关闭，
但是如果调用的是 `shutdownNow()` 方法，则相当于调用每个线程的 `interrupt()` 方法。

```java
public class ThreadPoolExecutorRunnable implements Runnable{
    @Override
    public void run() {
        try {
            Thread.sleep(5000);
            System.out.printf("ThreadName:%s date:%s \n", Thread.currentThread().getName(), new Date());
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // 初始化线程池
        int corePoolSize = 3;
        int maxPoolSize = 5;
        long keepAliveTime = 5000;
        int bufferQueueSize = 50;
        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(corePoolSize, maxPoolSize, keepAliveTime, TimeUnit.SECONDS,
                new ArrayBlockingQueue<Runnable>(bufferQueueSize));
        // 执行Runnable任务
        threadPool.execute(new ThreadPoolExecutorRunnable());

        // 优雅关闭
        threadPool.shutdown();
        // 立刻关闭
        threadPool.shutdownNow();
        System.out.printf("ThreadName:%s ending! \n", Thread.currentThread().getName());
    }
}
```

如果只想中断 Executor 中的一个线程，可以通过使用 submit() 方法来提交一个线程，它会返回一个 Future<?> 对象，
通过调用该对象的 cancel(true) 方法就可以中断线程。

```java
public class ThreadPoolExecutorRunnable implements Runnable{
    @Override
    public void run() {
        try {
            Thread.sleep(5000);
            System.out.printf("ThreadName:%s date:%s \n", Thread.currentThread().getName(), new Date());
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // 初始化线程池
        int corePoolSize = 3;
        int maxPoolSize = 5;
        long keepAliveTime = 5000;
        int bufferQueueSize = 50;
        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(corePoolSize, maxPoolSize, keepAliveTime, TimeUnit.SECONDS,
                new ArrayBlockingQueue<Runnable>(bufferQueueSize));
        // 提交Runnable或Callable任务
        Future<?> future = threadPool.submit(new ThreadPoolExecutorRunnable());
        // 中断该线程
        future.cancel(true);
        System.out.printf("ThreadName:%s ending! \n", Thread.currentThread().getName());
    }
}
```


## 线程间通信

### join
在线程中调用另一个线程的 `join()` 方法，会将当前线程挂起，直到目标线程执行结束

```java
public class ThreadTest {
    public static void main(String[] args) {
        ThreadA threadA = new ThreadA();
        ThreadB threadB = new ThreadB(threadA);
        threadB.start();
        threadA.start();
    }

    public static class ThreadA extends Thread {
        @Override
        public void run() {
            System.out.println("ThreadA");
        }
    }

    public static class ThreadB extends Thread {
        private ThreadA threadA;

        public ThreadB(ThreadA threadA) {
            this.threadA = threadA;
        }

        @Override
        public void run() {
            try {
                threadA.join();
                System.out.println("ThreadB");
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```

### wait & notify & notifyAll
`wait()` 方法使得当前线程（调用 `wait()` 的线程）进入等待状态，直到其他线程调用同一个对象的 `notify()` 或 `notifyAll()` 方法

- 当前线程必须拥有该对象的监视器（即对象锁）才能调用其 `wait()` 方法。换句话说，必须在同步块或同步方法中调用 `wait()`
- 调用 `wait()` 后，线程会释放它持有的对象锁，进入等待池

```java
public class ThreadTest {
    public static void main(String[] args) {
        ThreadTest threadTest = new ThreadTest();
        Thread before = new Thread(() -> threadTest.before());
        Thread after = new Thread(() -> threadTest.after());
        after.start();
        before.start();
    }

    public synchronized void before() {
        System.out.println("before");
        notifyAll();
    }

    public synchronized  void after() {
        try {
            wait();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("after");
    }
}
```

### await & signal & signalAll

`java.util.concurrent` 类库中提供了 `Condition` 类来实现线程之间的协调，可以在 `Condition` 上调用 `await()` 方法使线程等待，
其它线程调用 `signal()` 或 `signalAll()` 方法唤醒等待的线程。相比于 `wait()` 这种等待方式，`await()` 可以指定等待的条件，因此更加灵活。

```java
public class ThreadTest {
    private Lock lock = new ReentrantLock();
    private Condition condition = lock.newCondition();

    public void before() {
        lock.lock();
        try {
            System.out.println("before");
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }

    public void after() {
        lock.lock();
        try {
            condition.await();
            System.out.println("after");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) {
        ThreadTest threadTest = new ThreadTest();
        Thread before = new Thread(() -> threadTest.before());
        Thread after = new Thread(() -> threadTest.after());
        after.start();
        before.start();
    }
}
```