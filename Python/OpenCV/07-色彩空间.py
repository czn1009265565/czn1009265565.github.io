import cv2
import numpy as np

"""
色彩空间
色彩空间(Color Space)指的是表示颜色的一种方式，不同的色彩空间采用不同的方式来描述颜色的三要素
在计算机视觉和图像处理中，了解和转换不同的色彩空间是非常重要的，因为某些操作(例如，目标检测、图像分割、特征提取等)
在某些色彩空间中比在其他色彩空间中特征更为明显

常见的色彩空间主要包括 RGB,BGR,HSV,HLS,Lab,YUV

RGB
RGB 是最常用的色彩空间，尤其是在显示设备(如显示器、电视)中。每种颜色通道(红、绿、蓝)用一个整数值表示，通常是 0 到 255(即 8 位表示)。
该色彩空间直观且易于理解，主要用于显示和图像采集。每个颜色通道的值分别代表图像中的红、绿和蓝的强度。

BGR
BGR 是 OpenCV 中的默认色彩空间。虽然 RGB 更常见，但 OpenCV 默认读取图像为 BGR 格式。这是因为 OpenCV 设计时参考了早期的一些硬件标准。
在 BGR 色彩空间中，蓝色(Blue)是第一个通道，绿色(Green)是第二个通道，红色(Red)是第三个通道。

HSV
HSV 是一种在色彩选择、图像分割和增强中非常常用的色彩空间。它通过三个参数来描述颜色：色调(Hue)、饱和度(Saturation)和明度(Value)。

- 色调(H): 颜色的类型，通常表示为角度，范围为 0° 到 360°，例如，红色为 0°，绿色为 120°，蓝色为 240°
- 饱和度(S): 颜色的纯度或强度，范围是 0 到 100%。0 表示灰色，100% 表示最纯的颜色
- 明度(V): 颜色的亮度或亮度，范围是 0 到 100%。0 表示完全黑色，100% 表示最亮的颜色

在 HSV 空间中，图像的颜色信息更符合人类的视觉感知，通常在图像分割、颜色跟踪等任务中表现优异。

HLS
HLS 色彩空间与 HSV 相似，但将饱和度和亮度的位置交换。HLS 也常用于色彩处理，它比 HSV 更能模拟人眼对颜色的感知

Lab
Lab 是一种基于人类视觉感知的色彩空间，分为三个通道
- L: 亮度（Lightness），范围是 0 到 100，0 表示黑色，100 表示白色。
- a: 绿色到红色的色差，负值表示绿色，正值表示红色。
- b: 蓝色到黄色的色差，负值表示蓝色，正值表示黄色。
Lab 色彩空间的一个重要特点是它是与设备无关的（与显示设备的亮度、对比度等无关），因此在许多图像处理任务中具有很好的稳定性。

YUV
YUV 色彩空间常用于视频编码和广播电视等应用。它将颜色分为亮度分量（Y）和色度分量（U 和 V），因此能够更有效地处理视频图像。
- Y: 亮度分量（Luminance），范围是 0 到 255。
- U 和 V: 色度分量，表示色彩信息，范围是 -128 到 127。

提取特定颜色区域cv2.inRange函数检查每个像素值是否在定义的范围内，如果在这个范围内，则将该像素的值设为255（白色），否则设为0（黑色）
cv2.inRange(src, lowerb, upperb, dst=None)
- src: 源图片
- lowerb: 像素值下边界数组
- upperb: 像素值上边界数组
"""
img_bgr = cv2.imread("cube.jpg")

# 打印图像的尺寸，(height, width, channels)
print(img_bgr.shape)
# 打印图片第一个像素点的颜色值
print('BGR:' + str(img_bgr[0, 0, :]))

# 图片转换为RGB格式
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
print('RGB:' + str(img_rgb[0, 0, :]))

# 图片BGR转换为HSV
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
print('HSV:' + str(img_hsv[0, 0, :]))

# 图片BGR转换为Lab
img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
print('Lab:' + str(img_lab[0, 0, :]))

# 图片BGR转换为YUV
img_yuv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YUV)
print('YUV:' + str(img_yuv[0, 0, :]))

# 分割图片
# 获取指定像素点的颜色值，这里选择(118,130)
bgr = img_bgr[118,130,:]
thresh = 40
# BGR
minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])
maskBGR = cv2.inRange(img_bgr, minBGR, maxBGR)
resultBGR = cv2.bitwise_and(img_bgr, img_bgr, mask=maskBGR)

# HSV
hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
minHSV = np.array([hsv[0] - thresh, hsv[1] - thresh, hsv[2] - thresh])
maxHSV = np.array([hsv[0] + thresh, hsv[1] + thresh, hsv[2] + thresh])
maskHSV = cv2.inRange(img_hsv, minHSV, maxHSV)
resultHSV = cv2.bitwise_and(img_hsv, img_hsv, mask=maskHSV)

# Lab
lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0][0]
minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])
maskLAB = cv2.inRange(img_lab, minLAB, maxLAB)
resultLAB = cv2.bitwise_and(img_lab, img_lab, mask=maskLAB)

cv2.imshow("Result BGR", resultBGR)
cv2.imshow("Result HSV", resultHSV)
cv2.imshow("Output LAB", resultLAB)
cv2.waitKey(0)
cv2.destroyAllWindows()