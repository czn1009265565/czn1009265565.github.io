import cv2
import numpy as np

"""
图像卷积

图像卷积操作的目的是利用像素点和其邻域像素之前的空间关系，通过加权求和的操作，
实现模糊（blurring），锐化（sharpening），边缘检测（edge detection）等功能。

在图像处理中，卷积核是用于对图像进行滤波的2D矩阵。也称为卷积矩阵，卷积核通常是一个平方的MxN矩阵，
其中M和N都是奇数（例如3×3、5×5、7×7等），因为这样才有一个中心。


图像卷积: 卷积核在图像上按行滑动遍历像素时不断地相乘求和的过程
filter2D(src, ddepth, kernel[, dst[,anchor[,delta[,borderType]]]])
- src:    输入图片
- ddepth: 卷积之后图片的位深，即卷积之后图片的数据类型，一般设为-1，表示和原图类型一致
- kernel: 卷积核，用元组或者ndarray表示，要求数据类型必须是float型

高斯滤波器: 该滤波器执行加权平均，高斯模糊根据像素值与内核中心的距离对像素值进行加权。离中心更远的像素对加权平均值的影响较小
GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]])
- src:    输入图片
- ksize:  卷积核大小
- sigmaX: 水平方向上的高斯核标准差
- sigmaY: 垂直方向上的高斯核标准差

中值模糊
medianBlur(src, ksize)
- src:    输入图片
- ksize:  卷积核大小，必须是一个奇数正整数

双边滤波: 去除噪声的同时，能够保持边缘的清晰度，避免模糊化
bilateralFilter(src, d, sigmaColor, sigmaSpace)
- src: 输入图像，即需要进行滤波处理的图像
- d: 滤波器的直径，必须是正奇数。它决定了滤波器的空间范围
- sigmaColor: 颜色空间滤波器的sigma值。该值越大，颜色滤波的范围越广，即更多的颜色将被混合在一起
- sigmaSpace: 坐标空间滤波器的sigma值。该值越大，空间滤波的范围越广，即更多的像素将被包括在滤波过程中
"""

image = cv2.imread('image.jpg')
if image is None:
    print('Could not read image')

# 使用identity kernel，变换得到的还是原图
kernel1 = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])

identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)

cv2.imshow('Original', image)
cv2.imshow('Identity', identity)

cv2.waitKey()
cv2.destroyAllWindows()

# 使用模糊卷积核
kernel2 = np.ones((5, 5), np.float32) / 25
img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)

cv2.imshow('Kernel Blur', img)

cv2.waitKey()
cv2.destroyAllWindows()

# 使用模糊函数，等同模糊卷积核
img_blur = cv2.blur(src=image, ksize=(5, 5))

cv2.imshow('Blurred', img_blur)

cv2.waitKey()
cv2.destroyAllWindows()

# 使用高斯模糊
gaussian_blur = cv2.GaussianBlur(src=image, ksize=(5, 5), sigmaX=0, sigmaY=0)
cv2.imshow('Gaussian Blurred', gaussian_blur)

cv2.waitKey()
cv2.destroyAllWindows()

# 使用中值模糊
median = cv2.medianBlur(src=image, ksize=5)
cv2.imshow('Median Blurred', median)

cv2.waitKey()
cv2.destroyAllWindows()

# 使用自定义卷积核锐化图片
kernel3 = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
sharp_img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel3)
cv2.imshow('Sharpened', sharp_img)

cv2.waitKey()
cv2.destroyAllWindows()

# 双边滤波
bilateral_filter = cv2.bilateralFilter(src=image, d=9, sigmaColor=75, sigmaSpace=75)
cv2.imshow('Original', image)
cv2.imshow('Bilateral Filtering', bilateral_filter)

cv2.waitKey(0)
cv2.destroyAllWindows()