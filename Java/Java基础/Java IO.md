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

### 字节输入流

`java.io.InputStream` 抽象类是表示字节输入流的所有类的超类，可以读取字节信息到内存中。
它定义了字节输入流的基本共性功能方法

- `public void close()`: 关闭此输入流并释放与此流相关联的任何系统资源
- `public abstract int read()`: 从输入流读取数据的下一个字节
- `public int read(byte[] b)`: 从输入流中读取一些字节数，并将它们存储到字节数组b中

```java
public class FileInputStreamTest {
    public static void main(String[] args) throws IOException {
        // 使用File对象创建流对象
        File file = new File("input.txt");
        FileInputStream fileInputStream = new FileInputStream(file);

        // 基于文件路径创建对象
        FileInputStream fileInputStream2 = new FileInputStream("input.txt");

        // 读取字节数据，每次读取一个字节
        int read;
        while ((read = fileInputStream.read()) != -1) {
            System.out.println((char) read);
        }
        // 读取字节数据，每次读取字节数组
        int len;
        byte[] bytes = new byte[1024];
        while ((len = fileInputStream2.read(bytes)) != -1) {
            System.out.println(new String(bytes, 0, len));
        }

        // 释放资源
        fileInputStream.close();
        fileInputStream2.close();
    }
}
```

### 字节输出流
`java.io.OutputStream` 抽象类是表示字节输出流的所有类的超类，将指定的字节信息写出到目的地。
它定义了字节输出流的基本共性功能方法。

- `public void close()`: 关闭此输出流并释放与此流相关联的任何系统资源
- `public void flush()`: 刷新此输出流并强制任何缓冲的输出字节被写出
- `public void write(byte[] b)`: 将 b.length字节从指定的字节数组写入此输出流
- `public void write(byte[] b, int off, int len)`: 从指定的字节数组写入 len字节，从偏移量 off开始输出到此输出流
- `public abstract void write(int b)`: 将指定的字节输出流


```java
public class FileOutputStreamTest {
    public static void main(String[] args) throws IOException {
        // 使用File对象创建流对象
//        File file = new File("output.txt");
//        FileOutputStream fileOutputStream = new FileOutputStream(file);

        // 基于文件路径创建对象
        FileOutputStream fileOutputStream = new FileOutputStream("output.txt");
        // 写出字节数据
        fileOutputStream.write(97);
        // 写出字节数组
        byte[] bytes = {97, 98, 99, 100, 101};
        fileOutputStream.write(bytes);
        // 释放资源
        fileOutputStream.close();

        // 数据追加
        FileOutputStream fos = new FileOutputStream("output.txt",true);
        byte[] append = "Hello World".getBytes();
        fos.write(append);

        // 数据换行
        fos.write("\r\n".getBytes());
        
        // 释放资源
        fos.close();
    }
}
```

### 文件拷贝
```java
public class FileCopyTest {
    public static void streamCopy() {
        // 记录开始时间
        long start = System.currentTimeMillis();
        FileInputStream fis = null;
        FileOutputStream fos = null;
        try {
            // 创建流对象
            fis = new FileInputStream("movie.mp4");
            fos = new FileOutputStream("backup.mp4");
            int content;
            // 读取数据
            while ((content = fis.read()) != -1) {
                // 写出数据
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

    public static void zeroCopy() {
        long start = System.currentTimeMillis();
        FileInputStream fis = null;
        FileOutputStream fos = null;
        try {
            fis = new FileInputStream("movie.mp4");
            fos = new FileOutputStream("backup.mp4");

            FileChannel source = fis.getChannel();
            FileChannel target = fos.getChannel();
            //
            target.transferFrom(source, 0, source.position());
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
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
        System.out.println("使用channel复制文件总耗时:" + (end - start) + " 毫秒");
    }

    public static void filesCopy() {
        Path sourcePath = Paths.get("movie.mp4");
        Path destinationPath = Paths.get("backup.mp4");

        try {
            Files.copy(sourcePath, destinationPath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        streamCopy();
    }
}
```

## 字符流

### 字符输入流
java.io.Reader抽象类是表示用于读取字符流的所有类的超类，可以读取字符信息到内存中。
它定义了字符输入流的基本共性功能方法

- `public void close()`: 关闭此流并释放与此流相关联的任何系统资源。
- `public int read()`: 从输入流读取一个字符。
- `public int read(char[] cbuf)`: 从输入流中读取一些字符，并将它们存储到字符数组 `cbuf` 中

```java
public class FileReaderTest {
    public static void main(String[] args) throws IOException {
        // 创建字符流对象
        File file = new File("input.txt");
        FileReader fileReader = new FileReader(file);

        FileReader fileReader2 = new FileReader("input.txt");

        // 读取单个字符
        int ch;
        while((ch = fileReader.read()) != -1){
            System.out.println((char)ch);
        }

        char[] chars = new char[1024];
        int len;
        while((len = fileReader2.read(chars)) != -1){
            // 把数组中的数据变成字符串再进行打印
            System.out.println(new String(chars,0,len));
        }

        // 释放资源
        fileReader.close();
        fileReader2.close();
    }
}
```

### 字符输出流
`java.io.Writer` 抽象类是表示用于写出字符流的所有类的超类，将指定的字符信息写出到目的地。
它定义了字节输出流的基本共性功能方法。

- `void write(int c)` 写入单个字符
- `void write(char[] cbuf)` 写入字符数组
- `abstract void write(char[] cbuf, int off, int len)` 写入字符数组的某一部分,off数组的开始索引,len写的字符个数
- `void write(String str)` 写入字符串
- `void write(String str, int off, int len)` 写入字符串的某一部分,off字符串的开始索引,len写的字符个数
- `void flush()` 刷新该流的缓冲
- `void close()` 关闭此流

```java
public class FileWriterTest {
    public static void main(String[] args) throws IOException {
        File file = new File("output.txt");
        FileWriter fileWriter = new FileWriter(file);

        // 写出数据
        fileWriter.write(97); // 写出第1个字符
        fileWriter.write('b'); // 写出第2个字符
        fileWriter.write('C'); // 写出第3个字符
        fileWriter.write(30000); // 写出第4个字符，中文编码表中30000对应一个汉字

        // 释放资源
        fileWriter.close();

        // 追加数据
        FileWriter fileWriter2 = new FileWriter("output.txt",true);
        // 写出字节数组
        char[] chars = {'a','b','c','我'};
        fileWriter2.write(chars);
        // 写出字符串
        fileWriter2.write("Hello");
        // 释放资源
        fileWriter2.close();
    }
}
```

### 缓冲流
缓冲流的基本原理，是在创建流对象时，会创建一个内置的默认大小的缓冲区数组，通过缓冲区读写，减少系统IO次数，从而提高读写的效率。

- 字节缓冲流: BufferedInputStream，BufferedOutputStream
- 字符缓冲流: BufferedReader，BufferedWriter

```java
public class FileCopyTest {
    public static void bufferCopy() {
        // 记录开始时间
        long start = System.currentTimeMillis();
        BufferedInputStream bis = null;
        BufferedOutputStream bos = null;
        try {
            bis = new BufferedInputStream(new FileInputStream("movie.mp4"));
            bos = new BufferedOutputStream(new FileOutputStream("backup.mp4"));
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

## 压缩流与解压缩流
- 压缩流: 负责压缩文件或者文件夹

- 解压缩流: 负责把压缩包中的文件和文件夹解压出来

```java
public class ZipStreamTest {
    /**
     * 解压缩文件
     */
    public static void unzip(File src, File dest) throws IOException {
        //解压的本质：把压缩包里面的每一个文件或者文件夹读取出来，按照层级拷贝到目的地当中
        //创建一个解压缩流用来读取压缩包中的数据
        ZipInputStream zip = new ZipInputStream(new FileInputStream(src));
        //要先获取到压缩包里面的每一个zipEntry对象
        //表示当前在压缩包中获取到的文件或者文件夹
        ZipEntry entry;
        while ((entry = zip.getNextEntry()) != null) {
            System.out.println(entry);
            if (entry.isDirectory()) {
                //文件夹: 需要在目的地dest处创建一个同样的文件夹
                File file = new File(dest, entry.toString());
                file.mkdirs();
            } else {
                //文件: 需要读取到压缩包中的文件，并把他存放到目的地dest文件夹中（按照层级目录进行存放）
                FileOutputStream fos = new FileOutputStream(new File(dest, entry.toString()));
                int b;
                while ((b = zip.read()) != -1) {
                    //写到目的地
                    fos.write(b);
                }
                fos.close();
                //表示在压缩包中的一个文件处理完毕
                zip.closeEntry();
            }
        }
        zip.close();
    }

    /**
     * 压缩单个文件
     */
    public static void zipFile(File src, File dest) {
        try (FileInputStream fis = new FileInputStream(src);
             FileOutputStream fos = new FileOutputStream(dest);
             ZipOutputStream zipOS = new ZipOutputStream(fos);
        ) {
            ZipEntry zipEntry = new ZipEntry(src.toPath().toString());
            zipOS.putNextEntry(zipEntry);

            byte[] buffer = new byte[1024];
            int len;
            while ((len = fis.read(buffer)) != -1) {
                zipOS.write(buffer, 0, len);
            }
            zipOS.closeEntry();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 压缩文件夹
     */
    public static void zipDir(File src, File dest) throws IOException {
        if (!src.exists()) {
            throw new FileNotFoundException(src.getName() + " could not be found");
        } else if (src.isFile()) {
            throw new IOException("Does not support file");
        }
        if (dest.isFile()) {
            throw new IOException("Cannot place zipDir file into a file(" + dest.getName() + ")");
        }

        ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(dest));
        //遍历并压缩
        traverseZip(src, src.getName(), zos);
        zos.close();
    }

    private static void traverseZip(File src, String pathName, ZipOutputStream zos) throws IOException {
        //进入源文件夹，已经提前保证存在性、为目录
        File[] files = src.listFiles();

        //拼凑包内每一个文件的父级路径
        if (!pathName.isBlank() && !pathName.endsWith("\\\\")) {
            pathName = pathName.concat("\\");
        }

        for (File file : files) {
            //遍历文件夹
            if (file.isFile()) {
                //是文件
                ZipEntry fileEntry = new ZipEntry(pathName + file.getName());   //注意：表示的是压缩包内路径的名字
                zos.putNextEntry(fileEntry);    //创建的永远都是文件，若要创建目录，应当拼接字符串（父级路径）

                FileInputStream fis = new FileInputStream(file);
                byte[] bytes = new byte[1024];
                int len;
                while ((len = fis.read(bytes)) != -1) {
                    zos.write(bytes, 0, len);
                }
                fis.close();
                zos.closeEntry();   //关闭当前条目，准备写出下一个条目
            } else {
                //是目录
                String path = pathName + file.getName();    //用第三方变量，切忌直接更改原变量，防止路径出错
                traverseZip(file, path, zos);   //递归调用
            }
        }
    }

    public static void main(String[] args) throws IOException {
        // 压缩单个文件
        zipFile(new File("input.txt"), new File("input.zip"));

        // 压缩文件夹
        zipDir(new File("dest"), new File("backup.zip"));
    }
}
```