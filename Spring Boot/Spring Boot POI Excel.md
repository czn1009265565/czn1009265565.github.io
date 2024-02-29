## Spring Boot POI Excel

### 依赖配置

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.2</version>
</dependency>

<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.2</version>
</dependency>
```


### 自定义商品实体类
```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Product {
    private Long productId;
    private String title;
    private String description;
    private Double originalPrice;
    private Double currentPrice;
}
```

### 实现转换方法

```java
public class POIUtils {
    public static final String SHEET_NAME = "product";

    /**
     * 写入Excel
     */
    public static XSSFWorkbook product2Excel(List<Product> productList) {
        XSSFWorkbook workbook = new XSSFWorkbook();
        XSSFSheet sheet = workbook.createSheet(SHEET_NAME);

        // 创建表名
        XSSFRow r0 = sheet.createRow(0);
        r0.createCell(0).setCellValue("SHEET_NAME");
        // 合并单元格
        CellRangeAddress cellAddresses = new CellRangeAddress(0, 0, 0, 4);
        sheet.addMergedRegion(cellAddresses);

        // 创建表头
        XSSFRow r1 = sheet.createRow(1);
        r1.createCell(0).setCellValue("商品ID");
        r1.createCell(1).setCellValue("名称");
        r1.createCell(2).setCellValue("描述");
        r1.createCell(3).setCellValue("原价");
        r1.createCell(4).setCellValue("现价");
        // 写入行数据
        for (int i = 0; i < productList.size(); i++) {
            XSSFRow rn = sheet.createRow(i + 2);
            Product product = productList.get(i);
            rn.createCell(0).setCellValue(product.getProductId());
            rn.createCell(1).setCellValue(product.getTitle());
            rn.createCell(2).setCellValue(product.getDescription());
            rn.createCell(3).setCellValue(product.getOriginalPrice());
            rn.createCell(4).setCellValue(product.getCurrentPrice());
        }

        return workbook;
    }

    /**
     * Excel 转换为 Http返回对象 ResponseEntity
     */
    public static ResponseEntity<byte[]> excel2ResponseEntity(XSSFWorkbook workbook, String filename) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        HttpHeaders headers = new HttpHeaders();
        try {
            headers.setContentDispositionFormData("attachment", new String(filename.getBytes(StandardCharsets.UTF_8), StandardCharsets.ISO_8859_1));
            headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
            workbook.write(baos);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>(baos.toByteArray(), headers, HttpStatus.CREATED);
    }

    /**
     * Excel解析
     */
    public static List<Product> excel2Product(MultipartFile file) throws IOException {
//        FileInputStream inputStream = new FileInputStream( PATH + "template.xlsx");
        Workbook workbook = WorkbookFactory.create(file.getInputStream());
        // 获取Sheet表
        Sheet sheet1 = workbook.getSheetAt(0);
        // 获取标题行
        Row rowTitle = sheet1.getRow(0);
        // 获取行数
        int rowCount = sheet1.getPhysicalNumberOfRows();
        // 循环读取列行，第1行一般是标题，所以要从第二行开始读，rowNum从1开始
        List<Product> productList = new ArrayList<>();
        for (int rowNum=1; rowNum<rowCount; rowNum++){
            Row rowData = sheet1.getRow(rowNum);
            if (Objects.isNull(rowData)) continue;
//            int cellCount = rowTitle.getPhysicalNumberOfCells();
            long productId = (long) rowData.getCell(0).getNumericCellValue();
            String title = rowData.getCell(1).getStringCellValue();
            String desc = rowData.getCell(2).getStringCellValue();
            double originPrice = rowData.getCell(3).getNumericCellValue();
            double currentPrice = rowData.getCell(4).getNumericCellValue();
            Product product = new Product(productId, title, desc, originPrice, currentPrice);
            productList.add(product);
        }
        return productList;
    }

     /**
     * 判断是否合并单元格
     * 1. 非合并单元格 正常获取
     * 2. 合并单元格 获取合并单元格的值
     */
    public static boolean isMergedRegionValue(Sheet sheet,int row ,int column) {
        int sheetMergeCount = sheet.getNumMergedRegions();
        for (int i = 0; i < sheetMergeCount; i++) {
            CellRangeAddress range = sheet.getMergedRegion(i);
            int firstColumn = range.getFirstColumn();
            int lastColumn = range.getLastColumn();
            int firstRow = range.getFirstRow();
            int lastRow = range.getLastRow();
            if(row >= firstRow && row <= lastRow){
                if(column >= firstColumn && column <= lastColumn){
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * 获取单元格的值
     * 1. 非合并单元格 正常获取
     * 2. 合并单元格 获取合并单元格的值
     */
    public static String getMergedRegionValue(Sheet sheet,int row ,int column) {
        int sheetMergeCount = sheet.getNumMergedRegions();
        for (int i = 0; i < sheetMergeCount; i++) {
            CellRangeAddress range = sheet.getMergedRegion(i);
            int firstColumn = range.getFirstColumn();
            int lastColumn = range.getLastColumn();
            int firstRow = range.getFirstRow();
            int lastRow = range.getLastRow();
            if(row >= firstRow && row <= lastRow){
                if(column >= firstColumn && column <= lastColumn){
                    return sheet.getRow(firstRow).getCell(firstColumn).getStringCellValue();
                }
            }
        }
        return sheet.getRow(row).getCell(column).getStringCellValue();
    }
}
```


