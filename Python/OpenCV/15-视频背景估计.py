import numpy as np
import cv2
from skimage import data, filters

"""
视频背景估计

背景
对于固定镜头下的视频，包含有少量移动物体，可以通过中值滤波的方式来获得图像的背景图像。
再借助于帧间差可以获得图像中移动物体的掩膜，进一步进行物体检测、跟踪和识别，这样可以有效减少图像计算。
"""

# 读取视频
cap = cv2.VideoCapture('cars.mp4')

# 随机选择25帧
frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)

# 将所选帧存储到数组中
frames = []
for fid in frameIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    frames.append(frame)

# 中值计算
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

# 显示中值计算后的帧
cv2.imshow('frame', medianFrame)
cv2.waitKey(0)

# Reset frame number to 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

# 轮询视频帧
ret = True
while ret:
    # 读取视频帧并转换为灰度图
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 计算当前帧的灰度图与背景帧之间的差异的绝对值
    dframe = cv2.absdiff(frame, grayMedianFrame)
    # 二值化
    th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
    # Display image
    cv2.imshow('frame', dframe)
    cv2.waitKey(20)

# 释放文件
cap.release()
cv2.destroyAllWindows()
