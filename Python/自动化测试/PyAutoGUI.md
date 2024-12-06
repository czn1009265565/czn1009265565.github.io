# PyAutoGUI
PyAutoGUI是一个纯Python的GUI自动化工具，其目的是可以用程序自动控制鼠标和键盘操作，多平台支持（Windows，OS X，Linux）

PyAutoGUI的主要功能有：

- 移动鼠标并单击其他应用程序的窗口
- 向应用程序发送击键信号，如填写表格
- 截取屏幕截图，并给出一个图像（例如，按钮或复选框的图像），然后在屏幕上找到它
- 找到应用程序的窗口，移动、调整大小、最大化、最小化或关闭它（目前仅适用于 Windows）
- 显示警报和消息框

安装
```shell
pip install pyautogui -i https://mirrors.aliyun.com/pypi/simple
```
## 基础知识

屏幕上的位置由X和Y笛卡尔坐标表示。X坐标从左侧的0开始，向右增加。
与数学不同，Y坐标从顶部的0开始，向下增加。左上角的像素位于坐标(0, 0)。
如果您的屏幕分辨率为 1920 x 1080，则右下角的像素将为(1919, 1079)，因为坐标从0开始，而不是1。
坐标系如下所示。
```
0,0       X increases -->
+---------------------------+
|                           | Y increases
|                           |     |
|   1920 x 1080 screen      |     |
|                           |     V
|                           |
|                           |
+---------------------------+ 1919, 1079
```

## 一般函数
屏幕分辨率大小由size()函数作为两个整数的元组返回。
鼠标光标的当前X和Y坐标由position()函数返回。

```python
# 获取当前鼠标位置
print(pyautogui.position())
# 获取当前屏幕的分辨率
print(pyautogui.size())
# 判断某个坐标是否在屏幕上
print(pyautogui.onScreen(10, 10))
```

## 故障保证
在每次调用PyAutoGUI的函数后设置1秒的暂停
```python
# 暂停1s
pyautogui.PAUSE = 1
```
此外，为了防止程序出问题，当鼠标移动到屏幕左上角，
会引发 `pyautogui.FailSafeException` 错误进而中止程序。关闭命令如下（不建议关闭）:

```python
pyautogui.FAILSAFE = False
```

## 鼠标函数

### 鼠标移动
```python
# 用num_seconds(秒)将鼠标移动到(x,y)位置
x = 200
y = 100
num_seconds = 1
pyautogui.moveTo(x, y, duration=num_seconds)  

# 用num_seconds(秒)将鼠标从当前位置向右移动xOffset，向下移动yOffset
# 如果duration为0或未指定，则立即移动。
xOffset = 30
yOffset = -50
num_seconds = 0.5
pyautogui.moveRel(xOffset, yOffset, duration=num_seconds) 
```

### 鼠标拖动
```python
# 用num_seconds(秒)将鼠标推动到(x,y)位置
# 鼠标拖动是指按下鼠标左键移动鼠标。
x = 200
y = 100
num_seconds= 1
pyautogui.dragTo(x, y, duration=num_seconds)  

# 用num_seconds(秒)将鼠标从当前位置向右拖动xOffset，向下推动yOffset
xOffset = 30
yOffset = -50
num_seconds = 0.5
pyautogui.dragRel(xOffset, yOffset, duration=num_seconds) 
```

### 鼠标单击

```python
# 将鼠标移动到(moveToX,moveToY)位置，点击鼠标num_of_clicks次，每次点击间隔secs_between_clicks秒
# button表示单击方式，'left'左键单击，'middle'中键单击，'right'右键单击
moveToX = 500
moveToY = 600
num_of_clicks = 1
secs_between_clicks = 1
pyautogui.click(x=moveToX, y=moveToY, clicks=num_of_clicks, interval=secs_between_clicks, button='left')
```

### 鼠标滚动

```python
moveToX = 100
moveToY = 200
# 鼠标在当前位置向下滑动100格
# pyautogui.scroll(clicks=-100)
# 鼠标移动到(moveToX,moveToY)位置，然后向上滚动150格
pyautogui.scroll(clicks=150, x=moveToX, y=moveToY)
```

### 鼠标按下
```python
# 鼠标移动到(moveToX,moveToY)位置，鼠标左键按下
pyautogui.mouseDown(x=moveToX, y=moveToY, button='left')
# 鼠标移动到(moveToX,moveToY)位置，鼠标右键松开（按下右键的情况下）
pyautogui.mouseUp(x=moveToX, y=moveToY, button='right')
# 鼠标在当前位置，按下中键
pyautogui.mouseDown(button='middle')
```

## 键盘函数

### 文字输入

键盘控制文字输入的主要函数就是typewrite()/write()。这个函数可以实现字符输入，可以用interval参数设置两次输入间时间间隔。
```python
# 在当前位置输入文字text，每个字符输入间隔secs_between_keys秒
# \n表示换行
text = 'Hello world!\n'
secs_between_keys = 0.1
pyautogui.typewrite(message=text, interval=secs_between_keys)  
# 在当前位置按下键盘各种键
pyautogui.typewrite(['\t', 'a', 'b', 'c', 'left', 'backspace', 'enter', 'f1','\n'], interval=secs_between_keys)
# 查看所有支持按键
print(pyautogui.KEYBOARD_KEYS)
```

### 快捷键
```python
# ctrl+c 复制文字
pyautogui.hotkey('ctrl', 'c')  
# ctrl+v 粘贴文字
pyautogui.hotkey('ctrl', 'v') 

# 按下ctrl键
pyautogui.keyDown('ctrl')
# 按下v键，相当文字粘贴
pyautogui.keyDown('v')
# 松开ctrl键盘
pyautogui.keyUp('ctrl')
```

### hold()上下文管理器

```python
# 按住shift
with pyautogui.hold('shift'):
    # 连续按left,然后松开shift
    pyautogui.press(['left', 'left', 'left'])

# 上面代码功能和下面代码实现功能相同
# 按下shift键
pyautogui.keyDown('shift')
pyautogui.press('left')
pyautogui.press('left')
pyautogui.press('left')
# 松开shift键
pyautogui.keyUp('shift')
```

## 消息框函数
如果你需要暂停程序直到用户点击确定，或者想向用户显示一些信息，可以使用消息框函数。这里消息框函数的使用方式和javascript一样。
```python
# 警告窗口
alert_result = pyautogui.alert('点击确定返回字符串OK')
# 确认窗口
confirm_result = pyautogui.confirm('点击确定返回字符串OK，点击取消返回字符串Cancel')
# 点击ok保存输入的文字，点击Cancel返回None
prompt_result = pyautogui.prompt('输入文字')
# 点击ok保存输入的密码，点击Cancel返回None
# default默认文字，mask用什么符号代替输入的密码
password_result = pyautogui.password(text='', title='', default='', mask='*')
```

## 截图函数
PyAutoGUI使用Pillow/PIL库实现图像的处理。在Linux上，您必须运行以下命令安装scrot库才能使用屏幕截图功能。
```shell
sudo apt-get install scrot
```

```python
# 截屏返回result对象
result = pyautogui.screenshot()
# result是PIL中的Image对象
print(type(result))
# 保存图像
result.save('result.jpg')
# 展示图片
#result.show()

# imageFilename参数设置文件保存为止，在截屏前保存图片到本地foo.png文件
# region设置截图区域[x,y,w,h]，以(x,y)为左上角顶点，截宽w，高h的区域
result = pyautogui.screenshot(imageFilename='result2.jpg',region=[10,20,100,50])
```

## 图像定位

```python
# 在屏幕返回和result.jpg图片类似的区域坐标，返回值(左上角x坐标，左上角y坐标，宽度，高度)
# 如果没找到返回None
result = pyautogui.locateOnScreen('result.jpg')
# 在屏幕返回和result.jpg图片类似的区域中间位置的XY坐标,confidence返回区域最低置信度
result = pyautogui.locateCenterOnScreen('result.jpg', confidence=0.9)
# 为查找图片找到的所有位置返回一个生成器
results = pyautogui.locateAllOnScreen('result.jpg', confidence=0.6)
print(results)
# 打印各组的(左上角x坐标，左上角y坐标，宽度，高度)
for i in results:
    print(i)
# 将结果保存为list
list_result = list(pyautogui.locateAllOnScreen('result.jpg', confidence=0.6)

# 在haystackImage中，返回和image图片最类似区域的坐标
result = pyautogui.locate(needleImage='result.jpg', haystackImage='result.jpg', confidence=0.5)
# 在haystackImage中，返回和image图片所有类似区域的坐标(left, top, width, height)
result = pyautogui.locateAll(needleImage='result.jpg', haystackImage='result.jpg', confidence=0.5)
```

这些“定位”功能相当昂贵；他们可能需要整整几秒钟的时间才能运行。加速它们的最好方法是传递一个region参数（一个（左、上、宽、高）的4整数元组）来只搜索屏幕的较小区域而不是全屏。
但是这个region区域必须比待搜索截图区域大，否则会引发错误。

```python
result = pyautogui.locateOnScreen('result1.jpg', region=(0,0, 300, 400))
result = pyautogui.locate(needleImage='result1.jpg', haystackImage='result.jpg', confidence=0.5, region=(0,0, 300, 400))
```