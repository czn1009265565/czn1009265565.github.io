# Java 并发

## 背景
为什么需要多线程?

1. 多线程使得程序可以同时处理多个任务或请求，当一个线程执行耗时操作（如网络请求、文件读写等）时，其他线程可以继续执行，从而避免程序因为等待而被阻塞
2. 充分利用多核处理器，现代计算机通常拥有多个处理核心，多线程可以将任务分配给不同的核心并发执行，提高计算机系统的利用率和性能。
3. 简化编程模型： 多线程可以将复杂的任务分解为多个子任务，并发执行，使得程序结构更加清晰简洁。例如，在图形界面应用程序中，可以使用多线程来处理用户界面的响应和后台任务的执行，提升用户体验。
4. 资源共享和通信： 多线程可以共享同一进程的内存空间，使得线程之间可以方便地共享数据和通信。这样可以避免复制大量数据或使用复杂的进程间通信机制。

尽管多线程带来了很多好处，但也需要注意一些问题，例如线程安全性、死锁、上下文切换消耗等。

### 线程安全

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
上述代码正确输出结果应该为1000,但实际情况却不是这样，答案往往小于1000。真正的问题在于run方法的执行过程中可能会被中断。如果能够确保线程失去控制之前方法运行完成，则数据累加和永远不会讹误。

### 死锁
线程1申请了A资源的同时去申请B资源
线程2申请了B资源的同时去申请A资源

example:
```
// 线程1
begin;
update table set a=a+1 where id=1;

update table set a=a+1 where id=2;
commit;

// 线程2
begin;
update table set a=a+1 where id=2;

update table set a=a+1 where id=1;
commit;
```

#### 避免死锁

1. 避免一个线程同时获取多个锁
2. 避免一个锁占用多个资源.这里需要理解资源的概念,排他性使用的对象叫做资源,例如写文件

#### 死锁检测与恢复

1. 深度优先遍历资源线程分配图 a资源 -> A线程 -> 线程A还占用了b资源 -> B线程占用了b资源 -> B线程还占用了a资源
2. 主动释放,在Mysql中主动杀死小的事务

## Java 锁

### synchronized

1. 修饰实例方法: 作用于当前对象实例加锁，进入同步代码前要获得 当前对象实例的锁
2. 修饰静态方法: 给当前类加锁，会作用于类的所有对象实例 ，进入同步代码前要获得 当前 class 的锁
3. 修饰代码块  
    - `synchronized(this)` 表示进入同步代码库前要获得当前对象的锁
    - `synchronized(object)` 表示进入同步代码库前要获得给定对象的锁
    - `synchronized(类.class)` 表示进入同步代码前要获得 当前 class 的锁

#### 底层原理
对象实例在JVM堆中分为三部分

1. 对象头
2. 实例数据
3. 对齐填充字节

在同步的时候,获取对象的monitor即获取对象的锁,无非就是类似对对象的一个标志,
那么这个标志就是存放在Java对象的对象头。Java对象头里的Mark Word里默认的存放的对象的Hashcode,分代年龄和锁标记位

#### 锁状态

优化后锁状态分为以下四种,且锁状态只升不降

1. 无锁  
   CAS 无锁的特点就是修改操作在循环内进行，线程会不断的尝试修改共享资源。如果没有冲突就修改成功并退出，否则就会继续循环尝试
2. 偏向锁  
   偏向锁是指一段同步代码一直被一个线程所访问,那么该线程会自动获取锁而无需通过CAS获取锁,降低获取锁的代价。
3. 轻量级锁
   是指当锁是偏向锁的时候，被另外的线程所访问，偏向锁就会升级为轻量级锁，其他线程会通过自旋的形式尝试获取锁，不会阻塞，从而提高性能。
4. 重量级锁  
   升级为重量级锁时，锁标志的状态值变为“10”，此时Mark Word中存储的是指向重量级锁的指针，此时等待锁的线程都会进入阻塞状态。

### CAS(Compare And Swap)
适用于并发冲突较小的情况

存在的问题:

1. ABA问题

   解决:新增版本号字段
2. 自旋时间过长,导致CPU占用过高
3. 只能保证一个共享变量的原子操作

   当对一个共享变量执行操作时CAS能保证其原子性，如果对多个共享变量进行操作,CAS就不能保证其原子性。
   有一个解决方案是利用对象整合多个共享变量，即一个类中的成员变量就是这几个共享变量。
   然后将这个对象做CAS操作就可以保证其原子性。atomic中提供了AtomicReference来保证引用对象之间的原子性。

### volatile

1. 只能修饰变量
2. 保证变量在多个线程间的可见性,但不能保证原子性,和有序性

有序性:

引出指令重排,处理器为了提高运行效率,可能会对输入代码进行优化,
不保证执行顺序与代码顺序一致,但会保证最终执行结果和代码顺序执行一致.也就是说如下1,2顺序有可能互换,3和4也有可能互换
指令重排序不会影响单个线程的执行,但是会影响到线程并发执行的正确性.
```
int a = 0; // 1
int b = 0; // 2
a++;       // 3
b++;       // 4
```

应用场景: 状态标志
```
volatile boolean shutdownRequested;  
public void shutdown() {   
    shutdownRequested = true;   
}  
public void doWork() {   
    while (!shutdownRequested) {   
        // 代码业务逻辑  
    }  
}
```
线程A执行doWork()的逻辑代码时，线程B调用了shutdown()方法，线程A立即停止运行while中的逻辑代码。


### AQS(队列同步器)
同步器是用来构建锁和其他同步组件的基础框架,
AQS 使用一个 int 成员变量来表示同步状态，通过内置的 FIFO 队列来实现阻塞队列。AQS 使用 CAS 对该同步状态进行原子操作实现对其值的修改。

并发请求过程:

线程A请求共享资源,这个时候共享资源闲置(volatile 修饰的int成员变量来表示同步状态),则将线程A设置为有效的工作线程,并将共享资源设置为锁定状态(CAS原子操作实现修改)。
此时线程B请求该共享资源,发现共享资源被线程A占用,则将当前线程和等待信息构造成一个Node加入同步队列(双向链表,CAS add tail),同时阻塞线程.
当同步状态释放时,则唤醒首节点线程(这里可以引出公平锁、非公平锁的概念,队列中都是顺序的)。

### 公平锁和非公平锁
- 公平锁：按照线程在队列中的排队顺序，先到者先拿到锁
- 非公平锁：当线程要获取锁时，先通过两次 CAS 操作去抢锁，如果没抢到，当前线程再加入到队列中等待唤醒

1. 非公平锁性能优于公平锁(频繁上下文切换)
2. 非公平锁带来饥饿,最坏的情况,可能存在某一个线程一直获取不到锁

### 资源共享方式
AQS提供的模板方法可分为三类:

1. 独占式获取与释放同步状态
2. 共享式获取与释放同步状态
3. 查询同步队列中等待线程情况

### Lock
锁是用来控制多个线程访问共享资源的方式，一般来说，一个锁能够防止多个线程同时访问共享资源

虽然它失去了像synchronize关键字隐式加锁解锁的便捷性，但是却拥有了锁获取和释放的可操作性，
可中断的获取锁以及超时获取锁等多种synchronized关键字所不具备的同步特性。

1. void lock(); //获取锁
2. void lockInterruptibly() throws InterruptedException; //获取锁的过程能够响应中断
3. boolean tryLock(); //非阻塞式响应中断能立即返回，获取锁返回true反之返回fasle
4. boolean tryLock(long time, TimeUnit unit) throws InterruptedException;//超时获取锁，在超时内或者未中断的情况下能够获取锁
5. Condition newCondition();//获取与lock绑定的等待通知组件，当前线程必须获得了锁才能进行等待，进行等待时会先释放锁，当再次获取锁时才能从等待中返回

### ReentrantLock

```java
public class LockTest {
    // 初始化选择公平锁(true)、非公平锁(false)
    private static ReentrantLock lock = new ReentrantLock(false);

    public void fairLock() {
        // 获取不到锁则阻塞
        lock.lock();
        try {
            // 具体业务逻辑
        } finally {
            lock.unlock();
        }
    }

    public void nonFairLock() {
        boolean condition = lock.tryLock();
        if (!condition){
            // 未获取到锁
            return;
        }
        try {
            // 具体业务逻辑
        }
        finally {
            // 手动释放锁
            lock.unlock();
        }
    }
}
```
