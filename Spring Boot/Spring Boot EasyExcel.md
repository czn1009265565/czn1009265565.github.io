## Spring Boot EasyExcel

### 引入依赖

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

<dependency>
    <groupId>cn.hutool</groupId>
    <artifactId>hutool-all</artifactId>
    <version>5.8.20</version>
</dependency>
```

### 工具类

```java
public class ExcelUtils {

    /**
     * 将列表以 Excel 响应给前端
     *
     * @param response 响应
     * @param filename 文件名
     * @param sheetName Excel sheet 名
     * @param head Excel head 头
     * @param data 数据列表哦
     * @param <T> 泛型，保证 head 和 data 类型的一致性
     * @throws IOException 写入失败的情况
     */
    public static <T> void write(HttpServletResponse response, String filename, String sheetName,
                                 Class<T> head, List<T> data) throws IOException {

        // 设置 header 和 contentType。写在最后的原因是，避免报错时，响应 contentType 已经被修改了
        response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode(filename, "UTF-8"));
        response.setContentType("application/vnd.ms-excel;charset=UTF-8");
        // 输出 Excel
        EasyExcel.write(response.getOutputStream(), head)
                .autoCloseStream(false) // 不要自动关闭，交给 Servlet 自己处理
                .registerWriteHandler(new LongestMatchColumnWidthStyleStrategy()) // 基于 column 长度，自动适配。最大 255 宽度
                .sheet(sheetName).doWrite(data);
    }

    public static <T> List<T> read(MultipartFile file, Class<T> head) throws IOException {
        return EasyExcel.read(file.getInputStream(), head, null)
                .autoCloseStream(false)  // 不要自动关闭，交给 Servlet 自己处理
                .doReadAllSync();
    }
}
```

### 导入导出实例

#### 实体类

```java
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserImportExcelVO {

    @ExcelProperty("登录名称")
    private String username;

    @ExcelProperty("用户名称")
    private String nickname;

    @ExcelProperty("部门编号")
    private Long deptId;

    @ExcelProperty("用户邮箱")
    private String email;

    @ExcelProperty("手机号码")
    private String mobile;

    @ExcelProperty(value = "用户性别", converter = DictConvert.class)
    @DictFormat(value = "sex")
    private Integer sex;
}
```

#### 字典转换注解

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
public @interface DictFormat {

    /**
     * 例如说，SysDictTypeConstants、InfDictTypeConstants
     *
     * @return 字典类型
     */
    String value();

}
```

#### 字典转换类

```java
@Slf4j
public class DictConvert implements Converter<Object> {
    // 生产环境查询字典表
    public static Map<String, Map<String, String>> LableMap = Collections.singletonMap("sex", Collections.singletonMap("男", "1"));
    public static Map<String, Map<String, String>> valueMap = Collections.singletonMap("sex", Collections.singletonMap("1", "男"));

    @Override
    public Class<?> supportJavaTypeKey() {
        throw new UnsupportedOperationException("暂不支持，也不需要");
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        throw new UnsupportedOperationException("暂不支持，也不需要");
    }

    @Override
    public Object convertToJavaData(ReadCellData readCellData, ExcelContentProperty contentProperty,
                                    GlobalConfiguration globalConfiguration) {


        // 使用字典解析
        String type = getType(contentProperty);
        String label = readCellData.getStringValue();
        String value = LableMap.getOrDefault(type, Collections.emptyMap()).get(label);
        if (value == null) {
            log.error("[convertToJavaData][type({}) 解析异常 label({})]", type, label);
            return null;
        }
        // 将 String 的 value 转换成对应的属性
        Class<?> fieldClazz = contentProperty.getField().getType();
        return Convert.convert(fieldClazz, value);
    }

    @Override
    public WriteCellData<String> convertToExcelData(Object object, ExcelContentProperty contentProperty,
                                                    GlobalConfiguration globalConfiguration) {
        // 空时，返回空
        if (object == null) {
            return new WriteCellData<>("");
        }

        // 使用字典格式化
        String type = getType(contentProperty);
        String value = String.valueOf(object);
        String label = valueMap.getOrDefault(type, Collections.emptyMap()).get(value);
        if (label == null) {
            log.error("[convertToExcelData][type({}) 转换异常 label({})]", type, value);
            return new WriteCellData<>("");
        }
        // 生成 Excel 小表格
        return new WriteCellData<>(label);
    }

    private static String getType(ExcelContentProperty contentProperty) {
        return contentProperty.getField().getAnnotation(DictFormat.class).value();
    }
}
```

#### Controller

```java
@RestController
@RequestMapping(value = "excel")
public class ExcelController {

    @PostMapping(value = "read")
    public String read(UserImportForm userImportForm) throws IOException {
        List<UserImportExcelVO> userImportExcelVOList = ExcelUtils.read(userImportForm.getFile(), UserImportExcelVO.class);
        return "success";
    }

    @GetMapping(value = "write")
    public void write(HttpServletResponse response) throws IOException {
        UserImportExcelVO build = UserImportExcelVO.builder()
                .username("admin")
                .nickname("admin")
                .deptId(1L)
                .email("@")
                .mobile("10086")
                .sex(1)
                .build();
        ExcelUtils.write(response, "用户导入模板.xls", "用户列表", UserImportExcelVO.class, Collections.singletonList(build));
    }
}
```