## Azkaban Flow

官方提供了一个比较完善的配置样例

```yaml
config:
  user.to.proxy: azktest
  param.hadoopOutData: /tmp/wordcounthadoopout
  param.inData: /tmp/wordcountpigin
  param.outData: /tmp/wordcountpigout

# This section defines the list of jobs
# A node can be a job or a flow
# In this example, all nodes are jobs
nodes:
 # Job definition
 # The job definition is like a YAMLified version of properties file
 # with one major difference. All custom properties are now clubbed together
 # in a config section in the definition.
 # The first line describes the name of the job
 - name: AZTest
   type: noop
   # The dependsOn section contains the list of parent nodes the current
   # node depends on
   dependsOn:
     - hadoopWC1
     - NoOpTest1
     - hive2
     - java1
     - jobCommand2

 - name: pigWordCount1
   type: pig
   # The config section contains custom arguments or parameters which are
   # required by the job
   config:
     pig.script: src/main/pig/wordCountText.pig

 - name: hadoopWC1
   type: hadoopJava
   dependsOn:
     - pigWordCount1
   config:
     classpath: ./*
     force.output.overwrite: true
     input.path: ${param.inData}
     job.class: com.linkedin.wordcount.WordCount
     main.args: ${param.inData} ${param.hadoopOutData}
     output.path: ${param.hadoopOutData}

 - name: hive1
   type: hive
   config:
     hive.script: src/main/hive/showdb.q

 - name: NoOpTest1
   type: noop

 - name: hive2
   type: hive
   dependsOn:
     - hive1
   config:
     hive.script: src/main/hive/showTables.sql

 - name: java1
   type: javaprocess
   config:
     Xms: 96M
     java.class: com.linkedin.foo.HelloJavaProcessJob

 - name: jobCommand1
   type: command
   config:
     command: echo "hello world from job_command_1"

 - name: jobCommand2
   type: command
   dependsOn:
     - jobCommand1
   config:
     command: echo "hello world from job_command_2"
```

### 简单任务调度

1. 新建Flow配置文件 `simple.flow`

```yaml
nodes:
  - name: jobA
    type: command
    config:
      command: echo "Hello Azkaban Flow 2.0."
```

2. 新建一个 `simple.project` 文件，指明是使用的是 Flow 2.0

```
azkaban-flow-version: 2.0
```

3. 打包上传 `simple.zip`

### 多任务调度

和 1.0 给出的案例一样，这里假设我们有五个任务, D 任务需要在 A，B，C 任务执行完成后才能执行，而 E 任务则需要在 D 任务执行完成后才能执行，
相关配置文件应如下。可以看到在 1.0 中我们需要分别定义五个配置文件，而在 2.0 中我们只需要一个配置文件即可完成配置。

```yaml
nodes:
  - name: jobE
    type: command
    config:
      command: echo "This is job E"
    # jobE depends on jobD
    dependsOn: 
      - jobD
    
  - name: jobD
    type: command
    config:
      command: echo "This is job D"
    # jobD depends on jobA、jobB、jobC
    dependsOn:
      - jobA
      - jobB
      - jobC

  - name: jobA
    type: command
    config:
      command: echo "This is job A"

  - name: jobB
    type: command
    config:
      command: echo "This is job B"

  - name: jobC
    type: command
    config:
      command: echo "This is job C"
```


### 内嵌流

Flow2.0 支持在一个 Flow 中定义另一个 Flow，称为内嵌流或者子流。这里给出一个内嵌流的示例，其 Flow 配置如下：

```yaml
nodes:
  - name: jobC
    type: command
    config:
      command: echo "This is job C"
    dependsOn:
      - embedded_flow

  - name: embedded_flow
    type: flow
    config:
      prop: value
    nodes:
      - name: jobB
        type: command
        config:
          command: echo "This is job B"
        dependsOn:
          - jobA

      - name: jobA
        type: command
        config:
          command: echo "This is job A"
```