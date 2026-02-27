# Qt Designer
Qt Designer 是个强大、灵活的可视化GUI设计工具，使用简单，通过拖拽和单击就可以完成复杂的界面设计，并可随时预览效果图，
生成的UI界面是个后缀为 `.ui` 的文件。

## 安装
安装 PyQt6 和相关工具

```shell
pip install pyqt6 pyqt6-tools -i https://mirrors.aliyun.com/pypi/simple
```

启动 Qt Designer

```shell
pyqt6-tools designer
```

## 界面概览

主界面分为5个核心区域：

1. 控件工具箱（左侧）：各种UI控件
2. 画布区域（中央）：界面设计区域
3. 对象查看器（右上）：控件层次结构
4. 属性编辑器（右下）：控件属性设置
5. 菜单栏/工具栏（顶部）：文件操作和布局工具

## 操作流程

1. 创建新项目  
   1. 选择模板 → `Main Window` → 创建
   2. 保存为 `.ui` 文件
2. 添加控件  
   从工具箱拖拽控件到画布
3. 设置属性  
   选中控件 → 在属性编辑器中修改：
   - objectName: 控件标识（代码中引用）
   - geometry: 位置和大小
   - text: 显示文本
   - font: 字体设置
4. 布局管理  
   选择控件 → 右键 → 布局：
   - 水平布局（Lay Out Horizontally）
   - 垂直布局（Lay Out Vertically）
   - 栅格布局（Lay Out in a Grid）
   - 打破布局: 右键 → 打破布局
5. 预览界面
   快捷键: `Ctrl + R`
6. PyUIC代码转换  
   将 .ui 文件转换为 Python 代码: `pyuic6 windows.ui -o windows.py`
7. 代码引用
```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from windows import *


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_win = MyMainWindow()
    my_win.show()
    sys.exit(app.exec())
```

## 控件分类

### 1. Layouts（布局管理器）
布局管理器用于自动排列和管理子控件的位置和大小，确保界面在不同尺寸下保持美观和一致性。常见的布局包括：

- Vertical Layout（垂直布局）：子控件按垂直方向排列
- Horizontal Layout（水平布局）：子控件按水平方向排列
- Grid Layout（网格布局）：子控件按网格行列排列
- Form Layout（表单布局）：适合标签和输入框成对排列的表单界面

### 2. Spacers（间隔器）

间隔器用于在布局中填充空白区域，调整控件间的间距，分为两种类型：

- Horizontal Spacer（水平间隔器）：在水平方向上拉伸或压缩空白区域
- Vertical Spacer（垂直间隔器）：在垂直方向上调整间距

### 3. Buttons（按钮类）
按钮是用户交互的核心部件，常见类型包括：

- Push Button（普通按钮）：用于触发操作
- Tool Button（工具按钮）：常与工具栏结合，可关联菜单或动作
- Radio Button（单选按钮）：一组中只能选择一个选项
- Check Box（复选框）：允许用户多选

### 4. Item Views（项目视图）
用于显示和编辑结构化数据，通常与模型（Model）结合使用：

- List View（列表视图）：显示一维数据列表
- Tree View（树形视图）：分层显示数据（如文件目录）
- Table View（表格视图）：以行列形式展示数据
- Column View（列视图）：类似文件管理器的多列导航

### 5. Item Widgets（项目控件）
直接封装了模型-视图逻辑的便捷控件，无需单独设置模型：

- List Widget（列表控件）：直接管理字符串或自定义项的列表
- Tree Widget（树形控件）：可手动添加分层节点
- Table Widget（表格控件）：直接编辑行列数据

### 6. Containers（容器）
用于分组或容纳其他控件，增强界面组织性：

- Group Box（分组框）：为控件添加标题和边框分组
- Scroll Area（滚动区域）：为内容添加滚动条
- Tab Widget（标签页）：通过标签切换不同页面
- Stacked Widget（堆叠控件）：同一区域显示多个页面，通过代码切换

### 7. Input Widgets（输入控件）
用于接收用户输入数据：

- Line Edit（单行文本框）：输入简短文本
- Text Edit（多行文本编辑器）：支持富文本编辑
- Combo Box（下拉框）：从预设选项中选择
- Spin Box（数字选择框）：调整数值
- Date/Time Edit（日期时间编辑器）：选择日期或时间

### 8. Display Widgets（显示控件）
用于展示信息或状态，通常不可编辑：

- Label（标签）：显示文本或图片
- Text Browser（文本浏览器）：显示只读文本（支持超链接）
- Graphics View（图形视图）：显示复杂图形或自定义绘制内容
- Progress Bar（进度条）：展示任务进度
- LCD Number（液晶数字显示）：模拟液晶数字效果