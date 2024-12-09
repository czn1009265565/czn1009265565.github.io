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

### 可重入锁
RLock被称为重入锁，RLock锁是一个可以被同一个线程多次 acquire 的锁，但是最后必须由获取它的线程来释放它，
不论同一个线程调用了多少次的acquire，最后它都必须调用相同次数的 release 才能完全释放锁，这个时候其他的线程才能获取这个锁。

### 信号量


### 事件
Event是Python多线程同步编程中的一种同步原语，它可以协调多个线程的操作，以达到线程间传递信号、同步操作等目的。

Event 全局定义了一个内置标志Flag，当Flag未被设置时(False)，所有等待该Event的线程都会被阻塞，直到Event被设置为True。
当Event被设置为True时，所有等待该Event的线程都会被唤醒。


- `set()`     将Flag设为True，并通知所有处于等待阻塞状态的线程恢复运行状态
- `wait([timeout])`    如果标志为True将立即返回，否则一直阻塞线程，如果设置了timeout，则阻塞一定时间
- `clear()`   将Flag设置为False
- `is_set()`  返回bool值，判断Flag是否为True

## 线程池

