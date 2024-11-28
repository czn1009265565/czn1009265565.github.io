# PyQt6

## 简介
PySide / PyQt是C++的程序开发框架QT的Python实现，在介绍PyQt框架之前，先介绍下什么是QT、GUI?

- Qt 是跨平台C++图形用户界面应用程序开发框架。它既可以开发GUI程序，也可用于开发非GUI程序，比如控制台工具和服务器。Qt是面向对象的框架，使用特殊的代码生成扩展（称为元对象编译器(Meta Object Compiler, moc)）以及一些宏，Qt很容易扩展，并且允许真正的组件编程。

- GUI 是图形用户界面（Graphical User Interface）的简称，是指采用图形方式显示的计算机操作用户界面。

## 环境搭建

### 安装依赖  
```shell
pip install pyqt6 -i https://mirrors.aliyun.com/pypi/simple
```

安装完成后，基于脚本测试是否安装成功  
```python
import sys
from PyQt6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.resize(300, 200)
    widget.setWindowTitle("Hello, World!")
    widget.show()
    sys.exit(app.exec())
```

### 配置 Qt Designer
Qt Designer 是个强大、灵活的可视化GUI设计工具，使用简单，通过拖拽和单击就可以完成复杂的界面设计，并可随时预览效果图，生成的UI界面是个后缀为 `.ui` 的文件。

安装`pyqt6-tools` 工具包

```shell
pip install pyqt6-tools -i https://mirrors.aliyun.com/pypi/simple
```

配置Pycharm，`File => Settings => Tools => External Tools` 点击 + 号，添加外部工具  
```
# 名称
Name: QT Designer
Group: PyQt6
Program: C:\Users\Administrator\AppData\Local\Programs\Python\Python310\Scripts\pyqt6-tools.exe
Arguments: designer
Working directory: $FileDir$ 
```

验证是否设置成功，`Tools => PyQt6 => QT Designer` 启动工具。


### 配置 PyUIC
PyUIC 的作用是把上述 `.ui` 的文件转换成 `.py` 文件

```
Name: PyUIC
Group: PyQt6
Program: C:\Users\Administrator\AppData\Local\Programs\Python\Python310\Scripts\pyuic6.exe
Arguments: $FileName$ -o $FileNameWithoutExtension$.py
Working directory: $FileDir$ 
```

使用 `QT Designer`基于`Ctrl + S`保存窗体，自定义文件名例如 `windows.ui`，
右键点击`windows.ui => PyQt6 => PyUIC`生成对应的Python文件 `windows.py`，这里又叫做界面文件。

- 界面文件: `.py` 文件是由 `.ui` 文件编译而来，所以当 `.ui` 文件发生变化时，对应的 `.py` 文件也会发生变化，将这种由 `.ui` 文件编译而来的 `.py` 文件称之为界面文件
- 逻辑文件: 由于界面文件每次编译都会初始化，因此需要新建一个 `.py` 文件调用界面文件，这个新建的文件可以称之为逻辑文件

创建逻辑文件

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from windows import *


class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_win = MyMainWindow()
    my_win.show()
    sys.exit(app.exec())
```