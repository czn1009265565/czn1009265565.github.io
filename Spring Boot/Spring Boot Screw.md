## Spring Boot Screw


### MySQL
新增maven插件配置

```xml
<plugin>
	<groupId>cn.smallbun.screw</groupId>
	<artifactId>screw-maven-plugin</artifactId>
	<version>1.0.5</version>
	<dependencies>
		<!-- HikariCP -->
		<dependency>
			<groupId>com.zaxxer</groupId>
			<artifactId>HikariCP</artifactId>
			<version>4.0.3</version>
		</dependency>
		<!--mysql driver-->
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>8.0.20</version>
		</dependency>
	</dependencies>
	<configuration>
		<!--username-->
		<username>root</username>
		<!--password-->
		<password>root</password>
		<!--driver-->
		<driverClassName>com.mysql.cj.jdbc.Driver</driverClassName>
		<!--jdbc url-->
		<jdbcUrl>jdbc:mysql://127.0.0.1:3306/dbname?serverTimezone=UTC</jdbcUrl>
        <!-- 指定生成表前缀 -->
        <designatedTablePrefix>
            <value>tb_product</value>
            <value>tb_user</value>
        </designatedTablePrefix>
        <!-- 忽略表前缀 -->
        <ignoreTablePrefix>
            <value>tb_system</value>
        </ignoreTablePrefix>
		<!--生成文件类型：三种类型，直接修改 HTML MD WORD-->
		<fileType>WORD</fileType>
		<!--打开文件输出目录-->
		<openOutputDir>false</openOutputDir>
		<!--生成模板-->
		<produceType>freemarker</produceType>
		<!--描述-->
		<description>数据库文档生成</description>
		<!--版本-->
		<version>${project.version}</version>
		<!--标题-->
		<title>数据库文档</title>
	</configuration>
	<executions>
		<execution>
			<phase>compile</phase>
			<goals>
				<goal>run</goal>
			</goals>
		</execution>
	</executions>
</plugin>
```

执行mvn工程 `mvn screw:run` 即可生成数据库文档


### PostgreSQL

PostgreSQL生成数据库文档相较MySQL仅有依赖、配置改动

```xml
<plugin>
	<groupId>cn.smallbun.screw</groupId>
	<artifactId>screw-maven-plugin</artifactId>
	<version>1.0.5</version>
	<dependencies>
		<!-- HikariCP -->
		<dependency>
			<groupId>com.zaxxer</groupId>
			<artifactId>HikariCP</artifactId>
			<version>4.0.3</version>
		</dependency>
		<!--postgresql driver-->
		<dependency>
			<groupId>org.postgresql</groupId>
			<artifactId>postgresql</artifactId>
			<version>42.2.12</version>
		</dependency>
	</dependencies>
	<configuration>
		<!--username-->
		<username>postgres</username>
		<!--password-->
		<password>postgres</password>
		<!--driver-->
		<driverClassName>org.postgresql.Driver</driverClassName>
		<!--jdbc url-->
		<jdbcUrl>jdbc:postgresql://127.0.0.1:5432/dbname?allowMultiQueries=true</jdbcUrl>
        <!-- 指定生成表前缀 -->
        <designatedTablePrefix>
            <value>tb_product</value>
            <value>tb_user</value>
        </designatedTablePrefix>
        <!-- 忽略表前缀 -->
        <ignoreTablePrefix>
            <value>tb_system</value>
        </ignoreTablePrefix>
		<!--生成文件类型：三种类型，直接修改 HTML MD WORD-->
		<fileType>WORD</fileType>
		<!--打开文件输出目录-->
		<openOutputDir>false</openOutputDir>
		<!--生成模板-->
		<produceType>freemarker</produceType>
		<!--描述-->
		<description>数据库文档生成</description>
		<!--版本-->
		<version>${project.version}</version>
		<!--标题-->
		<title>数据库文档</title>
	</configuration>
	<executions>
		<execution>
			<phase>compile</phase>
			<goals>
				<goal>run</goal>
			</goals>
		</execution>
	</executions>
</plugin>
```

若出现生成失败问题,则可尝试修改对应MySQL、PostgreSQL Driver版本号
