# Maven 引入本地jar包

## 背景

接入支付宝、微信、京东等第三方jar包

## 步骤

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

build下新增

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