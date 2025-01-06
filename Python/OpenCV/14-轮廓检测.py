import cv2

"""
轮廓检测

背景
使用轮廓检测，我们可以检测物体的边界，并在图像中轻松定位它们。它通常是许多有趣应用的第一步，如图像前景提取、简单图像分割、检测和识别。

什么是轮廓
当我们把物体边缘所有的点连接在一起可以获得轮廓。通常，对于特定的轮廓是指那些具有相同颜色和亮度的边界点像素

检测和绘制轮廓的步骤
1. 读取图像并将其转换为灰度格式  
   将图像转换成单通道的灰度值可以用于后面的阈值处理，这是后面进行轮廓检测的必须步骤
2. 二值化阈值处理  
   在寻找轮廓时，首先对灰度图像应用二值阈值或Canny边缘检测。这将图像转换为黑白，突出显示感兴趣的对象，使轮廓检测算法更容易。
   阈值处理使图像中对象的边界完全变白，所有像素具有相同的强度。该算法现在可以从这些白色像素中检测物体的边界。
3. 检测轮廓  
   使用 findContours() 函数来检测图像中的所有的轮廓
4. 在原图中显示轮廓  
   当轮廓被确定之后，可以使用 drawContours() 函数来在原始图像上重合上轮廓标注曲线
   
查找轮廓
cv2.findContours(image, mode, method)
- image: 输入图像，通常是一个二值图像
- mode: 轮廓检索模式  
  枚举如下:
  - cv2.RETR_EXTERNAL: 只检索最外层的轮廓
  - cv2.RETR_LIST: 检索所有轮廓，并以列表形式返回
  - cv2.RETR_CCOMP: 检索所有轮廓，并以树状结构（contour hierarchy）形式返回。此时，轮廓被分为不同的层级
  - cv2.RETR_TREE: 检索所有轮廓，并以完整的树状结构形式返回
- method: 轮廓近似方法
  枚举如下:
  - cv2.CHAIN_APPROX_NONE: 存储轮廓上的所有点
  - cv2.CHAIN_APPROX_SIMPLE: 压缩水平、垂直和对角方向的轮廓点
  - cv2.CHAIN_APPROX_TC89_L1 和 cv2.CHAIN_APPROX_TC89_KCOS: 使用Teh-Chini chain近似算法


绘制轮廓
cv2.drawContours(image, contours, contourIdx, color, thickness=None, lineType=None, hierarchy=None, maxLevel=None, offset=None)
- image: 需要绘制轮廓的目标图像，注意会改变原图
- contours: 轮廓点，上述函数cv2.findContours()的第一个返回值
- contourIdx: 轮廓的索引，表示绘制第几个轮廓，-1表示绘制所有的轮廓
- color: 绘制轮廓的颜色
- thickness:（可选参数）轮廓线的宽度，-1表示填充
- lineType:（可选参数）轮廓线型，包括cv2.LINE_4,cv2.LINE_8（默认）,cv2.LINE_AA,分别表示4邻域线，8领域线，抗锯齿线（可以更好地显示曲线）
- hierarchy:（可选参数）层级结构，上述函数cv2.findContours()的第二个返回值，配合maxLevel参数使用
- maxLevel:（可选参数）等于0表示只绘制指定的轮廓，等于1表示绘制指定轮廓及其下一级子轮廓，等于2表示绘制指定轮廓及其所有子轮廓
- offset:（可选参数）轮廓点的偏移量
"""

image = cv2.imread('image.jpg')
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 应用二值化，像素值大于150将被转换成255(白色)，其余则转换成0(黑色)
ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
# 展示二值化处理后的图像
# cv2.imshow('Binary image', thresh)
# cv2.waitKey(0)

# 查找轮廓图
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_TC89_KCOS)

# 绘制轮廓
image_copy = image.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                 lineType=cv2.LINE_AA)

# see the results
cv2.imshow('None approximation', image_copy)
cv2.waitKey(0)

cv2.destroyAllWindows()

