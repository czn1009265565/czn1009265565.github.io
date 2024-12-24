import cv2
import numpy as np

"""
图像缩放

resize(src, dsize[, dst[, fx[, fy[, interpolation]]]])

src: 输入图片源
dsize: 目标大小 (w,h)
fx: x轴比例
fy: y轴比例
interpolation: 图像缩放的方法
  - INTER_LINEAR‌：双线性插值，适用于大多数情况，提供较好的图像质量
  - INTER_NEAREST‌：最近邻插值，处理速度快，但图像质量较低
  - INTER_AREA‌：适用于图像缩小，使用像素区域相似度的方法进行插值
  - INTER_CUBIC‌：双三次插值，适用于高精度要求的情况
  - INTER_LANCZOS4‌：Lanczos插值，适用于放大图像时提供较高的图像质量
"""

if __name__ == "__main__":
    # 读取图片
    image = cv2.imread('Resources/book.jpg')
    cv2.imshow('Original Image', image)
    h, w, c = image.shape
    print("原始图片 宽:%s 高:%s" % (w, h))

    # 图片缩小
    down_width = 300
    down_height = 200
    down_points = (down_width, down_height)
    resized_down = cv2.resize(image, down_points, interpolation=cv2.INTER_LINEAR)

    # 图片放大
    up_width = 600
    up_height = 400
    up_points = (up_width, up_height)
    resized_up = cv2.resize(image, up_points, interpolation=cv2.INTER_LINEAR)

    # Display images
    cv2.imshow('Resized Down by defining height and width', resized_down)
    cv2.waitKey()
    cv2.imshow('Resized Up image by defining height and width', resized_up)
    cv2.waitKey()

    # press any key to close the windows
    cv2.destroyAllWindows()
