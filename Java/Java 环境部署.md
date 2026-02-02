# Java 环境部署

## Windows

```shell
# 1. 下载JDK
# 访问 Oracle 官网或 OpenJDK 网站下载对应版本的JDK

# 2. 安装JDK
# 运行下载的exe安装程序，按提示完成安装

# 3. 配置环境变量
# 右键"此电脑" -> "属性" -> "高级系统设置" -> "环境变量"

# 新建系统变量：
JAVA_HOME = C:\Program Files\Java\jdk-21

# 编辑Path变量，添加：
%JAVA_HOME%\bin

# 4. 验证安装
java -version
```

## CentOS 7

```shell
# 1. 更新系统
sudo yum update -y

# 2. 查看可用的JDK版本
yum search java | grep -i --color JDK

# 3. 安装OpenJDK（选择其中一个版本）
sudo yum install -y java-11-openjdk-devel
# 或
sudo yum install -y java-17-openjdk-devel
# 或
sudo yum install -y java-21-openjdk-devel

# 4. 验证安装
java -version

# 5. 设置默认Java版本（如果有多个版本）
sudo alternatives --config java
```

## Ubuntu

```shell
# 1. 更新包索引
sudo apt update

# 2. 安装OpenJDK
sudo apt install -y openjdk-11-jdk
# 或
sudo apt install -y openjdk-17-jdk
# 或
sudo apt install -y openjdk-21-jdk

# 3. 验证安装
java -version
javac -version

# 4. 设置默认版本（如果有多个版本）
sudo update-alternatives --config java
```