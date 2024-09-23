# Java Path&File

## Paths

工具类，获取Path对象

```java
public class PathsTest {
    public static void main(String[] args) throws IOException {
        // 相对路径，基于user.dir路径定位
        Path path1 = Paths.get("README.md");
        // 路径拼接
        Path path2 = Paths.get("D:", "workspace", "project", "README.md");
        // 绝对路径
        Path path3 = Paths.get("D:\\workspace\\project\\README.md");
    }
}
```

## Path
Path对象来表示需要处理的文件或目录的路径

```java
public class PathTest {
    public static void main(String[] args) throws IOException {
        Path path = Paths.get("D:\\workspace\\project\\README.md");
        // 获取文件
        Path fileName = path.getFileName();
        // 基于索引获取文件或路径名称
        Path name = path.getName(0);
        // 获取路径层级个数
        int count = path.getNameCount();
        // 获取父级路径
        Path parent = path.getParent();
        // 获取根路径
        Path root = path.getRoot();
        // 获取子路径
        Path subpath = path.subpath(0, 1);
        // 转换为URI的格式
        URI uri = path.toUri();
        // 转化为File对象
        File file = path.toFile();
        // 转换为String
        String string = path.toString();
        // 追加路径
        Path resolve = path.resolve("resolve");
    }
}
```

## Files
Java中的Files工具类是Java 7中引入的一项强大的文件和目录处理工具

```java
public class FilesTest {
    public static void main(String[] args) throws IOException {
        // 创建文件
        Path path = Paths.get("test.txt");
        Files.createFile(path);

        Path source = Paths.get("input.txt");
        Path target = Paths.get("output.txt");
        // 复制文件
        Files.copy(source, target);
        // 移动文件
        Files.move(source, target);
        // 删除文件
        Files.delete(path);
        // 读取所有内容(字符串)
        List<String> content = Files.readAllLines(path, StandardCharsets.UTF_8);
        // 读取所有内容(字节)
        byte[] bytes = Files.readAllBytes(path);
        // 写入文件
        Files.write(target, bytes);
        Files.write(target, content);
    }
}
```

## File
1. java.io.File类：文件和文件目录路径的抽象表示形式，与平台无关
2. File类中涉及到关于文件或文件目录的创建、删除、重命名、修改时间、文件大小等方法，并未涉及到写入或读取文件内容的操作。如果需要读取或写入文件内容，必须使用IO流来完成
3. 想要在Java程序中表示一个真实存在的文件或目录，那么必须有一个File对象，但是Java程序中的一个File对象，可能没有一个真实存在的文件或目录
4. File对象可以作为参数传递给流的构造器，指明读取或写入的"终点"

```java
public class FileTest {
    public static void main(String[] args) throws IOException {
        Path path = Paths.get("D:\\workspace\\project");
        File file = path.toFile();

        // 创建目录
        boolean mkdir = file.mkdir();
        // 创建目录，父级不存在则一并创建
        boolean mkdirs = file.mkdirs();
        // 创建文件
        boolean newFile = file.createNewFile();
        // 删除文件
        boolean delete = file.delete();

        // 获取文件名
        String name = file.getName();
        // 转换为Path对象
        path = file.toPath();
        // 获取文件大小(字节数)
        long length = file.length();
        // 最后更新时间戳
        long last = file.lastModified();
        // 获取目录下文件字符串列表
        String[] fileString = file.list();
        // 获取目录下文件列表
        File[] files = file.listFiles();

        // 是否文件
        boolean fileCondition = file.isFile();
        // 是否目录
        boolean directory = file.isDirectory();
        // 是否存在
        boolean exists = file.exists();
        // 是否可读
        boolean read = file.canRead();
        // 是否可写
        boolean write = file.canWrite();
        // 是否可执行
        boolean execute = file.canExecute();
        // 是否隐藏
        boolean hidden = file.isHidden();
    }
}
```