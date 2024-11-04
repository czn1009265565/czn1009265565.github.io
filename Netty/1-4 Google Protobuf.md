# Google Protobuf

## 简介
Protocol Buffers 是一种语言无关、平台无关、可扩展的序列化结构数据的方法，它可用于（数据）通信协议、数据存储等。
Protocol Buffers 是一种灵活，高效，自动化机制的结构数据序列化方法。可类比 XML，但是比 XML 更小（3 ~ 10倍）、更快（20 ~ 100倍）、更为简单。

## 数据类型

### 基本数据类型

- double
- float
- int32
- int64
- bool
- string

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

### 对象

```
message Role{
  int32 role_id = 1;
  string name = 2;
}

message User{
  Role role = 1;
}
```

## protoc

下载地址: https://github.com/protocolbuffers/protobuf/releases

配置Path环境变量，指定protoc.exe执行程序路径