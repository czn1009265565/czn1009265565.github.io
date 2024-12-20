# Java IO
`IO`全称`Input/Output`，即数据的传输

- 根据数据的流向可以分为: 输入流和输出流
- 根据数据格式可以分为: 字节流和字符流

## 字节流和字符流
首先要了解下字节与字符的定义，
字节是最基本的数据存储单位，所有的数据最终都需要转换为字节来进行存储和传输。
字符则是在字节的基础上进行组合和编码（例如ASCII、UTF-8、UTF-16）得到的更高级别的文本表示。
简而言之，字节是计算机语言，字符是人的语言。

- 字节流: 以字节为单位，读写数据的流，常用于读写二进制文件
- 字符流: 以字符为单位，读写数据的流，常用于读写文本文件

## Java抽象类

1. FileInputStream、FileOutputStream 读写字节流
2. FileReader、FileWriter 读写字符流
3. BufferedInputStream、BufferedOutputStream 字节缓冲流
4. BufferedReader、BufferedWriter 字符缓冲流
5. RandomAccessFile 随机访问流
6. ZipOutputStream 压缩流

## 字节流
这里以文件拷贝为例

```java
public class FileCopyTest {
    public static void streamCopy() {
        // 记录开始时间
        long start = System.currentTimeMillis();
        FileInputStream fis = null;
        FileOutputStream fos = null;
        try {
            fis = new FileInputStream("movie.mp4");
            fos = new FileOutputStream("movie2.mp4");
            int content;
            while ((content = fis.read()) != -1) {
                fos.write(content);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                // 流的关闭准则，先开后关，后开先关
                if (fos != null) {
                    fos.close();
                }
                if (fis != null) {
                    fis.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        // 记录结束时间
        long end = System.currentTimeMillis();
        System.out.println("使用普通流复制文件总耗时:" + (end - start) + " 毫秒");
    }

    public static void main(String[] args) {
        streamCopy();
    }
}
```

### 字节缓冲流
缓冲流的基本原理，是在创建流对象时，会创建一个内置的默认大小的缓冲区数组，通过缓冲区读写，减少系统IO次数，从而提高读写的效率。

```java
public class FileCopyTest {
    public static void bufferCopy() {
        // 记录开始时间
        long start = System.currentTimeMillis();
        BufferedInputStream bis = null;
        BufferedOutputStream bos = null;
        try {
            bis = new BufferedInputStream(new FileInputStream("movie.mp4"));
            bos = new BufferedOutputStream(new FileOutputStream("movie2.mp4"));
            int content;
            while ((content = bis.read()) != -1) {
                bos.write(content);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                // 流的关闭准则，先开后关，后开先关
                if (bos != null) {
                    bos.close();
                }
                if (bis != null) {
                    bis.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
        // 记录结束时间
        long end = System.currentTimeMillis();
        System.out.println("使用缓冲流复制文件总耗时:" + (end - start) + " 毫秒");
    }

    public static void main(String[] args) {
        bufferCopy();
    }
}
```