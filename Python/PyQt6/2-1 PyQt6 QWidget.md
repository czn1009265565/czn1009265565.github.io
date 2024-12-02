# PyQt6 QWidget

QWidget 是 Qt 框架中的一个核心类，用于创建图形用户界面(GUI)应用程序的基本可视化元素。
它是所有窗口组件类的父类，每个窗口组件都是一个 QWidget。QWidget 类对象常用作父组件或顶级组件使用。
QWidget 提供了一套完整的窗口系统，包括窗口管理、事件处理、绘图等功能。


## 最小模板

```python
import sys

from PySide6 import QtCore, QtGui, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        # 调用父类的初始化方法
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle("空白测试模板")
        # 设置窗口大小，单位为像素
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""
        # 在此处编写设置UI的代码


if __name__ == "__main__":
    # 创建APP，将运行脚本时的其他参数传给Qt以初始化
    app = QtWidgets.QApplication(sys.argv)
    # 实例化一个MyWidget类对象
    window = MyWidget()
    # 显示窗口
    window.show()
    # 正常退出APP：app.exec()关闭app，sys.exit()退出进程
    sys.exit(app.exec())
```

## 位置
1. 当QWidget为窗口时，设置/获取其相对桌面的位置
2. 当QWidget为子控件时，设置/获取其相对父控件的位置

```python
import sys

from PySide6 import QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWidget 位置")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.location()

    def location(self) -> None:
        """设置位置功能"""
        # 设置窗口位置位于屏幕左上角向右向下移动200像素
        self.move(200, 200)
        # 创建一个标签子控件
        self.label = QtWidgets.QLabel("Label标签", self)
        # 相对父控件（窗口）移动位置
        self.label.move(100, 200)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```

## 父子关系
QWidget 提供了多种API来获取（访问）其父子控件

- `.setParent()`       指定本控件的父控件
- `.parentWidget()`    获取父控件
- `.children()`        获取所有子控件，返回一个列表
- `.childAt()`         获取在指定坐标的子控件
- `.childrenRect()`    所有子控件（被隐藏的除外）构成的矩形
- `.childrenRegion()`  所有子控件（被隐藏的除外）构成的范围

```python
import sys
from pprint import pprint

from PySide6 import QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWidget-父子关系")
        self.resize(400, 300)
        self.setup_ui()
        self.test_children()
        self.test_parent()

    def setup_ui(self) -> None:
        """设置界面"""
        self.button = QtWidgets.QPushButton("点击我！", self)
        self.button.clicked.connect(lambda: print("按钮被点击了"))
        self.button.move(50, 200)
        self.label = QtWidgets.QLabel("PySide", self)
        self.label.move(150, 50)

    def test_children(self) -> None:
        """测试访问子控件功能"""
        # 打印所有子控件，以列表返回，顺序同添加顺序
        pprint(self.children())

        # 获取处于指定坐标的子控件，若该坐标无子控件则返回None
        print(self.childAt(150, 55))

        # 返回的子控件都可以被操作
        self.childAt(150, 55).setStyleSheet("background-color: cyan;")

        # 打印所有子控件构成的矩形
        print(self.childrenRect())
        print(self.childrenRegion())

    def test_parent(self) -> None:
        """测试访问父控件功能"""
        print(self.label.parentWidget())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```

## 层级关系
QWidget 有层级关系
默认情况下，后绘制的控件会遮盖先绘制的控件
可以通过如下API调整层级关系

- `.lower()`                降低层级
- `.raise_()`               提高层级(注意为避免和关键字冲突，末尾有下划线)
- `.stackUnder(QWidget qWidget)`  将自身置于qWidget控件之下

```python
import sys

from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWidget-层级关系")
        self.resize(800, 600)
        self.setup_ui()
        self.test_hierarchical()

    def setup_ui(self) -> None:
        """设置界面"""
        self.label_1 = QtWidgets.QLabel("标签1", self)
        self.label_1.resize(200, 200)
        self.label_1.setStyleSheet("background-color: red;")

        # 默认情况下，后绘制的控件会覆盖先绘制的
        self.label_2 = QtWidgets.QLabel("标签2", self)
        self.label_2.resize(200, 200)
        self.label_2.setStyleSheet("background-color: green;")
        self.label_2.move(50, 50)

    def test_hierarchical(self) -> None:
        """测试调整层级关系功能"""
        button = QtWidgets.QPushButton("显示标签", self)
        button.move(400, 100)

        @QtCore.Slot()
        def test_slot() -> None:
            """按钮的槽函数"""
            # 以下三种方法之一，都可以使得label_1显示在前面
            # self.label_2.lower()  # 降低label_2的层级
            # self.label_1.raise_()  # 提高label_1的层级
            self.label_2.stackUnder(self.label_1)  # 使得2在1之下

        # 连接按钮点击信号与槽函数
        button.clicked.connect(test_slot)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```

## 键盘输入焦点控制

只有当前获得焦点的控件才能与用户交互

**本控件的焦点的控制**  
- `.hasFocus() -> bool`                          返回此控件（或其焦点代理）是否具有键盘输入焦点
- `.setFocus()`                                  槽函数，若其父控件为活动窗口，则为此控件（或其焦点代理）设置焦点
- `.setFocus(reason: Qt.FocusReason)`            Qt.FocusReason 详见下文
- `.clearFocus()`                                移除控件的焦点

**子控件的焦点的控制**  
- `.focusNextChild() -> bool`                    把焦点交给下一个子控件
- `.focusPreviousChild() -> bool`                把焦点交给上一个子控件
- `.focusNextPrevChild(next: bool) -> bool`      上两种方法的结合，当next为True向下查找下一个子控件，否则向上
- `.focusWidget() -> QWidget`

**Qt.FocusReason**具体分为如下数种  
- Qt.MouseFocusReason           鼠标活动导致
- Qt.TabFocusReason             按下了Tab键
- Qt.BacktabFocusReason         Backtab导致，例如按下Shift+Tab键
- Qt.ActiveWindowFocusReason    窗口系统使该窗口处于活动或非活动状态
- Qt.PopupFocusReason           应用程序打开/关闭一个弹出窗口，该弹出窗口抓取/释放键盘焦点
- Qt.ShortcutFocusReason        用户输入了一个标签的伙伴快捷键（参阅QLabel.buddy）
- Qt.MenuBarFocusReason         菜单栏获得了焦点
- Qt.OtherFocusReason           其他原因

```python
import sys

from PySide6 import QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QWidget-焦点控制")
        self.resize(800, 600)
        self.setup_ui()
        self.test_focus()

    def setup_ui(self) -> None:
        """设置界面"""
        self.button = QtWidgets.QPushButton("测试按钮", self)
        self.button.move(200, 200)

        # 单行文本编辑器，当获得焦点时可以输入内容
        self.le = QtWidgets.QLineEdit(self)
        self.le.move(350, 100)

        # 下拉菜单，当获得焦点时可以用键盘方向键上下切换当前所选
        self.cbb = QtWidgets.QComboBox(self)
        self.cbb.addItem("选项1")
        self.cbb.addItem("选项2")
        self.cbb.move(500, 100)

        # 纯文本编辑器，当获得焦点时可以输入内容
        self.pte = QtWidgets.QPlainTextEdit(self)
        # 将纯文本编辑器中按下Tab键功能设置为切换焦点
        self.pte.setTabChangesFocus(True)
        self.pte.move(350, 150)

    def test_focus(self):
        """测试设置焦点功能"""
        self.button.clicked.connect(self.pte.setFocus)
        self.button.clicked.connect(lambda: print(self.button.hasFocus()))
        self.button.clicked.connect(lambda: print(self.pte.hasFocus()))
        self.button.clicked.connect(lambda: print(self.focusWidget()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```