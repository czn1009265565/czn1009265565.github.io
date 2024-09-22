## Java ProcessBuilder

### 简介
ProcessBuilder用于创建操作系统进程

**进程属性**  
1. 命令 command，表示要调用的外部程序文件及其参数
2. 环境 environment，从变量到值依赖于系统的映射
3. 工作目录 working directory，默认值是当前进程的当前工作目录，通常根据系统属性 user.dir 来命名
4. redirectErrorStream属性，此属性为false意思是子进程的标准输出和错误输出被发送给两个独立的流，这些流可以通过 Process.getInputStream() 和 Process.getErrorStream()方法来访问。如果将值设置为 true，标准错误将与标准输出合并，在此情况下，合并的数据可从 Process.getInputStream() 返回的流读取，而从 Process.getErrorStream() 返回的流读取将直接到达文件尾。

### 执行命令行

```java
public class CommandTest {
    public static void main(String[] args) {
        try {
            // 创建ProcessBuilder对象，指定要执行的命令和参数
            ProcessBuilder pb = new ProcessBuilder("java", "--version");
            // 启动子进程并等待其完成
            Process process = pb.start();

            // 读取子进程的输出结果
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            // 等待子进程完成并获取退出值
            int exitCode = process.waitFor();
            System.out.println("Exit Code: " + exitCode);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

### 执行Python脚本

```java
public class PythonTest {
    public static void main(String[] args) {
        try {
            // 创建ProcessBuilder对象，指定要执行的命令和参数
            ProcessBuilder pb = new ProcessBuilder("python", getResourceFilePath("test.py"));
            // 启动子进程并等待其完成
            Process process = pb.start();

            // 读取子进程的输出结果
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            // 等待子进程完成并获取退出值
            int exitCode = process.waitFor();
            System.out.println("Exit Code: " + exitCode);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取资源文件路径
     *  * @param fileName 文件名称
     * @return 文件绝对路径
     */
    public static String getResourceFilePath(String fileName) {
        // 获取当前项目的根目录路径
        String rootPath = System.getProperty("user.dir");
        // 拼接资源文件夹的相对路径
        String resourceFolderPath = rootPath + File.separator + fileName;
        // 创建File对象，并打印资源文件夹的绝对路径
        File resourceFolder = new File(resourceFolderPath);
        // 打印资源文件夹的绝对路径
        return resourceFolder.getAbsolutePath();
    }
}
```

### 中断Python任务

```java
public class PythonTest {
    public static void main(String[] args) {
        try {
            // 创建ProcessBuilder对象，指定要执行的命令和参数
            ProcessBuilder pb = new ProcessBuilder("python", getResourceFilePath("test.py"));
            // 启动子进程并等待其完成
            Process process = pb.start();
            // 中断Python进程
            process.destroy();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取资源文件路径
     *  * @param fileName 文件名称
     * @return 文件绝对路径
     */
    public static String getResourceFilePath(String fileName) {
        // 获取当前项目的根目录路径
        String rootPath = System.getProperty("user.dir");
        // 拼接资源文件夹的相对路径
        String resourceFolderPath = rootPath + File.separator + fileName;
        // 创建File对象，并打印资源文件夹的绝对路径
        File resourceFolder = new File(resourceFolderPath);
        // 打印资源文件夹的绝对路径
        return resourceFolder.getAbsolutePath();
    }
}
```