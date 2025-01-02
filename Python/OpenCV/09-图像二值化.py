import cv2

"""
图像二值化
cv2.threshold是OpenCV库中用于实现图像二值化处理的函数。此函数可以将图像转换为二值图像，
即像素值只包含0和最大值（通常是255）的图像，常用于图像的预处理和特征提取。

ret, dst = cv2.threshold(src, thresh, maxval, type[, dst])
src: 源图像，必须是单通道灰度图像
thresh: 阈值，用于确定像素是否应该被视为前景或背景
maxval: 二值化操作中使用的最大值，通常设为255
type: 阈值类型，定义了多种二值化方法，包括:
    cv2.THRESH_BINARY: 简单二值化
    cv2.THRESH_BINARY_INV: 反向二值化
    cv2.THRESH_TRUNC: 截断二值化，所有高于阈值的像素被设为阈值
    cv2.THRESH_TOZERO: 像素值大于阈值部分不改变,否则设为0
    cv2.THRESH_TOZERO_INV: 像素值大于阈值时设置为0,否则保持不变
    cv2.THRESH_OTSU: 使用Otsu’s方法自动确定阈值
    cv2.THRESH_TRIANGLE: 使用三角方法自动确定阈值
dst:（可选）目标图像，用于存储二值化结果
"""

# 读取灰度图像
src = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)


# 简单二值化，将像素值在0到128范围内的变为255，其余变为0
th, dst = cv2.threshold(src, 0, 128, cv2.THRESH_BINARY)
cv2.imwrite("opencv-thresh-binary-maxval.jpg", dst)

# 简单二值化，将像素值在127到255范围内的变为255，其余变为0
th, dst = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite("opencv-thresh-binary.jpg", dst)

# 反向二值化，将像素值在127到255范围内的变为0，其余变为255
th, dst = cv2.threshold(src, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("opencv-thresh-binary-inv.jpg", dst)

# 截断阈值化，将图像中大于阈值的像素点的值设定为阈值，小于或等于该阈值的像素点的值保持不变，maxValue的值会被忽略
th, dst = cv2.threshold(src, 127, 255, cv2.THRESH_TRUNC)
cv2.imwrite("opencv-thresh-trunc.jpg", dst)

# 像素值大于阈值部分不改变,否则设为0
th, dst = cv2.threshold(src, 127, 255, cv2.THRESH_TOZERO)
cv2.imwrite("opencv-thresh-tozero.jpg", dst)

# 像素值大于阈值时设置为0,否则保持不变
th, dst = cv2.threshold(src, 127, 255, cv2.THRESH_TOZERO_INV)
cv2.imwrite("opencv-thresh-to-zero-inv.jpg", dst)
