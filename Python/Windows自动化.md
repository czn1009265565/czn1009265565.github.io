# Windows自动化

Python版本3.6.8

### 安装依赖

```
# 自动化工具
pip install -i  https://pypi.tuna.tsinghua.edu.cn/simple pywinauto pywin32 pyautogui
```

### 鼠标控制

#### 获取鼠标位置

```ptthon
import pyautogui

point = pyautogui.position()
x = point.x
y = point.y
```

#### 移动鼠标

```python
# 移动到指定位置 移动到x,y的位置
pyautogui.moveTo(x,y)
pyautogui.moveTo(x,y,duration=1)

# 相对位移,向右移动100px,向下移动500px,持续4秒
pyautogui.moveRel(x,y,duration=0.8)
```

### 鼠标点击

```python
pyautogui.click(10,10) # 鼠标点击指定位置，默认左键
pyautogui.click(10,10,button='left') # 单击左键
pyautogui.click(1000,300,button='right') # 单击右键
pyautogui.click(1000,300,button='middle') # 单击中间

pyautogui.doubleClick(10,10)  # 指定位置，双击左键
pyautogui.rightClick(10,10)   # 指定位置，双击右键
pyautogui.middleClick(10,10)  # 指定位置，双击中键
```

### 键盘控制

```python
pyautogui.press('esc')
pyautogui.press(['left', 'left', 'left'])  # 依次按多个按键
 
# 组合热键（从左到右依次按下按键，再从右到左依次松开按键）
pyautogui.hotkey('ctrl', 'c')
```


### 屏幕处理

```python
im = pyautogui.screenshot()
im.save('screen.png')
```

### 图像识别

```
# 图像识别
pip install -i  https://pypi.tuna.tsinghua.edu.cn/simple opencv-python==4.4.0.46 pytesseract Pillow
```

```python
import random
from time import sleep

import cv2
import pyautogui
import pyscreeze

# 屏幕缩放系数 mac缩放是2 windows一般是1
screenScale = 1
# 睡眠范围
sleepMin = 0.8
sleepMax = 1.5
# 最大空闲时间
keepAliveTime = 360


def random_position(left_top_x, left_top_y, right_bottom_x, right_bottom_y):
    x = random.randint(left_top_x, right_bottom_x)
    y = random.randint(left_top_y, right_bottom_y)
    return x, y


if "__main__" == __name__:
    timer = 0
    # 事先读取按钮截图
    target_list = ["target1.png", "target2.png", "target3.png"]
    target_image = []
    for i in target_list:
        target_image.append(cv2.imread(i, cv2.IMREAD_GRAYSCALE))

    while True:
        if timer >= keepAliveTime:
            print("超过最大空闲时间 程序退出")
            break
        sleep_time = random.uniform(sleepMin, sleepMax)
        # 截图
        pyscreeze.screenshot('screenshot.png')
        # 读取截图
        temp = cv2.imread(r'screenshot.png', cv2.IMREAD_GRAYSCALE)
        for target in target_image:
            theight, twidth = target.shape[:2]
            tempheight, tempwidth = temp.shape[:2]
            # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
            scaleTemp = cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
            stempheight, stempwidth = scaleTemp.shape[:2]
            # 匹配图片
            res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
            mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if (max_val >= 0.9):
                top_left = max_loc
                bottom_right = (top_left[0] + twidth, top_left[1] + theight)
                # 计算出内部随机点
                tagCenterX, tagCenterY = random_position(top_left[0], top_left[1], bottom_right[0], bottom_right[1])
                # 左键点击屏幕上的这个位置
                print("找到目标 X:" + str(tagCenterX) + " Y:" + str(tagCenterY))
                pyautogui.click(tagCenterX, tagCenterY, button='left')  # 点击
                # 点击后重置计时器
                timer = 0
                break
            else:
                print("未找到目标")
        timer += sleep_time
        sleep(sleep_time)
```


### 文字识别

#### 安装 `Tesseract OCR`

1. `Windows Tesseract` 安装包: https://digi.bib.uni-mannheim.de/tesseract/ 下载安装包安装并添加环境变量
2. `Tesseract OCR` github地址: https://github.com/tesseract-ocr/tesseract/ 拷贝中文包`chi_sim.traineddata` 放在`C:\Program Files\Tesseract-OCR\tessdata\`下

