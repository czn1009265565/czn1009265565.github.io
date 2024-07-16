# Maven最佳实践

## Maven项目

### 创建Maven项目
IDEA创建Maven项目

1. File => New => Project => Maven Archetype
2. 选择对应的JDK版本
3. Archetype: maven-archetype-quickstart
4. 等待项目初始化

### Maven目录结构

```groovy
src /
  main /
    java/
    resources/
  test / 
    java/
    resources/
pom.xml
```

- `src/main/java`：源代码目录
- `src/main/resources`：资源文件目录
- `src/test/java`：测试代码目录
- `src/test/resources`：测试资源文件目录

### 属性配置

```xml
<properties>
    <jdk.version>11</jdk.version>
    <springboot.version>2.7.6</springboot.version>
</properties>
```

### 指定编译器插件

指定Java8编译，如果需要使用其他版本的 JDK，你只需要修改`<source>`和`<target>`标签的值即可。例如，使用 Java11，你可以将它们的值改为 11。

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.8.1</version>
      <configuration>
        <source>1.8</source>
        <target>1.8</target>
      </configuration>
    </plugin>
  </plugins>
</build>
```

### 依赖管理

在顶层 pom 文件中，通过标签 `dependencyManagement` 定义公共的依赖关系，这有助于避免冲突并确保所有模块使用相同版本的依赖项。

父模块配置  
```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.7.2</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

子模块配置

```xml
<dependencies>
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
  </dependency>
</dependencies>
```

### 依赖排除
一般在解决依赖冲突的时，都会优先保留高版本。因为大部分 jar 在升级的时候都会做到向下兼容

```xml
<dependencys>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <!-- 排除老版本jackson，存在高危漏洞-->
        <exclusions>
            <exclusion>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-databind</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    
    <!-- 引入新版本jackson-->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.17.2</version>
    </dependency>
</dependencys>
```

### 依赖范围

```xml
<dependencies>
    <!-- 在编译和运行时使用 -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>3.1.0</version>
        <scope>compile</scope>
    </dependency>
 
    <!-- 仅在测试时使用 -->
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.12</version>
        <scope>test</scope>
    </dependency>
 
    <!-- 由JDK或容器提供 -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>3.1.0</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

Maven 的依赖范围如下：

- **compile**：编译依赖范围（默认），使用此依赖范围对于编译、测试、运行三种都有效，即在编译、测试和运行的时候都要使用该依赖 Jar 包。
- **test**：测试依赖范围，从字面意思就可以知道此依赖范围只能用于测试，而在编译和运行项目时无法使用此类依赖，典型的是 JUnit，它只用于编译测试代码和运行测试代码的时候才需要。
- **provided**：此依赖范围，对于编译和测试有效，而对运行时无效。比如 `servlet-api.jar` 在 Tomcat 中已经提供了，我们只需要的是编译期提供而已。
- **runtime**：运行时依赖范围，对于测试和运行有效，但是在编译主代码时无效，典型的就是 JDBC 驱动实现。
- **system**：系统依赖范围，使用 system 范围的依赖时必须通过 systemPath 元素显示地指定依赖文件的路径，不依赖 Maven 仓库解析，所以可能会造成建构的不可移植。

#### 引入本地Jar包

1. 项目根路径下(pom文件同级)新建lib文件夹并放入需引入的jar包
2. pom.xml加入
    ```xml
    <dependency>
        <groupId>com.jd</groupId>
        <artifactId>jdlm</artifactId>
        <version>2.2</version>
        <scope>system</scope>
        <systemPath>${project.basedir}/lib/jd-cps-2.2.jar</systemPath>
    </dependency>
    ```
   注意点:
    - groupId：自定义
    - artifactId：自定义
    - version：自定义
    - scope：必须是system
    - systemPath：jar包的路径（idea编写的时候会有提示的）
3. 打包处理
    ```xml
    <build>
        <resources>
            <resource>
                <directory>${project.basedir}/lib</directory>
                <targetPath>BOOT-INF/lib/</targetPath>
            </resource>
            <resource>
                <directory>src/main/resources</directory>
            </resource>
        </resources>
    </build>
    ```

### 多模块管理
这里以Blog项目为例

#### 父模块
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.3.4.RELEASE</version>
	</parent>
	<packaging>pom</packaging>
	<groupId>com.czndata.blog</groupId>
	<artifactId>blog</artifactId>
	<version>${blog.version}</version>
	<name>blog</name>
	<description>my blog</description>

	<properties>
		<java.version>1.8</java.version>
        <blog.version>1.0.0</blog.version>
	</properties>

	<modules>
		<module>blog-mbg</module>
		<module>blog-service</module>
		<module>blog-admin</module>
		<module>blog-web</module>
    </modules>
</project>
```

#### 子模块

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.czndata.blog</groupId>
        <artifactId>blog</artifactId>
        <version>${blog.version}</version>
    </parent>

    <artifactId>blog-service</artifactId>
    <version>${blog.version}</version>
    <name>blog-service</name>
    <description>Demo project for Spring Boot</description>
</project>
```

## Maven Wrapper
Maven Wrapper是一个用于管理Maven版本的工具。它允许在项目中使用特定的Maven版本，而无需全局安装Maven。
通过使用Maven Wrapper，可以确保所有开发者在构建项目时都使用相同的Maven版本，从而避免因不同的Maven版本导致的构建差异和潜在的兼容性问题。

### 初始化mvnw文件

```shell
mvn -N wrapper:wrapper

# 指定maven版本
mvn -N wrapper:wrapper -Dmaven=3.9.5
```

```
├── .mvn 
│   └── wrapper 
│       ├── maven-wrapper.jar 
│       └── maven-wrapper.properties 
├── mvnw 
└── mvnw.cmd
```
- mvnw: Unix/Linux/macOS 系统上的 Maven Wrapper 启动脚本
- mvnw.cmd: 这是 Windows 系统上的 Maven Wrapper 启动脚本
- .mvn/wrapper/maven-wrapper.properties: 这个文件包含 Maven Wrapper 的配置信息，例如要使用的 Maven 版本和下载 URL
- .mvn/wrapper/maven-wrapper.jar: 这是 Maven Wrapper 的核心 JAR 文件，它负责确保使用正确的 Maven 版本

### 使用mvnw

#### 项目构建
```shell
./mvnw clean install
```

#### 修改Maven版本

在 maven-wrapper.properties 文件中，找到 distributionUrl 属性。这个属性定义了 Maven 分发的下载 URL

```shell
distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.5/apache-maven-3.9.5-bin.zip
```