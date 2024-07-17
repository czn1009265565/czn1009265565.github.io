# Java 环境搭建

本文介绍 Centos7 搭建 Java环境

## 查看版本
查看yum包含的jdk版本

```shell
yum list | grep openjdk
```

### 安装JDK
JDK 默认安装位置：`/usr/lib/jvm`

```shell
# JDK1.8
yum install -y java-1.8.0-openjdk.x86_64
# JDK11
yum install -y java-11-openjdk.x86_64
```

### 配置全局变量
```shell
vim /etc/profile 

# JDK1.8
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$PATH:$JAVA_HOME/bin

# JDK11
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-11.0.23.0.9-2.el7_9.x86_64
export PATH=$PATH:$JAVA_HOME/bin

source /etc/profile
```

### JDK版本查看

```shell
java -version
```