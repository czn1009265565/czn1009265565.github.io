# Maven 仓库

Maven 仓库分为：

- **本地仓库**：运行 Maven 的计算机上的一个目录，它缓存远程下载的构件并包含尚未发布的临时构件。`settings.xml` 文件中可以看到 Maven 的本地仓库路径配置，默认本地仓库路径是在 `${user.home}/.m2/repository`。
- **远程仓库**：官方或者其他组织维护的 Maven 仓库。

Maven 远程仓库可以分为：

- **中央仓库**：这个仓库是由 Maven 社区来维护的，里面存放了绝大多数开源软件的包，并且是作为 Maven 的默认配置，不需要开发者额外配置。另外为了方便查询，还提供了一个[查询地址](https://search.maven.org/)，开发者可以通过这个地址更快的搜索需要构件的坐标。
- **私服**：私服是一种特殊的远程 Maven 仓库，它是架设在局域网内的仓库服务，私服一般被配置为互联网远程仓库的镜像，供局域网内的 Maven 用户使用。
- **其他的公共仓库**：有一些公共仓库是为了加速访问（比如阿里云 Maven 镜像仓库）或者部分构件不存在于中央仓库中。
 
## 仓库搭建

这里我采用docker的方式启动

```bash
docker run -d -p 8081:8081 --name nexus --restart=always sonatype/nexus3
```

管理员默认用户名admin,密码根据提示，`$ docker exec -it nexus bin/bash`查看`$ cat /nexus-data/admin.password`即可。

## 基本认识
管理员登录后，可以在设置页面管理角色、用户、仓库等其他一系列的操作。
通常我们需要设置proxy代理中央仓库为aliyun中央仓库 `http://maven.aliyun.com/nexus/content/groups/public`
默认有如下几个仓库:

|name|type|format|mean|
|---|---|---|---|
|maven-public|group|maven2|组合下述仓库|
|maven-central|proxy|maven2|代理中央仓库(阿里云镜像)|
|maven-releases|hosted|maven2|上传发布包的仓库|
|maven-snapshots|hosted|maven2|上传测试版本的仓库|

## 通用配置
所谓的通用配置就是所有本地项目默认都走该代理仓库

1.新建`settings-security.xml`

2.生成Master Password
```bash
mvn --encrypt-master-password
```

3.修改`settings-security.xml`
其中`<master></master>`中的内容为步骤二生成的密码。

```xml
<settingsSecurity>
<master>
	{SCMYWqA9gx0HhnqnT0OXHtqHsFO0eoBOd70PdgGrmos=}
</master>
</settingsSecurity>
```

4.生成maven私服密码

```bash
mvn --encrypt-password
```

5.修改`settings.xml`文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

  <mirrors>
     <mirror>
      <id>czndata-public</id>
      <mirrorOf>central</mirrorOf>
      <name>czndata-public</name>
      <url>http://nexus.czndata.cn/repository/maven-public/</url>
    </mirror>
  </mirrors>

  <servers>
    <server>
	  <id>czndata-public</id>
	  <username>username</username>
	  <password>{VNBgle6Dqp8HZg8ECCK4/fwcumRcGiYcyshHvTW26eA=}</password>
	</server>

	<server>
	  <id>czndata-releases</id>
	  <username>username</username>
	  <password>{VNBgle6Dqp8HZg8ECCK4/fwcumRcGiYcyshHvTW26eA=}</password>
	</server>

	<server>
	  <id>czndata-snapshots</id>
	  <username>username</username>
	  <password>{VNBgle6Dqp8HZg8ECCK4/fwcumRcGiYcyshHvTW26eA=}</password>
	</server>

  </servers>
</settings>
```
注意点： `server.id`仅需要与`mirror.id`对应即可。

### 项目配置
项目单独指定仓库

```xml
<!-- 仓库 -->
<repositories>
    <repository>
      <id>aliyun-repos</id>
      <name>aliyun-repos</name>
      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
</repositories>

<!-- 插件仓库 -->
<pluginRepositories>
    <pluginRepository>
      <id>aliyun-plugin</id>
      <name>aliyun-plugin</name>
      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </pluginRepository>
</pluginRepositories>
```

### 发布包
1. 如果需要向仓库中发布包的，首先需要对仓库有权限
2. 需要在项目pom文件中配置如下

```xml
<distributionManagement>
       <repository>
           <id>czndata-releases</id>
           <name>czndata-releases</name>
           <url>http://nexus.local:8081/repository/maven-releases/</url>
       </repository>
       <snapshotRepository>
           <id>czndata-snapshots</id>
           <name>czndata-snapshots</name>
           <url>http://nexus.local:8081/repository/maven-snapshots/</url>
       </snapshotRepository>
</distributionManagement>
```

3. 执行`mvn clean deploy`


只要在项目中配置 1.1.0-SNAPSHOT 这样，带有 SNAPSHOT 的就会到 snapshots 仓库，如果不加 SNAPSHOT 就会到 releases 仓库。

还有要注意的是，你要发布的包不能有父模块,否则在获取依赖的时候会有问题

