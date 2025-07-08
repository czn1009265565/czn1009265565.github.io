# HTTrack 使用详细教程
HTTrack 是一个免费开源的网站复制工具，可以将整个网站下载到本地进行离线浏览。以下是完整的使用指南：

## 一、安装HTTrack

### Windows系统
1. 访问官网 https://www.httrack.com
2. 下载Windows安装包
3. 运行安装程序，按向导完成安装

### macOS系统
```shell
brew install httrack
```

### Linux系统
```shell
sudo apt-get install httrack  # Debian/Ubuntu
sudo yum install httrack      # CentOS/RHEL
```

## 二、图形界面使用教程

1. 启动HTTrack
   - Windows: 从开始菜单启动"WinHTTrack Website Copier"
   - Linux/macOS: 终端输入httrack-gui
2. 新建项目
   - 输入项目名称
   - 设置保存路径
   - 点击"下一步"
3. 设置下载选项
   ```
   操作模式选择：
   - 下载网站(默认)
   - 仅下载文件
   - 测试链接
   ```
4. 输入目标URL
   - 格式：https://www.example.com
   - 可添加多个URL，用空格分隔
5. 设置选项
   - 下载深度(建议3-5层)
   - 文件类型过滤(可选)
   - 是否保留外部链接
   - 是否下载图片/CSS/JavaScript
6. 开始下载
   - 点击"完成"开始复制
   - 进度条显示下载状态

## 三、命令行高级用法

### 基本命令
```shell
httrack https://example.com -O /path/to/save -%v
```
### 常用参数

| 参数              | 说明                 |
|-----------------|--------------------|
| -O              | 目录指定保存目录           |
| -%v             | 显示详细输出             |
| -rN             | 设置递归深度(N为数字)       |
| -*              | 仅接受指定扩展名(如 -*.pdf) |
| +*              | 排除指定扩展名            |
| -N %h%p/%n%q    | 保持原始目录结构           |
| --robots=0      | 忽略robots.txt限制     |
| -F "user-agent" | 设置自定义User-Agent    |

### 示例命令
1. 完整镜像网站<br>
```httrack https://example.com -O ./mirror -%v -r5```

2. 仅下载PDF文件<br>
```httrack https://example.com -O ./pdfs -%v -*.pdf```

3. 排除图片<br>
```httrack https://example.com -O ./no_images -%v +*.jpg +*.png +*.gif```

## 四、高级功能

1. 断点续传<br>
   中断后重新运行相同命令会自动继续
2. 更新已有镜像<br>
   ```httrack https://example.com -O ./existing_mirror --update```
3. 限制下载速度<br>
   ```httrack https://example.com --sockets=2 --rate=50```
4. 使用代理<br>
   ```httrack https://example.com --proxy=127.0.0.1:8080```


## 五、常见问题解决

1. SSL证书错误<br>
   ```httrack --ssl-no-verify https://example.com```
2. 中文乱码问题<br>
   ```httrack --default-encoding=utf-8 https://example.com```
3. 403禁止访问<br>
   尝试设置User-Agent<br>
   ```httrack -F "Mozilla/5.0" https://example.com```
4. 下载卡顿<br>
   增加延迟<br>
   ```httrack --timeout=30 --retries=3 https://example.com```