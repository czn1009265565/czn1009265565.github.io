## Flume 安装部署

### 前置环境

1. Java 环境搭建

### 安装步骤

1. 下载并解压
```markdown
$ wget https://dlcdn.apache.org/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz
$ tar -zxvf apache-flume-1.9.0-bin.tar.gz
$ mv apache-flume-1.9.0-bin /usr/local/flume
```

2. 配置环境变量
```markdown
$ vim /etc/profile

export FLUME_HOME=/usr/local/flume
export PATH=$FLUME_HOME/bin:$PATH

$ source /etc/profile
```

3. 修改配置文件
```markdown
$ cp flume-env.sh.template flume-env.sh

$ vim flume-env.sh
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
```

4. 验证
```markdown
$ flume-ng version
```
出现对应版本信息则代表成功
