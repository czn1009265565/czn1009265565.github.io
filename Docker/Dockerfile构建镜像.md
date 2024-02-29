# Dockerfile指令
Dockerfile 是一个文本文件，其内包含了一条条的指令(Instruction)，每一条指令构建一层，因此每一条指令的内容，就是描述该层应当如何构建。

## 指令
### Form
指定基础镜像

```
FROM openjdk:8-jdk-alpine
```

### RUN
执行命令行命令

```
RUN shell
```
但是这里有一个注意点，Dockerfile 中每一个指令都会建立一层，RUN 也不例外。每一个 RUN 的行为，就和刚才我们手工建立镜像的过程一样：新建立一层，在其上执行这些命令，执行结束后，commit 这一层的修改，构成新的镜像。因此我们可以用`&&`将多个命令串联起来。

### COPY
支持通配符
```
COPY file /root/file
COPY dir /root/dir
COPY file* /root/
```

### ENV
设置环境变量，无论是后面的其它指令，还是运行时的应用，都可以直接使用这里定义的环境变量。

* `ENV <key> <value>`
* `ENV <key1>=<value1> <key2>=<value2>...`

### ARG
构建参数和 `ENV` 的效果一样，都是设置环境变量。所不同的是，`ARG` 所设置的构建环境的环境变量，在将来容器运行时是不会存在这些环境变量的。

* `ARG <key> <value>`
* `ARG <key1>=<value1> <key2>=<value2>...`


### WORKDIR
使用 WORKDIR 指令可以来指定工作目录（或者称为当前目录），以后各层的当前目录就被改为指定的目录，如该目录不存在，WORKDIR 会帮你建立目录。

```
RUN cd /app
RUN echo "hello" > world.txt
```
如果将这个 Dockerfile 进行构建镜像运行后，会发现找不到 /app/world.txt 文件，或者其内容不是 hello。原因其实很简单，在 Shell 中，连续两行是同一个进程执行环境，因此前一个命令修改的内存状态，会直接影响后一个命令；而在 Dockerfile 中，这两行 RUN 命令的执行环境根本不同，是两个完全不同的容器。这就是对 Dockerfile 构建分层存储的概念不了解所导致的错误。
```
WORKDIR /root/project
```

### CMD
CMD 指令就是用于指定默认的容器主进程的启动命令的.
一些初学者将 CMD 写为：

```
CMD service nginx start
```
然后发现容器执行后就立即退出了。甚至在容器内去使用 systemctl 命令结果却发现根本执行不了。这就是因为没有搞明白前台、后台的概念，没有区分容器和虚拟机的差异，依旧在以传统虚拟机的角度去理解容器。

对于容器而言，其启动程序就是容器应用进程，容器就是为了主进程而存在的，主进程退出，容器就失去了存在的意义，从而退出，其它辅助进程不是它需要关心的东西。
正确的做法是直接执行 nginx 可执行文件，并且要求以前台形式运行
```
CMD nginx -g "daemon off;"
```

## Java服务示例

```
FROM openjdk:8-jdk-alpine

## 创建目录，并使用它作为工作目录
RUN mkdir -p /yudao-server
WORKDIR /yudao-server
## 将后端项目的 Jar 文件，复制到镜像中
COPY ./target/yudao-server.jar app.jar

## 设置 TZ 时区
ENV TZ=Asia/Shanghai
## 设置 JAVA_OPTS 环境变量，可通过 docker run -e "JAVA_OPTS=" 进行覆盖
ENV JAVA_OPTS="-Xms512m -Xmx512m"

## 应用参数
ENV ARGS=""

## 启动后端项目
CMD java ${JAVA_OPTS} -jar app.jar $ARGS
```