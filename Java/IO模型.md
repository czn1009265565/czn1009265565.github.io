# IO模型

## UNIX IO模型

1. 同步阻塞IO 数据的读取写入都阻塞在一个线程
2. 同步非阻塞IO 通过read轮询来实现非阻塞,缺点则是占用过高的CPU
3. IO多路复用 select/epoll系统调用,ready通知
4. 异步非阻塞IO 完成通知

## Java IO模型

1. BIO 同步阻塞IO
2. NIO (Selector,Channel,Buffer)可以看作IO多路复用
3. AIO 异步IO模型

![](pictures/NIO.png)

### Buffer

本质上是一个可以读写数据的内存块，可以理解成是一个容器对象。
用于和Channel交互,Channel 读取至 Buffer; Buffer 写入至 Channel

### Channel

和Stream类似，但不同点是双向的，总是基于Buffer缓冲区进行读写(可以同时进行读写)

### Selector

Selector被称为选择器，Selector会不断地轮询注册在其上的Channel，如果某个Channel上面发生读或者写事件，这个Channel就处于就绪状态, 进行后续的I/O操作。