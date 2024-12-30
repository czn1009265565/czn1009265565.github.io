import cv2

"""
旋转图片

1.计算旋转变换矩阵
cv2.getRotationMatrix2D(center, angle, scale)
- center: 图像的旋转中心
- angle:  旋转的角度
- scale:  缩放比例系数

2.基于旋转变换矩阵，计算旋转后的图像
cv2.warpAffine(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]])
- src: 源图片
- M: 旋转变换矩阵
- dsize: 输出图片大小
- dst: 输出图片
"""

image = cv2.imread('image.jpg')

# 获取图片中心点
height, width = image.shape[:2]
center = (width / 2, height / 2)

# 获取旋转变换矩阵
rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=45, scale=1)

# 计算旋转后的图像
rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))

cv2.imshow('Original image', image)
cv2.imshow('Rotated image', rotated_image)

cv2.waitKey(0)
# 保存旋转后的图片
cv2.imwrite('rotated_image.jpg', rotated_image)