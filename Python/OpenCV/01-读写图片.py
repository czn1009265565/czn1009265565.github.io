import cv2

"""
读取、展示、保存图片
- imread(filename, flags=None)        读取图片，返回一个BGR形式的图像对象，其类型为一个numpy数组。flags枚举见ImreadModes
- imshow(winname, mat)                展示图片
- imwrite(filename, img, params=None) 保存图片


ImreadModes 图片读取模式分为以下三种
  - cv2.IMREAD_COLOR      默认参数，以彩色模式读取图像，忽略 alpha 通道。对应的数值是 1
  - cv2.IMREAD_GRAYSCALE  以灰度模式读取图像，将图像转换为单通道灰度图像。对应的数值是 0
  - cv2.IMREAD_UNCHANGED  读取包括 alpha 通道（透明度）在内的所有图像信息。对于带有 alpha 通道的图像（如 PNG 图像），将保持完整信息。对应的数值是 -1
"""

if __name__ == "__main__":
    # 读取图片
    img_color = cv2.imread('Resources/p1.jpg', 1)
    img_grayscale = cv2.imread('Resources/p1.jpg', 0)
    img_alpha = cv2.imread('Resources/p1.jpg', -1)

    # 展示图片
    cv2.imshow('graycsale image', img_grayscale)

    # 等待用户按键触发，waitKey(0)代表按任意键继续
    cv2.waitKey(0)

    # 销毁全部窗口
    cv2.destroyAllWindows()

    # 保存图片
    cv2.imwrite('grayscale.jpg', img_grayscale)