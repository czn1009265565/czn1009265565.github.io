# PyInstaller

PyInstaller是一个用于将Python脚本打包成独立可执行文件的工具。
它的原理是将Python脚本及其依赖的库、资源文件等打包成一个单独的可执行文件，使得在其他机器上运行时不需要安装Python解释器和相关库，即可直接运行。

安装
```shell
pip install pyinstaller -i https://mirrors.aliyun.com/pypi/simple
```

## 基本语法  
```shell
pyinstaller main.py
```

- `build/`: 该目录是pyinstaller生成的临时目录，用于存放编译过程中生成的中间文件和临时文件
- `dist/`: 该目录是pyinstaller生成的最终目录，用于存放编译后生成的可执行文件或打包后的应用程序
- `xxx.spec`: pyinstaller的配置文件，用于指定编译的参数和选项。可以通过修改该文件来自定义编译过程中的一些设置

## 常用参数
我们可以通过 `pyinstaller --help` 命令查看参数介绍，这里列举常用的参数

- `-D`: 文件夹模式。在打包完成后生成一个文件夹，其中包含一个exe文件和一个包含若干依赖文件的文件夹
- `-F`: 单文件模式。在打包完成后只会生成一个单独的exe文件
- `--add-data source:target`: 指定要添加到应用程序的其他数据文件或包含数据文件的目录，source是文件的路径，target是项目根目录下的相对路径
- `--add-binary source:target`: 和`--add-data`类似，不过指定的文件夹或文件是二进制的
- `-p DIR`: 搜索并导入该路径下的模块
- `--hidden-import MODULENAME`: 需要进行额外导入的模块。当pyinstaller在程序中找不到一些模块时，需要你额外指定
- `-w`: 打包程序运行后隐藏控制台窗口
- `-i`: 设置打包后exe程序的图标
- `--disable-windowed-traceback`: 禁用异常提示(只能在Windows和macOS上使用)
- `--uac-admin`: 启动打包后的程序时申请以管理员模式运行(仅Windows)

## 基本使用

```shell
# 打包单个exe文件
pyinstaller -F main.py

# 隐藏控制台窗口
pyinstaller -w main.py

# 更改图标
pyinstaller -i icon.ico main.py

# 禁用异常提示
pyinstaller --disable-windowed-traceback main.py

# 申请管理员权限
pyinstaller --uac-admin main.py
```

### 内嵌静态文件  

使用资源嵌入后，资源文件夹的路径发生了变化，我们不能使用一般的相对路径来调用assets这样的内嵌资源文件夹
```python
import os
import sys


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.normpath(os.path.join(base_path, relative_path))


if __name__ == "__main__":
    get_path("assets/image.gif")
```

打包命令  
```shell
pyinstaller --add-data assets:assets main.py
```

### 综合案例

```shell
pyinstaller -w -F -i icon.ico --add-data assets:assets --uac-admin main.py
```