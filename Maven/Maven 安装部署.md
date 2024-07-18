# Maven安装部署

## 前置准备

确保JDK正确安装部署

```shell
java -version
```

## Windows安装部署

1. 访问下载页面：`http://maven.apache.org/download.html`
2. 下载zip二进制包，解压并重命名至 `C:\Program Files\apache-maven`
3. 新增环境变量 M2_HOME, `C:\Program Files\apache-maven`
4. 环境变量Path新增 `%M2_HOME%\bin`
5. 测试 `mvn -version`
6. 配置阿里云镜像仓库 `~/.m2/settings.xml`文件  
   ```xml
   <mirrors>
     <mirror>
         <id>nexus-aliyun</id>
         <mirrorOf>central</mirrorOf>
         <name>Nexus aliyun</name>
         <url>http://maven.aliyun.com/nexus/content/groups/public</url>
     </mirror>
   </mirrors>
   ```
7. 指定下载资源路径
   ```xml
   <localRepository>D:/maven/repository</localRepository>
   ```
8. 代理配置
   ```xml
   <proxies>
     <proxy>
         <id>httpproxy</id>
         <active>true</active>
         <protocol>http</protocol>
         <host>localhost</host>
         <port>10809</port>
     </proxy>
     <proxy>
         <id>httpsproxy</id>
         <active>true</active>
         <protocol>https</protocol>
         <host>localhost</host>
         <port>10809</port>
     </proxy>
   </proxies>
   ```

## Linux安装部署

1. 访问下载页面：`http://maven.apache.org/download.html`
2. 下载tar二进制包，解压并重命名至 `/usr/local/apache-maven`
3. 配置环境变量
   ```shell
   ### 配置环境变量
   vim /etc/profile
   
   export MAVEN_HOME=/usr/local/apache-maven
   export PATH=$PATH:$MAVEN_HOME/bin
   
   source /etc/profile
   ```
4. 测试 `mvn --version`
5. 配置阿里云镜像仓库 `vim /usr/local/apache-maven/conf/settings.xml`  
   在`<mirrors></mirrors>`之间新增
   ```xml
   <mirrors>
     <mirror>
         <id>nexus-aliyun</id>
         <mirrorOf>central</mirrorOf>
         <name>Nexus aliyun</name>
         <url>http://maven.aliyun.com/nexus/content/groups/public</url>
     </mirror>
   </mirrors>
   ```