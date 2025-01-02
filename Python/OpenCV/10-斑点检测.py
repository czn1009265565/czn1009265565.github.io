import cv2
import numpy as np

"""
斑点检测
用于在图像中检测和定位简单的二值化斑点（blob），可以帮助我们在图像处理和计算机视觉任务中找到感兴趣的斑点或物体

"""
im = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
# 基于默认参数初始化检测器
detector = cv2.SimpleBlobDetector_create()
# 检测斑点
keypoints = detector.detect(im)

# 使用红色圆标准检测到的斑点
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

# 自定义SimpleBlobDetector参数
params = cv2.SimpleBlobDetector_Params()

# 设置最小阈值与最大阈值
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 1500

# 设置圆度
params.filterByCircularity = True
params.minCircularity = 0.1

# 设置凸性
params.filterByConvexity = True
params.minConvexity = 0.87

# 设置惯性比
params.filterByInertia = True
params.minInertiaRatio = 0.01

# 初始化SimpleBlobDetector
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)
# 检测斑点
keypoints = detector.detect(im)

# 使用红色圆标准检测到的斑点
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)