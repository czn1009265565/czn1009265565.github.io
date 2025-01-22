# Keyboard

Python的`keyboard`模块是一个用于模拟键盘按键输入和监听键盘事件的第三方库，
但需要注意的是 `keyboard` 本身并不是驱动级的键鼠模拟工具。

功能:

- 模拟按键输入: 模拟按键事件，如按下，释放，或者同时按下多个键等
- 监听键盘事件: 监听全局键盘事件，包括捕获特定键的按下或释放，记录所有键盘输入，以及来执行特定的回调函数

安装: `pip install keyboard`

## 模拟按键

```python
import keyboard

# 模拟文字输入
keyboard.write("Hello World!")

# 模拟按键按下
keyboard.press("a")
keyboard.press("ctrl+c")

# 模拟按键释放
keyboard.release("a")
keyboard.release("ctrl+c")

# 模拟按键按下并释放 press_and_release等同于send
keyboard.press_and_release("a")
keyboard.press_and_release("ctrl+c")
```

## 事件监听
监听按键并打印
```python
import keyboard


def on_press_reaction(event):
    print(event.name)


keyboard.on_press(on_press_reaction)

keyboard.wait("esc")
```

监听热键

```python
import keyboard


def hotkey_reaction():
    print("触发回调函数")


# 设置热键，例如alt+b
keyboard.add_hotkey("alt+a", hotkey_reaction)

keyboard.wait("esc")
```