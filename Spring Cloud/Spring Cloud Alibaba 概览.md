## Spring Cloud Alibaba 概览.md

Spring Cloud Alibaba 致力于提供微服务开发的一站式解决方案。此项目包含开发分布式应用服务的必需组件，方便开发者通过 Spring Cloud 编程模型轻松使用这些组件来开发分布式应用服务。


### 版本依赖关系

|Spring Cloud Alibaba Version |Spring Cloud Version |Spring Boot Version|
|---|---|---|
|2021.0.1.0|2021.0.1|2.6.3|
|2.2.7.RELEASE|Hoxton.SR12|2.3.12.RELEASE|
|2021.1|2020.0.1 |2.4.2|
|2.2.6.RELEASE|Hoxton.SR9|2.3.2.RELEASE|
|2.1.4.RELEASE|Greenwich.SR6|2.1.13.RELEASE|
|2.2.1.RELEASE|Hoxton.SR3|2.2.5.RELEASE|
|2.2.0.RELEASE|Hoxton.RELEASE|2.2.X.RELEASE|
|2.1.2.RELEASE|Greenwich|2.1.X.RELEASE|
|2.0.4.RELEASE(停止维护，建议升级)|Finchley|2.0.X.RELEASE|
|1.5.1.RELEASE(停止维护，建议升级)|Edgware|1.5.X.RELEASE|

### 依赖引入

```xml
<properties>
    <java.version>1.8</java.version>
    <spring-cloud.version>2021.0.1</spring-cloud.version>
    <spring-cloud-alibaba.version>2021.0.1.0</spring-cloud-alibaba.version>
</properties>

<dependencyManagement>
    <dependencies>
        <!-- Spring Cloud -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Spring Cloud Alibaba -->
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-alibaba-dependencies</artifactId>
            <version>${spring-cloud-alibaba.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 子项目简介
1. Nacos 服务注册发现、配置管理、服务管理
2. Sentinel 流量控制、熔断降级、系统负载保护
3. Seata 高性能微服务分布式事务解决方案