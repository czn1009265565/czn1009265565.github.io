# PyQt6 QLabel
标签控件用于在界面上显示文字、图像等

## 简单创建

```python
import sys

from PySide6 import QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QLabel-创建")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""
        # 创建时即设置了标签文本与父对象
        label1 = QtWidgets.QLabel("PySide6", self)
        label1.move(350, 200)

        # 也可以创建空白标签，随后设置父控件与文字
        label2 = QtWidgets.QLabel()
        label2.setParent(self)
        label2.setText("QLabel 标签控件")
        label2.move(350, 240)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```

## 文本对齐、缩进、换行

### 对齐

- `setAlignment(Qt.Alignment)`    设置文本对齐方式，详见下方Qt.Alignment
- `alignment() -> Qt.Alignment`   获取文本对齐方式

水平对齐:  
- `Qt.AlignLeft`      与左边缘对齐
- `Qt.AlignRight`     与右边缘对齐
- `Qt.AlignHCenter`   在可用空间中水平居中
- `Qt.AlignJustify`   两端对齐（尽可能使文字占满横向空间）

垂直对齐:  
- `Qt.AlignTop`       与顶部对齐
- `Qt.AlignBottom`    与底部对齐
- `Qt.AlignVCenter`   在可用空间中垂直居中
- `Qt.AlignBaseline`  与基线对齐

若需同时设置水平、垂直两个维度的对齐方式，只需将两个Flags用或运算符连接，例如:
`Qt.AlignCenter` 等价于 `Qt.AlignVCenter | Qt.AlignHCenter`

### 缩进
缩进的方向与对齐方向有关，`Qt.AlignLeft` 则缩进出现在左边缘，`Qt.AlignTop` 则出现在上边缘，以此类推。

- `setIndent(indent: int)`        设置缩进，默认为-1，即不进行缩进
- `indent() -> int`               获取缩进数

### 换行
`QLabel` 可以开启自动换行功能，即在需要时从单词之间换行

- `setWordWrap(on: bool)`   设置是否开启自动换行，默认关闭
- `wordWrap() -> bool`      获取是否开启自动换行

### 编码

```python
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QLabel-文本操作")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面与测试功能"""
        label = QtWidgets.QLabel(self)

        # 手动设置控件尺寸，而非由内容自动设置
        label.resize(300, 300)
        center_x = (self.width() - label.width()) // 2
        center_y = (self.height() - label.height()) // 2
        label.move(center_x, center_y)

        # 设置标签文本
        label.setText("PySide6 Code Tutorial")

        # 设置文本对齐方式
        # 居中对齐
        label.setAlignment(Qt.AlignCenter)
        # 水平+垂直居中对齐，等价于 Qt.AlignCenter
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # 上对齐
        # label.setAlignment(Qt.AlignTop)
        # 两侧对齐
        # label.setAlignment(Qt.AlignJustify)

        # 设置文本缩进
        # label.setText(description)
        # 设置缩进，缩进方向对对齐方向相关
        # label.setIndent(30)
        print(label.indent())

        # 设置文本自动换行(若关闭自动换行，则超出单行的部分无法显示)
        label.setWordWrap(True)
        print(label.wordWrap())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
```