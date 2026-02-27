# PyQt6

## 简介
PySide / PyQt是C++的程序开发框架QT的Python实现，都用于在Python中构建GUI应用程序，主要区别在于它们的授权，
PyQt商业使用可能需要购买许可
在介绍PyQt框架之前，先介绍下什么是QT、GUI?

- Qt 是跨平台C++图形用户界面应用程序开发框架。它既可以开发GUI程序，也可用于开发非GUI程序，比如控制台工具和服务器。Qt是面向对象的框架，使用特殊的代码生成扩展（称为元对象编译器(Meta Object Compiler, moc)）以及一些宏，Qt很容易扩展，并且允许真正的组件编程。

- GUI 是图形用户界面（Graphical User Interface）的简称，是指采用图形方式显示的计算机操作用户界面。

PyQt和PySide是两个Python绑定的Qt库，它们都用于在Python中构建GUI应用程序。主要区别在于它们的授权和维护者。PyQt由英国的Riverbank Computing开发，使用GPLv3和商业许可证，商业使用可能需要购买许可，而PySide起初由Nokia开发，现在由Qt公司和开源社区共同维护，遵循更为宽松的LGPL许可证，更适合商业项目。

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