## Java与Python协同开发

### 背景
Java与Python结合开发是指将Python语言与Java语言结合起来，利用它们的优势，共同开发一个应用程序。  
Python语言拥有许多强大的特性，如易于学习、快速开发、可扩展性等，而Java语言则拥有跨平台、可靠性、安全性等优势，因此将它们结合起来，可以发挥出更大的作用。  
在一个大型企业系统中，Java可能用于后端服务和业务逻辑，而Python可能用于数据分析和机器学习任务。在这种情况下，两种语言需要能够协同工作，以实现全面的功能。  


### ProcessBuilder
Java提供了ProcessBuilder类，可以在Java代码中调用外部程序或脚本。

**Java执行命令行**  
```java
public class PythonTest {
    public static void main(String[] args) {
        try {
            // 创建ProcessBuilder对象，指定要执行的命令和参数
            ProcessBuilder pb = new ProcessBuilder("python", "-c", "print('Hello, Python!')");
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

**Java执行Python脚本**  
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

**Java中断Python任务**  
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