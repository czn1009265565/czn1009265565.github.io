import cv2

"""
边缘检测

背景
- 特征提取: 边缘是图像中亮度变化最显著的部分，它们通常对应于物体的轮廓、不同区域的边界等。
  通过边缘检测，可以从图像中提取出这些重要的特征信息，为后续处理如图像分割、目标识别等提供基础
- 图像简化: 边缘检测后的图像往往比原始图像更为简洁，只保留了重要的边缘信息，去除了大量冗余的像素点。
  这种简化有助于减少计算量，提高处理速度，并使得图像更易于分析和理解
- 结构分析: 边缘检测可以帮助我们分析图像中的结构信息，如物体的形状、大小、方向等。这些信息对于图像理解、场景重建等任务至关重要

检测原理
- 灰度变化: 边缘检测的基本原理是基于图像中局部区域与周围区域之间的灰度变化。当图像中存在灰度变化时，这种变化通常被视为边缘。
- 梯度计算: 为了检测这些灰度变化，边缘检测算法会计算图像中每个像素点或其邻域的灰度梯度。梯度是一个向量，它反映了亮度变化的方向和速率。
  梯度的幅值（大小）表示亮度变化的强度，而梯度的方向则指出了亮度变化的方向。在实际应用中，梯度可以通过不同的算法来计算，如Sobel算子、Prewitt算子等。
  这些算法通过应用特定的卷积核（或模板）到图像上，来计算每个像素点的梯度。
- 阈值处理: 计算得到梯度后，通常需要进行阈值处理来进一步确定哪些像素点属于边缘。阈值处理通过比较梯度幅值与预设的阈值来判断该点是否为边缘点。
  如果梯度幅值大于阈值，则认为该点是边缘点；否则，认为该点是非边缘点。
- 非极大值抑制: 为了进一步细化边缘，部分边缘检测算法（如Canny边缘检测算法）会采用非极大值抑制技术。
  非极大值抑制会沿着梯度的方向检查每个像素点，如果当前像素点的梯度幅值不是其邻域内的局部最大值，则将该点标记为非边缘点。
- 边缘连接: 在某些情况下，边缘检测算法还会进行边缘连接，以将断开的边缘片段连接起来，形成完整的边缘轮廓。


Sobel边缘检测算法
cv2.Sobel(src, ddepth, dx, dy)
- src: 输入图像，通常为灰度图像
- ddepth: 输出图像的深度（即数据类型）。常用的深度有:
  cv2.CV_8U: 8位无符号整数（用于存储图像数据）
  cv2.CV_16S: 16位有符号整数（常用于表示梯度值）
  cv2.CV_32F: 32位浮动数据类型（当需要更高精度时使用）
  cv2.CV_64F: 64位浮动数据类型（当需要更高精度时使用）
- dx: 

Canny边缘检测算法，方法本身就综合了高斯降噪，计算梯度，抑制假边，滞后阈值。
cv2.Canny(image, threshold1, threshold2)
- src: 输入图像，通常为灰度图像
- threshold1: 小阈值
- threshold2: 大阈值

如果梯度幅度值高于较大的阈值，则这些像素与实心边缘相关联，并包含在最终的边缘图中。
如果梯度幅度值低于较小的阈值，则像素将被抑制并从最终的边缘图中排除。
梯度幅度落在这两个阈值之间的所有其他像素都被标记为“弱”边缘（即它们成为最终边缘图中包含的候选者）。
如果“弱”像素连接到与实边关联的像素，它们也将包含在最终的边缘图中
"""


img = cv2.imread('image.jpg')
cv2.imshow('Original', img)
cv2.waitKey(0)

# 转换为灰度图像
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 高斯模糊减少噪声
img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

# Sobel边缘检测
# 计算X轴方向上的梯度
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
# 计算Y轴方向上的梯度
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
# 组合X轴与Y轴方向上的梯度
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
# 展示
cv2.imshow('Sobel X', sobelx)
cv2.waitKey(0)
cv2.imshow('Sobel Y', sobely)
cv2.waitKey(0)
cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
cv2.waitKey(0)

# Canny边缘检测
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
cv2.imshow('Canny Edge Detection', edges)
cv2.waitKey(0)

cv2.destroyAllWindows()