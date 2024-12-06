# PyQt6 Button
按钮控件，允许用户通过单击来执行操作

## QPushButton
QPushButton 普通按钮

构造函数:  
- `QPushButton(parent = None)`                单个参数，父对象默认值为None
- `QPushButton(text[, parent = None])`        两个参数，指定按钮上的文字
- `QPushButton(icon, text[, parent = None])`  三个参数，指定按钮上的图标和文字

```python
import sys

from PySide6 import QtGui, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QPushButton-创建")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""

        icon = QtGui.QIcon("./icon/Python_128px.png")
        # 1. 单个参数
        # button = QtWidgets.QPushButton()
        # button.setParent(self)  # 创建时父对象为None,可用setParent方法指定
        # button.setText("普通按钮")  # 设置按钮上的文字
        # button.setIcon(icon)  # 设置按钮上的图标

        # 2. 两个参数
        # button = QtWidgets.QPushButton("普通按钮", self)

        # 3. 三个参数
        button = QtWidgets.QPushButton(icon, "普通按钮", self)

        button.resize(150, 50)  # 调整按钮尺寸
        # 通过计算需要移动的尺寸，令按钮居中
        button.move((self.width() - button.width()) // 2, (self.height() - button.height()) // 2)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```

## 信号与槽函数

信号与槽机制是 PyQt6 中用于处理事件的核心机制，通过连接信号与槽，可以在某个事件发生时触发特定的功能。

- 信号: 信号是在对象上发生的事件，例如按钮被点击、文本发生变化等。每个对象都可以发射（emit）零个或多个信号。例如，QPushButton对象有一个clicked信号，表示按钮被点击
- 槽: 槽是接收信号的函数。槽函数可以连接到一个或多个信号，并在信号触发时执行。槽函数可以是类的成员函数、全局函数或者lambda表达式

```python
import sys

from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QAbstractButton-信号")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""
        # 由于QAbstractButton类无法被实例化，用QPushButton演示
        self.button = QtWidgets.QPushButton("点击我！", self)
        # 移动按钮控件的位置
        self.button.move(350, 300)
        # 点击事件
        self.button.clicked.connect(self.slot)
        # 按下事件
        # self.button.pressed.connect(self.slot)
        # 释放事件
        # self.button.released.connect(self.slot)

    def slot(self) -> None:
        print("按钮被交互了!")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```