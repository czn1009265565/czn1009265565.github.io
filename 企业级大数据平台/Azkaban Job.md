## Azkaban Job

### 单Job配置
1. 新建任务配置文件 `Hello-Azkaban.job`，内容如下。这里的任务很简单，就是输出一句 'Hello Azkaban!'

```
#command.job
type=command
command=echo 'Hello Azkaban!'
```

2. 打包上传

将 `Hello-Azkaban.job` 打包为 zip 压缩文件，通过 Web UI 界面上传

3. 点击页面上的 Execute Flow 执行任务

### 多Job配置
这里假设我们有五个任务（TaskA——TaskE）,D 任务需要在 A，B，C 任务执行完成后才能执行，而 E 任务则需要在 D 任务执行完成后才能执行，这种情况下需要使用 dependencies 属性定义其依赖关系。各任务配置如下

Task-A.job:

```
type=command
command=echo 'Task A'
```

Task-B.job:

```
type=command
command=echo 'Task B'
```

Task-C.job:

```
type=command
command=echo 'Task C'
```

Task-D.job

```
type=command
command=echo 'Task D'
dependencies=Task-A,Task-B,Task-C
```

Task-E.job

```
type=command
command=echo 'Task E'
dependencies=Task-D
```

### 调度其他任务
调度Hadoop任务

```
type=command
command=/usr/app/hadoop-2.6.0-cdh5.15.2/bin/hadoop fs -ls /
```

MR作业配置

```
type=command
command=/usr/app/hadoop-2.6.0-cdh5.15.2/bin/hadoop jar /usr/app/hadoop-2.6.0-cdh5.15.2/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.6.0-cdh5.15.2.jar pi 3 3
```

Hive作业

```
type=command
command=/usr/app/hive-1.1.0-cdh5.15.2/bin/hive -f 'test.sql'
```
