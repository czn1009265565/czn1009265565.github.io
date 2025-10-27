# Spring Boot EasyExcel
`EasyExcel` 是阿里巴巴开源的一个基于 `Java` 的、简单、省内存的读写 `Excel` 的开源工具。

推荐使用场景:  
- 大数据量 Excel 导入导出（万行以上）
- 内存敏感的环境
- Web 环境下的文件下载
- 需要高性能读写的业务场景

不适用场景(Apache POI):  
- 需要复杂 Excel 操作（如图表、公式等）
- 需要修改现有 Excel 模板的复杂场景
- 对样式有极高要求的场景


## 引入依赖
```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>easyexcel</artifactId>
    <version>3.3.2</version>
</dependency>

<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

## 核心注解

- `@ExcelProperty` 定义列名及排序
- `@ExcelIgnore` 忽略注释字段导入导出
- `@NumberFormat` 小数格式
- `@DateTimeFormat` 日期格式

## 定义实体类

```java
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserImportExcelVO {
    @ExcelProperty(value = "用户名", index=0)
    private String username;

    @ExcelProperty(value = "用户邮箱", index=1)
    private String email;

    @ExcelProperty(value = "手机号码", index=2)
    private String mobile;

    @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @ExcelProperty(value = "创建时间", converter = LocalDateTimeConverter.class, index = 3)
    private LocalDateTime createTime;
}
```

## 定义转换器

```java
public class LocalDateTimeConverter implements Converter<LocalDateTime> {
    private final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Override
    public Class<?> supportJavaTypeKey() {
        return LocalDateTime.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public LocalDateTime convertToJavaData(ReadConverterContext<?> context) {
        String stringValue = context.getReadCellData().getStringValue();
        return LocalDateTime.parse(stringValue, formatter);
    }

    @Override
    public WriteCellData<?> convertToExcelData(WriteConverterContext<LocalDateTime> context) {
        return new WriteCellData<>(context.getValue().format(formatter));
    }
}
```

## 写入Excel
### 写入实体类

```java
public static void entity() {
    UserImportExcelVO userImportExcelVO = UserImportExcelVO.builder()
            .username("admin")
            .email("admin@gmail.com")
            .mobile("123")
            .createTime(LocalDateTime.now())
            .build();
    List<UserImportExcelVO> userImportExcelVOList = Arrays.asList(userImportExcelVO);

    EasyExcel.write("fileName.xlsx")
            .head(UserImportExcelVO.class)
            .registerConverter(new LocalDateTimeConverter())
            .sheet("SheetName")
            .doWrite(userImportExcelVOList);
}
```

### 复杂表头

```java
public static void multipleHead() {
    List<List<String>> head = new ArrayList<>();

    head.add(Arrays.asList("用户基本信息", "用户名"));
    head.add(Arrays.asList("联系信息", "邮箱"));
    head.add(Arrays.asList("联系信息", "手机号"));
    head.add(Arrays.asList("时间", "创建时间"));
    // 数据
    List<List<Object>> data = new ArrayList<>();
    data.add(Arrays.asList("张三", "zhangsan@qq.com", "123", LocalDateTime.now()));
    data.add(Arrays.asList("李四", "lisi@qq.com", "123", LocalDateTime.now()));

    EasyExcel.write("fileName.xlsx")
            .head(head)
            .sheet("SheetName")
            .doWrite(data);
}
```

### 分批写入

```java
public static void batch() {
    ExcelWriter excelWriter = null;
    try {
        excelWriter = EasyExcel.write("fileName.xlsx")
                .build();
        WriteSheet writeSheet = EasyExcel.writerSheet("SheetName")
                .head(UserImportExcelVO.class)
                .build();
        // 总数与批处理数量
        int totalCount = 10;
        int batchSize = 1;
        for (int i = 0; i < totalCount; i += batchSize) {
            // 分页查询数据
            List<UserImportExcelVO> batchData = Collections.singletonList(UserImportExcelVO.builder()
                    .username("admin")
                    .email("admin@gmail.com")
                    .mobile("123")
                    .createTime(LocalDateTime.now())
                    .build());

            // 写入当前批次数据
            excelWriter.write(batchData, writeSheet);
            System.out.println("已写入第 " + ((i / batchSize) + 1) + " 批数据，共 " + batchData.size() + " 条");
        }
        System.out.println("导出完成");
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        if (excelWriter != null) {
            excelWriter.finish();
        }
    }
}
```

### 文件下载

```java
public static void download(HttpServletResponse response) {
    UserImportExcelVO userImportExcelVO = UserImportExcelVO
            .builder()
            .username("admin")
            .email("admin@gmail.com")
            .mobile("123")
            .createTime(LocalDateTime.now())
            .build();

    try {
        response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode("result.xlsx", "UTF-8"));
        response.setContentType("application/vnd.ms-excel;charset=UTF-8");
        EasyExcel.write(response.getOutputStream())
                .head(UserImportExcelVO.class)
                .autoCloseStream(false)
                .registerWriteHandler(new LongestMatchColumnWidthStyleStrategy())
                .sheet("SheetName")
                .doWrite(Collections.singletonList(userImportExcelVO));
    } catch (Exception e){
        e.printStackTrace();
    }
}
```

## 读取Excel

### 同步读取
适用于小文件

```java
public static List<UserImportExcelVO> syncRead() {
    String fileName = "input.xlsx";
    List<UserImportExcelVO> dataList = new ArrayList<>();
    try {
         dataList = EasyExcel.read(fileName)
                .head(UserImportExcelVO.class)
                .sheet()
                .doReadSync();
        System.out.println("同步读取数据量: " + dataList.size());
    } catch (Exception e) {
        e.printStackTrace();
        
    }
    return dataList;
}
```

### 使用监听器读取

自定义监听器
```java
/**
 * 监听器
 */
public class UserImportExcelVOListener extends AnalysisEventListener<UserImportExcelVO> {
    private static final int BATCH_COUNT = 1000;
    private List<UserImportExcelVO> dataList = new ArrayList<>();

    @Override
    public void invoke(UserImportExcelVO data, AnalysisContext context) {
        dataList.add(data);
        System.out.println("read data: " + data);
        // 大文件分批处理避免内存溢出
        if (dataList.size() >= BATCH_COUNT) {
            processBatchData();
            dataList.clear();
        }
    }

    @Override
    public void doAfterAllAnalysed(AnalysisContext context) {
        System.out.println("read complete，size: " + dataList.size());
    }

    public List<UserImportExcelVO> getDataList() {
        return dataList;
    }
    
    public void processBatchData() {
        // TODO 批处理数据
    }
}
```

数据读取
```java
public static List<UserImportExcelVO> listenerRead() {
    String fileName = "input.xlsx";
    List<UserImportExcelVO> result = new ArrayList<>();
    UserImportExcelVOListener listener = new UserImportExcelVOListener();
    try {
        EasyExcel.read(fileName, UserImportExcelVO.class, listener)
                .sheet()
                .doRead();

        result = listener.getDataList();
        System.out.println("last data size: " + result.size());
    } catch (Exception e) {
        e.printStackTrace();
    }
    return result;
}
```
