# Spring Boot MinIO

## 依赖配置

### 引入依赖

```xml
<dependency>
    <groupId>io.minio</groupId>
    <artifactId>minio</artifactId>
    <version>${minio.version}</version>
</dependency>
```

### application配置

```yml
minio:
  endpoint: http://localhost:9000
  access-key: Th2J1OIDP57yI8nD
  secret-key: byShZYUxHIqk0PIq4XUW0M3EFKIzh0IQ
  bucket-name: muxin
```

### MinioConfig

```java
@Configuration
public class MinioConfig {
    @Value("${minio.endpoint}")
    private String endpoint;

    @Value("${minio.access-key}")
    private String accessKey;

    @Value("${minio.secret-key}")
    private String secretKey;

    @Value("${minio.bucket-name}")
    private String bucketName;

    @Bean
    public MinioClient minioClient() {
        return MinioClient
                .builder()
                .endpoint(endpoint)
                .credentials(accessKey, secretKey)
                .build();
    }
}
```

## Service实现

### 接口定义

```java
public interface MinioService {
    /**
     * 获取上传文件前缀路径
     */
     String getBasisUrl();

    /**
     * 启动SpringBoot容器的时候初始化Bucket
     * 如果没有Bucket则创建
     * @throws Exception
     */
     void createBucket(String bucketName) throws Exception;

    /**
     *  判断Bucket是否存在，true：存在，false：不存在
     * @return
     * @throws Exception
     */
     boolean bucketExists(String bucketName) throws Exception;

    /**
     * 获得Bucket的策略
     * @param bucketName
     * @return
     * @throws Exception
     */
     String getBucketPolicy(String bucketName) throws Exception;

    /**
     * 获得所有Bucket列表
     * @return
     * @throws Exception
     */
     List<Bucket> getAllBuckets() throws Exception;

    /**
     * 根据bucketName获取其相关信息
     * @param bucketName
     * @return
     * @throws Exception
     */
     Optional<Bucket> getBucket(String bucketName) throws Exception;

    /**
     * 根据bucketName删除Bucket，true：删除成功； false：删除失败，文件或已不存在
     * @param bucketName
     * @throws Exception
     */
     void removeBucket(String bucketName) throws Exception;

    /**
     * 判断文件是否存在
     * @param bucketName 存储桶
     * @param objectName 文件名
     * @return
     */
     boolean isObjectExist(String bucketName, String objectName);

    /**
     * 判断文件夹是否存在
     * @param bucketName 存储桶
     * @param objectName 文件夹名称
     * @return
     */
     boolean isFolderExist(String bucketName, String objectName);

    /**
     * 根据文件前置查询文件
     * @param bucketName 存储桶
     * @param prefix 前缀
     * @param recursive 是否使用递归查询
     * @return MinioItem 列表
     * @throws Exception
     */
     List<Item> getAllObjectsByPrefix(String bucketName, String prefix, boolean recursive) throws Exception;

    /**
     * 获取文件流
     * @param bucketName 存储桶
     * @param objectName 文件名
     * @return 二进制流
     */
     InputStream getObject(String bucketName, String objectName) throws Exception;

    /**
     * 断点下载
     * @param bucketName 存储桶
     * @param objectName 文件名称
     * @param offset 起始字节的位置
     * @param length 要读取的长度
     * @return 二进制流
     */
     InputStream getObject(String bucketName, String objectName, long offset, long length) throws Exception;

    /**
     * 获取路径下文件列表
     * @param bucketName 存储桶
     * @param prefix 文件名称
     * @param recursive 是否递归查找，false：模拟文件夹结构查找
     * @return 二进制流
     */
     Iterable<Result<Item>> listObjects(String bucketName, String prefix, boolean recursive);

    /**
     * 使用MultipartFile进行文件上传
     * @param bucketName 存储桶
     * @param file 文件名
     * @param objectName 对象名
     * @param contentType 类型
     * @return
     * @throws Exception
     */
     ObjectWriteResponse uploadFile(String bucketName, MultipartFile file, String objectName, String contentType) throws Exception;

    /**
     * 上传本地文件
     * @param bucketName 存储桶
     * @param objectName 对象名称
     * @param fileName 本地文件路径
     */
     ObjectWriteResponse uploadFile(String bucketName, String objectName, String fileName) throws Exception;

    /**
     * 通过流上传文件
     *
     * @param bucketName 存储桶
     * @param objectName 文件对象
     * @param inputStream 文件流
     */
     ObjectWriteResponse uploadFile(String bucketName, String objectName, InputStream inputStream) throws Exception;

    /**
     * 创建文件夹或目录
     * @param bucketName 存储桶
     * @param objectName 目录路径
     */
     ObjectWriteResponse createDir(String bucketName, String objectName) throws Exception;

    /**
     * 获取文件信息, 如果抛出异常则说明文件不存在
     *
     * @param bucketName 存储桶
     * @param objectName 文件名称
     */
     String getFileStatusInfo(String bucketName, String objectName) throws Exception;

    /**
     * 拷贝文件
     *
     * @param bucketName 存储桶
     * @param objectName 文件名
     * @param srcBucketName 目标存储桶
     * @param srcObjectName 目标文件名
     */
     ObjectWriteResponse copyFile(String bucketName, String objectName, String srcBucketName, String srcObjectName) throws Exception;

    /**
     * 删除文件
     * @param bucketName 存储桶
     * @param objectName 文件名称
     */
     void removeFile(String bucketName, String objectName) throws Exception;

    /**
     * 批量删除文件
     * @param bucketName 存储桶
     * @param keys 需要删除的文件列表
     * @return
     */
     void removeFiles(String bucketName, List<String> keys);

    /**
     * 获取文件外链
     * @param bucketName 存储桶
     * @param objectName 文件名
     * @param expires 过期时间 <=7 秒 （外链有效时间（单位：秒））
     * @return url
     * @throws Exception
     */
     String getPresignedObjectUrl(String bucketName, String objectName, Integer expires) throws Exception;

    /**
     * 获得文件外链
     * @param bucketName
     * @param objectName
     * @return url
     * @throws Exception
     */
     String getPresignedObjectUrl(String bucketName, String objectName) throws Exception;

    /**
     * 将URLDecoder编码转成UTF8
     * @param str
     * @return
     * @throws UnsupportedEncodingException
     */
     String getUtf8ByURLDecoder(String str) throws UnsupportedEncodingException;
}

```

### 实现类

```java
@Slf4j
@Service
public class MinioServiceImpl implements MinioService {

    public static final String SEPARATOR = "/";

    @Value("${minio.endpoint}")
    private String endpoint;

    @Value("${minio.bucket-name}")
    private String bucketName;

    @Resource
    private MinioClient minioClient;


    public String getBasisUrl() {
        return endpoint + SEPARATOR + bucketName + SEPARATOR;
    }

    public void createBucket(String bucketName) throws Exception {
        if (!bucketExists(bucketName)) {
            minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucketName).build());
        }
    }

    public boolean bucketExists(String bucketName) throws Exception {
        return minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
    }

    public String getBucketPolicy(String bucketName) throws Exception {
        return minioClient
                .getBucketPolicy(
                        GetBucketPolicyArgs
                                .builder()
                                .bucket(bucketName)
                                .build()
                );
    }

    public List<Bucket> getAllBuckets() throws Exception {
        return minioClient.listBuckets();
    }

    public Optional<Bucket> getBucket(String bucketName) throws Exception {
        return getAllBuckets().stream().filter(b -> b.name().equals(bucketName)).findFirst();
    }

    public void removeBucket(String bucketName) throws Exception {
        minioClient.removeBucket(RemoveBucketArgs.builder().bucket(bucketName).build());
    }

    public boolean isObjectExist(String bucketName, String objectName) {
        boolean exist = true;
        try {
            minioClient.statObject(StatObjectArgs.builder().bucket(bucketName).object(objectName).build());
        } catch (Exception e) {
            log.error("[Minio工具类]>>>> 判断文件是否存在, 异常：", e);
            exist = false;
        }
        return exist;
    }

    public boolean isFolderExist(String bucketName, String objectName) {
        boolean exist = false;
        try {
            Iterable<Result<Item>> results = minioClient.listObjects(
                    ListObjectsArgs.builder().bucket(bucketName).prefix(objectName).recursive(false).build());
            for (Result<Item> result : results) {
                Item item = result.get();
                if (item.isDir() && objectName.equals(item.objectName())) {
                    exist = true;
                }
            }
        } catch (Exception e) {
            log.error("[Minio工具类]>>>> 判断文件夹是否存在，异常：", e);
            exist = false;
        }
        return exist;
    }

    public List<Item> getAllObjectsByPrefix(String bucketName, String prefix, boolean recursive) throws Exception {
        List<Item> list = new ArrayList<>();
        Iterable<Result<Item>> objectsIterator = minioClient.listObjects(
                ListObjectsArgs.builder().bucket(bucketName).prefix(prefix).recursive(recursive).build());
        if (objectsIterator != null) {
            for (Result<Item> o : objectsIterator) {
                Item item = o.get();
                list.add(item);
            }
        }
        return list;
    }

    public InputStream getObject(String bucketName, String objectName) throws Exception {
        return minioClient.getObject(GetObjectArgs.builder().bucket(bucketName).object(objectName).build());
    }

    public InputStream getObject(String bucketName, String objectName, long offset, long length) throws Exception {
        return minioClient.getObject(
                GetObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .offset(offset)
                        .length(length)
                        .build());
    }

    public Iterable<Result<Item>> listObjects(String bucketName, String prefix, boolean recursive) {
        return minioClient.listObjects(
                ListObjectsArgs.builder()
                        .bucket(bucketName)
                        .prefix(prefix)
                        .recursive(recursive)
                        .build());
    }

    public ObjectWriteResponse uploadFile(String bucketName, MultipartFile file, String objectName, String contentType) throws Exception {
        InputStream inputStream = file.getInputStream();
        return minioClient.putObject(
                PutObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .contentType(contentType)
                        .stream(inputStream, inputStream.available(), -1)
                        .build());
    }

    public ObjectWriteResponse uploadFile(String bucketName, String objectName, String fileName) throws Exception {
        return minioClient.uploadObject(
                UploadObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .filename(fileName)
                        .build());
    }

    public ObjectWriteResponse uploadFile(String bucketName, String objectName, InputStream inputStream) throws Exception {
        return minioClient.putObject(
                PutObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .stream(inputStream, inputStream.available(), -1)
                        .build());
    }

    public ObjectWriteResponse createDir(String bucketName, String objectName) throws Exception {
        return minioClient.putObject(
                PutObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .stream(new ByteArrayInputStream(new byte[]{}), 0, -1)
                        .build());
    }

    public String getFileStatusInfo(String bucketName, String objectName) throws Exception {
        return minioClient.statObject(
                StatObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .build()).toString();
    }

    public ObjectWriteResponse copyFile(String bucketName, String objectName, String srcBucketName, String srcObjectName) throws Exception {
        return minioClient.copyObject(
                CopyObjectArgs.builder()
                        .source(CopySource.builder().bucket(bucketName).object(objectName).build())
                        .bucket(srcBucketName)
                        .object(srcObjectName)
                        .build());
    }

    public void removeFile(String bucketName, String objectName) throws Exception {
        minioClient.removeObject(
                RemoveObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .build());
    }

    public void removeFiles(String bucketName, List<String> keys) {
        List<DeleteObject> objects = new LinkedList<>();
        keys.forEach(s -> {
            objects.add(new DeleteObject(s));
            try {
                removeFile(bucketName, s);
            } catch (Exception e) {
                log.error("[Minio工具类]>>>> 批量删除文件，异常：", e);
            }
        });
    }

    public String getPresignedObjectUrl(String bucketName, String objectName, Integer expires) throws Exception {
        GetPresignedObjectUrlArgs args = GetPresignedObjectUrlArgs.builder()
                .expiry(expires)
                .bucket(bucketName)
                .object(objectName)
                .method(Method.GET)
                .build();
        return minioClient.getPresignedObjectUrl(args);
    }

    public String getPresignedObjectUrl(String bucketName, String objectName) throws Exception {
        GetPresignedObjectUrlArgs args = GetPresignedObjectUrlArgs.builder()
                .bucket(bucketName)
                .object(objectName)
                .method(Method.GET).build();
        return minioClient.getPresignedObjectUrl(args);
    }

    public String getUtf8ByURLDecoder(String str) throws UnsupportedEncodingException {
        String url = str.replaceAll("%(?![0-9a-fA-F]{2})", "%25");
        return URLDecoder.decode(url, StandardCharsets.UTF_8);
    }
}

```