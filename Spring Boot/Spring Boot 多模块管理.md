## Spring Boot 多模块管理

在项目开发过程中,将项目划分成多个模块或者微服务，能够有效降低系统复杂度。

### 模块划分

以商城项目划分为例:

```
mall
├── mall-common -- 工具类及通用代码模块
├── mall-mbg -- MyBatisGenerator生成的数据库操作代码模块
├── mall-auth -- 基于Spring Security Oauth2的统一的认证中心
├── mall-gateway -- 基于Spring Cloud Gateway的微服务API网关服务
├── mall-monitor -- 基于Spring Boot Admin的微服务监控中心
├── mall-admin -- 后台管理系统服务
├── mall-search -- 基于Elasticsearch的商品搜索系统服务
└── mall-portal -- 移动端商城系统服务
```

### 父模块

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>mall</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>mall-common</module>
        <module>mall-mbg</module>
        <module>mall-admin</module>
        <module>mall-search</module>
        <module>mall-portal</module>
        <module>mall-monitor</module>
        <module>mall-gateway</module>
        <module>mall-auth</module>
    </modules>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.0.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

</project>
```

子模块中的版本依赖，可以统一在父模块中properties标签中配置

### 子模块

以common模块为例,配置如下

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.example</groupId>
        <artifactId>mall</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <groupId>org.example</groupId>
    <artifactId>mall-common</artifactId>
    <version>1.0-SNAPSHOT</version>
    <name>mall-common</name>
    <description>mall-common</description>
    <properties>
        <java.version>1.8</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

### 开发中遇到的问题

1. 跨模块Bean的扫描
    
```
@SpringBootApplication(scanBasePackages = {"org.example"})
@SpringBootApplication(scanBasePackages = {"org.example.module-a", "org.example.module-b"})
```
   
2. MyBatis 跨模块 Mapper、Dao扫描配置
   
```yaml
mybatis:
  configuration:
    # 控制台日志配置,打出执行的sql语句
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  mapper-locations: classpath*:mapper/*.xml
```

```
// JavaBean Dao层扫描配置
@MapperScan("com.springboot.mbg.dao")
```