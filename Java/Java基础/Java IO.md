# Java IO
数据的传输可以看做是一种数据的流动，按照流动的方向，以内存为基准，分为输入input 和输出output ，即流向内存是输入流，流出内存的输出流。

## 抽象类

1. File
2. FileInputStream、FileOutputStream 读写字节流
3. BufferedInputStream、BufferedOutputStream 字节缓冲流
4. FileReader、FileWriter 读写字符流
5. BufferedReader、BufferedWriter 字符缓冲流
6. RandomAccessFile 随机访问流
7. ZipOutputStream 压缩流

### File与FileInputStream区别

- File类实现的方法:getName,getParent,exists,isDirectory,isFilede,list等，关注的是文件在磁盘上的存储，File 不属于文件流，只能代表文件名和目录路径名

- FileInputStream实现的方法:read,close等，关注的是文件内容

### FileInputStream与FileReader区别

FileInputStream：以字节流方式读取

FileReader：把文件转换为字符流读入

### 缓冲流的作用

IO 操作是很消耗性能的，缓冲流将数据加载至缓冲区，一次性读取/写入多个字节，从而避免频繁的 IO 操作，提高流的传输效率。

```java
public class FileUtils {

    public static void copy_pdf_to_another_pdf_stream() {
        // 记录开始时间
        long start = System.currentTimeMillis();
        try (FileInputStream fis = new FileInputStream("深入理解计算机操作系统.pdf");
             FileOutputStream fos = new FileOutputStream("深入理解计算机操作系统-副本.pdf")) {
            int content;
            while ((content = fis.read()) != -1) {
                fos.write(content);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        // 记录结束时间
        long end = System.currentTimeMillis();
        System.out.println("使用普通流复制PDF文件总耗时:" + (end - start) + " 毫秒");
    }

    public static void copy_pdf_to_another_pdf_buffer_stream() {
        // 记录开始时间
        long start = System.currentTimeMillis();
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream("深入理解计算机操作系统.pdf"));
             BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("深入理解计算机操作系统-副本.pdf"))) {
            int content;
            while ((content = bis.read()) != -1) {
                bos.write(content);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        // 记录结束时间
        long end = System.currentTimeMillis();
        System.out.println("使用缓冲流复制PDF文件总耗时:" + (end - start) + " 毫秒");
    }
}
```

### RandomAccessFile

这里要介绍的随机访问流指的是支持随意跳转到文件的任意位置进行读写的 RandomAccessFile。

RandomAccessFile 的构造方法如下，我们可以指定 mode（读写模式）。


RandomAccessFile 可以帮助我们合并文件分片，示例代码如下：

```java
public class FileUtils {
    public boolean merge(String fileName) throws IOException {
        byte[] buffer = new byte[1024 * 10];
        int len = -1;
        try (RandomAccessFile saveFile = new RandomAccessFile(fileName, "rw")) {
            for (int i = 0; i < DOWNLOAD_BATCH_SIZE; i++) {
                try (BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream(fileName + FILE_TEMP_SUFFIX + i))) {
                    // 读到文件末尾则返回-1
                    while ((len = bufferedInputStream.read(buffer)) != -1) {
                        // 追加
                        saveFile.write(buffer, 0, len);
                    }
                }
            }
            log.info("文件合并完成 {}", fileName);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return true;
    }
}
```