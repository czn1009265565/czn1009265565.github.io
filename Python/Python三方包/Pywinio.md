# Pywinio
WinIO 是一个用于 Windows 平台的内核级硬件访问库（通过驱动实现），允许用户程序直接读写 I/O 端口、物理内存以及模拟硬件输入（如键盘、鼠标）。
它绕过了 Windows 系统的安全限制，提供了对底层的直接控制。

## 应用场景
1. 硬件测试与调试  
   - 直接与硬件设备（如 PCI 卡、传感器）交互
   - 读写特定 I/O 端口或内存映射寄存器
2. 游戏与外挂开发  
   - 绕过游戏反作弊机制（如模拟键盘鼠标输入）
   - 修改游戏内存数据（需注意法律风险）
3. 嵌入式系统交互  
   - 控制工业设备或单片机接口。
4. 低级输入模拟  
   - 替代 pyautogui 或 pydirectinput 无法处理的场景（如驱动级按键）
5. 系统工具开发  
   - 开发硬件监控工具（如直接读取温度传感器）

## 驱动安装

### 下载驱动文件:

官网 http://www.internals.com/
Github https://github.com/vaptu/winio.git

下载 `WinIo64.sys` 或 `WinIo32.sys`

### 将驱动文件放入系统目录

`C:\Windows\System32\drivers\`

### 注册并启动驱动

```shell
# 注册驱动（以 WinIo64.sys 为例）
sc create WinIo type= kernel start= auto binPath= C:\Windows\System32\drivers\WinIo64.sys

# 启动驱动
sc start WinIo
```

### 安装依赖
```shell
pip install pywinio -i https://mirrors.aliyun.com/pypi/simple
```

## 键盘模拟

```python
import time
from pywinio import WinIO

# 初始化 WinIO 对象（自动尝试加载驱动）
winio = WinIO()

# 常用键盘扫描码表（PS/2 标准）
SCAN_CODES = {
    'a': 0x1E,      'b': 0x30,      'c': 0x2E,      'd': 0x20,
    'e': 0x12,      'f': 0x21,      'g': 0x22,      'h': 0x23,
    'i': 0x17,      'j': 0x24,      'k': 0x25,      'l': 0x26,
    'm': 0x32,      'n': 0x31,      'o': 0x18,      'p': 0x19,
    'q': 0x10,      'r': 0x13,      's': 0x1F,      't': 0x14,
    'u': 0x16,      'v': 0x2F,      'w': 0x11,      'x': 0x2D,
    'y': 0x15,      'z': 0x2C,
    '0': 0x0B,      '1': 0x02,      '2': 0x03,      '3': 0x04,
    '4': 0x05,      '5': 0x06,      '6': 0x07,      '7': 0x08,
    '8': 0x09,      '9': 0x0A,
    'f1': 0x3B,     'f2': 0x3C,     'f3': 0x3D,     'f4': 0x3E,
    'f5': 0x3F,     'f6': 0x40,     'f7': 0x41,     'f8': 0x42,
    'f9': 0x43,     'f10': 0x44,    'f11': 0x57,    'f12': 0x58,
    'enter': 0x1C,  'esc': 0x01,    'backspace': 0x0E,
    'tab': 0x0F,    'space': 0x39,  'capslock': 0x3A,
    'shift': 0x2A,  'ctrl': 0x1D,   'alt': 0x38,
    'left': 0x4B,   'right': 0x4D,  'up': 0x48,     'down': 0x50
}

def key_down(key_name):
    """按下指定按键"""
    scan_code = SCAN_CODES.get(key_name.lower())
    if scan_code is None:
        raise ValueError(f"不支持的按键: {key_name}")
    winio.key_down(scan_code)

def key_up(key_name):
    """释放指定按键"""
    scan_code = SCAN_CODES.get(key_name.lower())
    if scan_code is None:
        raise ValueError(f"不支持的按键: {key_name}")
    winio.key_up(scan_code)

def press_key(key_name, duration=0.1):
    """按下并释放按键（默认持续0.1秒）"""
    key_down(key_name)
    time.sleep(duration)
    key_up(key_name)

def type_text(text, delay=0.05):
    """输入文本（支持字母和数字）"""
    for char in text.lower():
        if char in SCAN_CODES:
            press_key(char, duration=delay)
        else:
            print(f"跳过不支持字符: {char}")

def hotkey(*keys, duration=0.1):
    """模拟组合键（如 Ctrl+C）"""
    for key in keys:
        key_down(key)
    time.sleep(duration)
    for key in reversed(keys):
        key_up(key)

# 使用示例
if __name__ == "__main__":
    try:
        print("开始模拟键盘输入...")
        
        # 单键操作
        press_key('a')  # 输入字母 a
        time.sleep(1)
        
        # 组合键示例
        hotkey('ctrl', 'c')  # 模拟 Ctrl+C
        time.sleep(1)
        
        # 输入文本
        type_text("Hello World!")
        time.sleep(1)
        
        # 方向键操作
        press_key('right')
        press_key('enter')
        
        print("模拟完成！")
        
    except Exception as e:
        print(f"错误: {e}")
    finally:
        # 清理资源
        if 'winio' in locals():
            winio.__del__()
```