## Java 环境搭建

本文介绍 Centos7 搭建 Java环境

### 查看版本
查看yum包含的jdk版本

```shell
yum list java*
```

### 下载jdk1.8

```shell
yum install -y java-1.8.0-openjdk-devel.x86_64
```

### 配置全局变量
```shell
vim /etc/profile 

export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$PATH:$JAVA_HOME/bin

source /etc/profile
```
### jdk版本查看

```shell
java -version
```