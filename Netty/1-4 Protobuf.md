# Protobuf

## 简介
Protocol Buffers 是一种语言无关、平台无关、可扩展的序列化结构数据的方法，它可用于（数据）通信协议、数据存储等。
Protocol Buffers 是一种灵活，高效，自动化机制的结构数据序列化方法。可类比 XML，但是比 XML 更小（3 ~ 10倍）、更快（20 ~ 100倍）、更为简单。

## 数据类型

### 基本数据类型

| ProtoBuf类型 | 	Java类型 |
|------------|---------|
| int32      | 	int    |
| int64	     | long    |
| float	     | float   |
| double	    | double  |
| bool	      | boolean |
| string     | 	String |

默认值:  
- string: 默认为空字符串
- byte: 默认值为空字节
- bool: 默认为false
- 数值: 默认为0
- enum: 默认为第一个元素

### List

```protobuf
message User{
  repeated int32 int_list = 1;
  repeated string string_list = 2;
}
```

### Map

```protobuf
message User{
  map<string, string> string_map = 1;
}
```

### 对象及枚举

```
message User{
  Role role = 1;
  SexEnum sex = 2;
}

message Role{
  int32 role_id = 1;
  string name = 2;
}

enum SexEnum{
  SEX_MAN = 0;
  SEX_WOMAN= 1;
}
```

## Java 集成

### protoc 编译器

下载地址: https://github.com/protocolbuffers/protobuf/releases

配置Path环境变量，查看对应版本  
```shell
# 查看版本
protoc --version
```

### 定义Protobuf

```protobuf
syntax = "proto3";
// 表示生成的Java序列化器包路径
option java_package = "com.czndata.proto";
// 表示生成的Java序列化器类名
option java_outer_classname = "UserProfileFactory";


message UserProfile {
  int64 id = 1;
  string name = 2;
}

```

### 引入依赖

```xml
<dependency>
    <groupId>com.google.protobuf</groupId>
    <artifactId>protobuf-java</artifactId>
    <version>4.29.0-RC2</version>
</dependency>
```

这里引入的依赖版本需要与下载的ProtoBuf编译器版本保持一致，否则会报错

### 序列化与反序列化

```java
public class TestApplication {
    public static void main(String[] args) throws InvalidProtocolBufferException {
        // 创建对象
        UserProfileFactory.UserProfile userProfile = UserProfileFactory.UserProfile.newBuilder()
                .setId(1L)
                .setName("Tom")
                .build();
        // 序列化
        byte[] byteArray = userProfile.toByteArray();

        // 反序列化
        UserProfileFactory.UserProfile userProfileRes = UserProfileFactory.UserProfile.parseFrom(byteArray);
    }
}
```