# Python多线程

## 介绍
Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁: `Global Interpreter Lock`，任何Python线程执行前，必须先获得GIL锁。
Python中得多线程只能交替执行，仅能利用单核CPU，因此适用于I/O密集型任务，而不是CPU密集型任务。

Python处理线程的模块有两个: `thread` 和 `threading`。Python3中停用了 `thread` 模块，并改名为 `_thread`，
并在 `_thread` 模块的基础上开发了更高级的 `threading` 模块。

## 创建线程

创建线程的方法有两种，一种是直接使用 `threading` 模块里面的类来进行创建，一种是继承 `threading` 模块的类写一个类来对线程进行创建。

### 直接创建

```python
import time
import threading


def print_time(thread_name, delay) -> None:
    """
    时间打印
    :param thread_name: 线程名称
    :param delay: 延时时间
    :return: None
    """
    while True:
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        time.sleep(delay)


if __name__ == "__main__":
    job1 = threading.Thread(target=print_time, args=('Thread-1', 3))
    job1.start()
    job2 = threading.Thread(target=print_time, args=('Thread-2', 3))
    job2.start()
```

### 继承创建

```python
import threading
import time


class MyThread(threading.Thread):
    def __init__(self, delay, **kwargs):
        # 必须调用父类的初始化方法
        super().__init__(**kwargs)
        self.delay = delay

    def run(self) -> None:
        while True:
            print("%s: %s" % (threading.current_thread().name, time.ctime(time.time())))
            time.sleep(self.delay)


if __name__ == "__main__":
    job1 = MyThread(3, name="Thread-1")
    job1.start()
    job2 = MyThread(3, name="Thread-2")
    job2.start()
```

## 守护线程

守护线程（Daemon Thread）‌是一种在程序后台运行的线程，主要用于为其他线程提供服务和支持。有以下两个特点:

1. 后台运行: 守护线程在程序后台运行，不直接影响程序的执行流程
2. 自动终止: 当所有的非守护线程结束运行时，守护线程会自动退出，程序也会随之终止

```python
import time
import threading


def print_time(thread_name, delay) -> None:
    while True:
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        time.sleep(delay)


if __name__ == "__main__":
    job1 = threading.Thread(target=print_time, args=('Thread-1', 3), daemon=True)
    job1.start()
    job2 = threading.Thread(target=print_time, args=('Thread-2', 3), daemon=True)
    job2.start()
    print("主线程结束")
```
可以看到，当我们设置为守护线程后，随着main线程的结束，程序立刻就停止了。


## 阻塞线程

`join()` 方法会使线程进入等待状态（阻塞），直到调用 `join()` 方法的子线程运行结束。同时也可以通过设置 `timeout` 参数来设定等待的时间

```python
import time
import threading


def print_time(thread_name, delay) -> None:
    while True:
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        time.sleep(delay)


if __name__ == "__main__":
    job1 = threading.Thread(target=print_time, args=('Thread-1', 3), daemon=True)
    job1.start()
    job1.join()
    print("主线程结束")
```

## 线程安全
我们可以进行这样一个实验，定义一个全局变量 num=0，开启两个线程对其进行1000000次加1，最后打印结果
```python
import threading

num = 0


def add():
    global num
    for i in range(1000000):
        num += 1


if __name__ == "__main__":
    job1 = threading.Thread(target=add, name='add1')
    job1.start()
    job2 = threading.Thread(target=add, name='add2')
    job2.start()

    job1.join()
    job2.join()
    print('num = {}'.format(num))
```
在Python3.6中，可以发现最终结果并不等于2000000，并且每次执行的结果都不同。(Python3.10居然每次都是2000000)

### 互斥锁
互斥锁是一种简单的加锁方法，用于控制对共享资源的访问。互斥锁只有两种状态:上锁和解锁。
如果互斥量已经上锁，调用线程会阻塞，直到互斥量被解锁。互斥锁保证了一次只有一个线程可以访问共享资源。

```python
import threading

num = 0
# 声明互斥锁
lock = threading.Lock()


def add():
    global num
    for i in range(1000000):
        # 加锁
        lock.acquire()
        num += 1
        # 释放锁
        lock.release()


if __name__ == "__main__":
    job1 = threading.Thread(target=add, name='add1')
    job1.start()
    job2 = threading.Thread(target=add, name='add2')
    job2.start()

    job1.join()
    job2.join()
    print('num = {}'.format(num))
```
到这里我们可以思考一个问题，假如上文add函数方法里面存在递归调用自身的情况，那么就会发生同一线程多次获取同一个锁的情况，也就造成了死锁，
因此需要引入可重入锁的概念。

### 可重入锁
可重入锁，也称为递归锁，允许同一个线程在已经持有锁的情况下，可以再次获取该锁而不会造成死锁。
其核心特性是锁能够支持同一线程的多次加锁。

```python
import threading

num = 0
# 声明互斥锁
lock = threading.Lock()


def add():
    global num
    for i in range(1000000):
        # 加锁
        lock.acquire()
        num += 1
        # 递归调用一次
        if num == 1000000:
            add()
        # 释放锁
        lock.release()


if __name__ == "__main__":
    job = threading.Thread(target=add, name='add1')
    job.start()

    job.join()
    print('num = {}'.format(num))
```

### 信号量
互斥锁同时只允许一个线程修改数据，而Semaphore是同时允许一定数量的线程修改数据

```python
import time
import threading

semaphore = threading.BoundedSemaphore(3)


def print_time(thread_name, delay) -> None:
    semaphore.acquire()
    print("%s: %s" % (thread_name, time.ctime(time.time())))
    time.sleep(delay)
    semaphore.release()


if __name__ == "__main__":
    for i in range(10):
        job = threading.Thread(target=print_time, args=('Thread-%s'%i, 3))
        job.start()
    print("主线程结束")
```


### 事件
Event是Python多线程同步编程中的一种同步原语，它可以协调多个线程的操作，以达到线程间传递信号、同步操作等目的。

Event 全局定义了一个内置标志Flag，当Flag未被设置时(False)，所有等待该Event的线程都会被阻塞，直到Event被设置为True。
当Event被设置为True时，所有等待该Event的线程都会被唤醒。


- `set()`     将Flag设为True，并通知所有处于等待阻塞状态的线程恢复运行状态
- `wait([timeout])`    如果标志为True将立即返回，否则一直阻塞线程，如果设置了timeout，则阻塞一定时间
- `clear()`   将Flag设置为False
- `is_set()`  返回bool值，判断Flag是否为True

案例一: 裁判开枪，运动员们同时起跑  
```python
import threading
import time

# 创建Event实例
et = threading.Event()


def run():
    print("%s waiting~" % threading.current_thread().name)
    et.wait()
    print("%s running~ time:%s" % (threading.current_thread().name, time.time()))


if __name__ == "__main__":
    for i in range(10):
        thread = threading.Thread(target=run, name="athlete-%s" % i)
        thread.start()

    time.sleep(10)
    et.set()
```

案例二: 线程的启动与关闭  
```python
import threading
import time


def start_up(event):
    print("线程%s开启"%threading.current_thread().name)
    event.clear()
    while not event.is_set():
        print("%s: %s" % (threading.current_thread().name, time.ctime(time.time())))
        event.wait(3)
    print("线程%s关闭" % threading.current_thread().name)


def shutdown(event):
    event.set()


if __name__ == "__main__":
    event = threading.Event()
    # 启动线程
    job1 = threading.Thread(target=start_up, args=(event, ), name="start_up")
    job1.start()

    time.sleep(10)
    # 关闭线程
    job2 = threading.Thread(target=shutdown, args=(event, ), name="shutdown")
    job2.start()
```

## 线程池
线程是稀缺资源，如果无限制的创建与销毁，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一的分配，调优和监控

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor

# 创建一个包含3个线程的线程池
pool = ThreadPoolExecutor(3)


# 定义一个函数，该函数将被线程池中的线程执行
def task_function(x):
    # 随机休息1~3秒
    time.sleep(random.randint(1, 3))
    return x * x


if __name__ == "__main__":
    # 使用线程池执行任务
    results = [pool.submit(task_function, i) for i in range(10)]

    # 获取所有任务的结果
    for future in results:
        print(future.result())
```
`result` 方法能够输出对应的线程运行后方法的返回结果，如果线程还在运行，那么其会一直阻塞在那里，直到该线程运行完。
当然，也可以设置 `result(timeout)`，即如果调用还没完成那么这个方法将等待 `timeout` 秒。如果在 `timeout` 秒内没有执行完成，
则会抛出 `concurrent.futures.TimeoutError` 异常。
