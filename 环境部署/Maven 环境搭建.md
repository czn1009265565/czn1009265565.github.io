# Maven 环境搭建
官网地址: http://maven.apache.org/ 下载二进制包

## Centos7
### 解压缩

```shell
tar -vxf apache-maven-3.6.3-bin.tar.gz
mv /root/apache-maven-3.6.3 /usr/local/apache-maven
```

### 配置环境变量

```shell
vim /etc/profile

export MAVEN_HOME=/usr/local/apache-maven
export PATH=$PATH:$MAVEN_HOME/bin

source /etc/profile
```

### 查看版本号

```shell
mvn --version
```

### 配置镜像地址

```shell
vim /usr/local/apache-maven/conf/settings.xml

# 在<mirrors></mirrors>之间新增
<mirror>
    <id>nexus-aliyun</id>
    <mirrorOf>central</mirrorOf>
    <name>Nexus aliyun</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public</url>
</mirror>
```

## Windows 

1. 确保已安装JDK，并配置JAVA_HOME,详情查看Java环境配置

2. 新增环境变量 M2_HOME, `C:\Program Files\apache-maven`
   
3. 环境变量Path新增 `%M2_HOME%\bin`
   
4. 测试 `mvn -version`
   
5. 阿里云镜像配置 修改maven根目录下的conf文件夹中的settings.xml文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <pluginGroups></pluginGroups>
  <proxies></proxies>
  <servers></servers>

  <mirrors>
    <mirror>
        <id>nexus-aliyun</id>
        <mirrorOf>central</mirrorOf>
        <name>Nexus aliyun</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public</url>
    </mirror>
  </mirrors>

  <profiles></profiles>
</settings>
```