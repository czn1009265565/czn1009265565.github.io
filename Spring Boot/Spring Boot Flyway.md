# Spring Boot Flyway

Flyway是一个开源的数据库迁移框架,可以帮助开发人员自动化管理数据库结构和预置数据的变更,减少手动数据迁移,从而提高开发效率和数据库管理的可靠性

## Flyway规则

Flyway 将 SQL 文件分为 `Versioned` 、`Repeatable` 和 `Undo`

- Versioned 用于版本升级，每个版本有唯一的版本号并只能执行一次，命名规则 `V1.0.0__create_user.sql`
- Repeatable 可重复执行，当 Flyway 检测到 Repeatable 类型的 SQL 脚本的有变动，Flyway 就会重新执行该脚本，它并不用于版本更新，这类的 migration 总是在 Versioned 执行之后才被执行
- Undo 用于撤销具有相同版本的版本化迁移带来的影响

1. `Prefix` 可配置，前缀标识，默认值 `V` 表示 `Versioned`， `R` 表示 `Repeatable`， `U` 表示 `Undo`
2. `Version` 标识版本号, 由一个或多个数字构成，数字之间的分隔符可用点 `.` 或下划线 `_`
3. `Separator` 可配置，用于分隔版本标识与描述信息，默认为两个下划线 `__`
4. `Description` 描述信息，文字之间可以用下划线 `_` 或空格` `分隔。
5. `Suffix` 可配置，后续标识，默认为 `.sql`

## Spring Boot Flyway
### 引入依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>

    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
    </dependency>
</dependencies>
```

### application配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/db_test
    username: root
    password: root
    driver-class-name: org.postgresql.Driver

  # 启动flyway migration, 默认为true
  flyway:
    enabled: true
    # SQL 脚本的目录,多个路径使用逗号分隔 默认值 classpath:db/migration
    locations: classpath:db/migration
    #  metadata 版本控制历史表 默认 flyway_schema_history
    table: flyway_schema_history
    # 如果没有 flyway_schema_history 这个 metadata 表， 在执行 flyway migrate 命令之前, 必须先执行 flyway baseline 命令
    # 设置为 true 后 flyway 将在需要 baseline 的时候, 自动执行一次 baseline。
    baseline-on-migrate: true
```

### 创建初始化表

- V1.0.0_1__create_user.sql
- V1.0.0_2__create_role.sql
- R__init_data.sql
