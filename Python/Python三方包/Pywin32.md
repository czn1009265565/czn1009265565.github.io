# Pywin32

Pywin32是Python的一个强大而广泛使用的库，它提供了访问`Windows API`的接口，以实现处理Windows系统资源的功能，
如窗口管理、文件操作、注册表访问、系统信息获取等操作。

安装  
```shell
pip install pywin32 -i https://mirrors.aliyun.com/pypi/simple
```

## 常用模块

### win32gui
`win32gui` 提供了对Windows GUI（图形用户界面）组件的访问和控制，如窗口操作、菜单、绘图等

```python
import win32gui
from PIL import ImageGrab


if __name__ == "__main__":
    # 获取所有窗口句柄
    hwnd_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnd_list)

    # 根据窗口名称获取窗口句柄
    hwnd = win32gui.FindWindow(None, "窗口名称")

    # 根据窗口句柄获取窗口标题
    title = win32gui.GetWindowText(hwnd)

    # 根据父窗口句柄获取子窗口句柄列表
    hwnd_child_list = []
    win32gui.EnumChildWindows(hwnd, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
    # 根据子窗口句柄获取父窗口句柄
    parent_hwnd = win32gui.GetParent(hwnd)

    # 获取前台窗口
    foreground_window = win32gui.GetForegroundWindow()
    # 激活窗口
    win32gui.SetForegroundWindow(hwnd)

    # 获取窗口全局坐标
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    # 截取指定窗口截图
    region = win32gui.GetWindowRect(hwnd)
    grab = ImageGrab.grab(region)
```