# MapStruct

## 需求介绍
Car是数据库映射类,CarDTO是我们的数据传输层，我们需要将从数据库查到的Car转换成CarDTO返回。

我们通常的做法是通过get、set方法，但是这样的代码往往很不美观，
当然我们也可以通过BeanUtils.copyProperties方法,但依旧存在一个问题，
属性字段名称略微不一致就无法完成数据的转换。mapstruct正是为了解决这样的问题。

### 依赖配置

[版本查看](https://github.com/mapstruct/mapstruct)
```
<properties>
    <org.mapstruct.version>1.5.5.Final</org.mapstruct.version>
</properties>

<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>${org.mapstruct.version}</version>
</dependency>

<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct-processor</artifactId>
    <version>${org.mapstruct.version}</version>
</dependency>
```


### 基本用法
1. 不同字段名称映射
```java
@Mapper
public interface CarConvertMapper {
    CarConvertMapper INSTANCE = Mappers.getMapper(CarConvertMapper.class);

    @Mapping(source = "seat", target = "seatNum")
    CarDTO entityToDto(Car car);
}
```

2. 集合
```java
@Mapper
public interface CarConvertMapper {
    CarConvertMapper INSTANCE = Mappers.getMapper(CarConvertMapper.class);

    @Mapping(expression = "java((long) map.get(\"id\"))", target = "id")
    @Mapping(expression = "java((int) map.get(\"seat\"))", target = "seat")
    @Mapping(expression = "java(String.valueOf(map.get(\"brand\")))", target = "brand")
    Car mapToCar(Map<String, Object> map);
}
```
3. 指定类型转换

自定义实现默认特定类型转换，可实现复用

```java
public interface BaseMapper {
   default LocalDateTime date2LocalDateTime(Date date) {
       if (date == null) return null;
       return date.toInstant()
           .atZone(ZoneId.systemDefault())
           .toLocalDateTime();
   }

   default Date localDateTime2Date(LocalDateTime localDateTime) {
       if (localDateTime == null) return null;
       return Date.from(localDateTime.atZone(ZoneId.systemDefault()).toInstant());
   }
}
```
继承BaseMapper即可

这里有几个注意点：

1. `@Mapper`注解和Mybatis区分
2. 之前采用Github官方配置与lombok存在编译顺序问题，删除官方plugin即可