# JVM调优
优先架构调优和代码调优，JVM优化是不得已的手段，大多数的Java应用不需要进行JVM优化。

## 参数类型
- `-` 标准选项，`java -help`查看支持的选项
- `-X` 附加选项，`java -X`查看支持的选项，`-Xmx4096m -Xms4096m -Xloggc:/path/to/gc.log` 
- `-XX` 高级选项 `-XX:+HeapDumpOnOutOfMemoryError`

### `-XX` 高级选项
- Boolean类型  
  格式: `-XX:[+-]<name>` 表示启用或禁用 name 属性，`+`表示选项设置为true，`-`表示选项设置为false  
  示例: `-XX:+UseParallelGC -XX:+UseParallelOldGC` 启用ParallelGC收集器(jdk8默认)，`-XX:+UseG1GC` 启用G1垃圾收集器
- 非Boolean类型  
  格式: `-XX:<name>=<value>` 表示 name 属性的值是 value  
  示例: `-XX:MaxGCPauseMillis=500` 设置GC最大停用时间为500ms  
  其中最常用的`-Xmx` `-Xms` 也属于 `XX` 参数，`-Xms` 等价于 `-XX:InitialHeapSize` 初始化堆大小，
  `-Xmx` 等价于 `-XX:MaxHeapSize` 最大堆大小，`-xss` 等价于 `-XX:ThreadStackSize` 线程堆栈


## 监控工具

### jps
`jps` 查看本地正在运行的java进程和进程ID  
`jps -l` 查看类全路径

### jstat
Java虚拟机统计工具，全称“Java Virtual Machine statistics monitoring tool”。 可以用于监视JVM各种堆和非堆内存大小和使用量
- `jstat -class pid`: 输出加载类的数量及所占空间信息。
- `jstat -gc pid`: 输出gc信息，包括gc次数和时间，内存使用状况（可带时间和显示条目参数）

对应指标含义:  
S0C: 年轻代中第一个survivor（幸存区）的容量 （字节）  
S1C: 年轻代中第二个survivor（幸存区）的容量 (字节)  
S0U: 年轻代中第一个survivor（幸存区）目前已使用空间 (字节)  
S1U: 年轻代中第二个survivor（幸存区）目前已使用空间 (字节)  
EC: 年轻代中Eden（伊甸园）的容量 (字节)  
EU: 年轻代中Eden（伊甸园）目前已使用空间 (字节)  
OC: Old代的容量 (字节)  
OU: Old代目前已使用空间 (字节)  
MC: metaspace(元空间)的容量 (字节)  
MU: metaspace(元空间)目前已使用空间 (字节)  
YGC: 从应用程序启动到采样时年轻代中gc次数  
YGCT: 从应用程序启动到采样时年轻代中gc所用时间(s)  
FGC: 从应用程序启动到采样时old代(全gc)gc次数  
FGCT: 从应用程序启动到采样时old代(全gc)gc所用时间(s)  
GCT: 从应用程序启动到采样时gc用的总时间(s)

## 故障排查工具

### jinfo
主要用来查看和调整JVM参数

- `jinfo pid` 查看指定pid的所有JVM信息
- `jinfo -flags pid` 查询虚拟机运行参数信息

### jmap
手动导出内存映像文件
- `jmap -dump:format=b,file=/var/logs/heap.hprof pid`: 导出堆内存快照
- `jmap -heap pid`: 输出堆内存设置和使用情况（JDK11使用jhsdb jmap --heap --pid pid）
- `jmap -histo pid`: 输出heap的直方图，包括类名，对象数量，对象占用大小
- `jmap -histo:live pid`: 同上，只输出存活对象信息
- `jmap -clstats pid`: 输出加载类信息
- `jmap -help`: jmap命令帮助信息

### jstack
jstack命令用于生成虚拟机当前时刻的线程快照

- `jstack pid`

### MAT
MAT下载地址: `https://www.eclipse.org/mat/downloads.php`

1. overview: 堆内存大小、对象个数、类的个数、类加载器的个数、GC root 个数、线程概况等全局统计信息。
2. Leak Suspects: 直击引用链条上占用内存较多的可疑对象，可解决一些基础问题，但复杂的问题往往帮助有限。
3. Histogram: 罗列每个类实例的内存占比，包括自身内存占用量（Shallow Heap）及支配对象的内存占用量（Retain Heap），
   支持按 package、class loader、super class、class 聚类统计，最常用的功能之一。

    1. Merge Shortest to Paths to GC Roots
    2. exclude all phantom/weak/soft/etc. references
4. Dominator tree: 按对象的 Retain Heap 排序，也支持按多个维度聚类统计，最常用的功能之一


## 实战

### CPU飙高排查
CPU飙高可能的原因: 线程死锁，死循环等

1. 查看CPU占用 `top`
2. 转储Java进程内的线程堆栈信息 `jstack pid > pid.txt`
3. 查看进程中最占CPU的线程 `top -Hp pid`
4. 最耗CPU的线程PID转换为16进制输出 `printf "%x" pid`
5. 查看高占用CPU具体问题 文本搜索16进制线程号

### 内存溢出
- 堆内存溢出
- 栈内存溢出 
- 方法区溢出
- 直接内存溢出

#### 堆内存溢出
报错信息: `java.lang.OutOfMemoryError: Java heap space`

可能的原因: 存在内存泄露或大对象分配

解决: 分析堆内存排查是否存在内存泄露，调整堆内存大小`-Xmx`

#### 栈内存溢出
报错信息: `java.lang.StackOverflowError`

可能的原因: 线程请求的栈深度大于虚拟机所允许的最大深度，例如不合理的递归调用

解决: 调整栈内存大小`-Xss`

#### 方法区溢出

报错信息: `java.lang.OutOfMemoryError：Metaspace`
可能的原因: 常量池里对象过大，加载的类过多
解决办法: 留空元空间相关配置(因为元空间使用的是本机直接内存)，或设置元空间大小 `-XX:MetaspaceSize`和`-XX:MaxMetaspaceSize`

### 项目变慢

可能的原因:   
1. Stop The World过长
2. 项目依赖的资源变慢，例如DB表过大
3. 线程竞争
4. 服务器问题，CPU、内存占用
