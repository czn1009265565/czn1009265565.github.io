## Azkaban 安装部署

### 下载源码包
下载所需版本的源码，Azkaban 的源码托管在 GitHub 上，地址为 https://github.com/azkaban/azkaban。
可以使用 git clone 的方式获取源码，也可以直接下载对应 release 版本的 tar.gz 文件

由于4.0.0版本编译失败，因此安装3.90.0版本

### 源码编译
1. 解压

```shell
tar -zxvf azkaban-3.90.0.tar.gz
mv azkaban-3.90.0 /usr/local/azkaban
```

2. 准备编译环境
    1. JDK1.8
    2. Gradle 可以不安装
3. 项目编译

在根目录下执行编译命令，编译成功后会有 BUILD SUCCESSFUL 的提示

```shell
./gradlew build installDist -x test
```

编译过程中需要注意以下问题：

- 缺乏gcc依赖包导致编译失败`yum install -y gcc gcc-c++*`即可
- 因为编译的过程需要下载大量的 Jar 包，下载速度根据网络情况而定，通常都不会很快，如果网络不好，耗费半个小时，一个小时都是很正常的；
- 编译过程中如果出现网络问题而导致 JAR 无法下载，编译可能会被强行终止，这时候重复执行编译命令即可，gradle 会把已经下载的 JAR 缓存到本地，所以不用担心会重复下载 JAR 包。

### 部署模式

- Solo mode 内置数据库，Server和Executor在同一个进程中
- Two mode 基于MySQL 数据库，启动一个Server,一个Executor
- Multi mode 分布式模式，启动一个Server,多个Executor


### Solo Server模式部署

1. 解压

Solo Server 模式安装包在编译后的 `/azkaban-solo-server/build/distributions`目录下

```shell
# 解压
tar -zxvf  azkaban-solo-server-3.90.0.tar.gz
```

2. 修改时区
```
vim conf/azkaban.properties

# 时区
default.timezone.id=Asia/Shanghai
```
3. 启动/关闭
```shell
bin/start-solo.sh
bin/shutdown-solo.sh
```

4. 验证

- jsp 查看`AzkabanSingleServer`进程
- 访问 8081 端口，查看 Web UI 界面，默认的登录名密码都是 azkaban


### Two mode模式部署
编译后获得

1. `azkaban-db-0.1.0-SNAPSHOT.tar.gz`
2. `azkaban-exec-server-0.1.0-SNAPSHOT.tar.gz`
3. `azkaban-web-server-0.1.0-SNAPSHOT.tar.gz`

