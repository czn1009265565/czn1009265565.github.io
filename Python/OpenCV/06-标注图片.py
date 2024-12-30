import cv2

"""
标注图片

画线
cv2.line(image, start_point, end_point, color, thickness)
- image:       源图片
- start_point: 起始点
- end_point:   结束点
- color:       颜色(BGR)，蓝色(255,0,0) 绿色(0,255,0) 红色(0,0,255)
- thickness:   粗细

画圆
cv2.circle(image, center_coordinates, radius, color, thickness)
- image:              源图片
- center_coordinates: 圆心坐标
- radius:             半径
- color:              颜色(BGR)，蓝色(255,0,0) 绿色(0,255,0) 红色(0,0,255)
- thickness:          粗细，当thickness为-1时，会填充整个区域

画框
cv2.rectangle(image, start_point, end_point, color, thickness)

文本注释
putText(image, text, org, font, fontScale, color)
- image:     源图片
- text:      文本内容
- org:       文本起始左顶点
- font:      字体类型，枚举值见FontEnum
- fontScale: 字体缩放比例
- color:     颜色(BGR)，蓝色(255,0,0) 绿色(0,255,0) 红色(0,0,255)

FontEnum:
  FONT_HERSHEY_SIMPLEX        = 0,
  FONT_HERSHEY_PLAIN          = 1,
  FONT_HERSHEY_DUPLEX         = 2,
  FONT_HERSHEY_COMPLEX        = 3,
  FONT_HERSHEY_TRIPLEX        = 4,
  FONT_HERSHEY_COMPLEX_SMALL  = 5,
  FONT_HERSHEY_SCRIPT_SIMPLEX = 6,
  FONT_HERSHEY_SCRIPT_COMPLEX = 7,
  FONT_ITALIC                 = 16
"""

img = cv2.imread('image.jpg')
if img is None:
    print('Could not read image')

# 展示源图片
cv2.imshow('Original Image', img)

# 画线
# 副本是为了对图像所做的任何更改都不会影响原始图像
imageLine = img.copy()
pointA = (200, 80)
pointB = (450, 80)
cv2.line(imageLine, pointA, pointB, (255, 255, 0), thickness=3)
cv2.imshow('Image Line', imageLine)

# 画圆
imageCircle = img.copy()
circle_center = (415, 190)
radius = 100
cv2.circle(imageCircle, circle_center, radius, (0, 0, 255), thickness=3)
cv2.imshow("Image Circle", imageCircle)

# 填充实心圆
imageFilledCircle = img.copy()
circle_center = (415, 190)
radius = 100
cv2.circle(imageFilledCircle, circle_center, radius, (255, 0, 0), thickness=-1)
cv2.imshow('Image with Filled Circle', imageFilledCircle)

# 画框
imageRectangle = img.copy()
start_point = (300, 115)
end_point = (475, 225)
cv2.rectangle(imageRectangle, start_point, end_point, (0, 0, 255), thickness=3)
cv2.imshow('imageRectangle', imageRectangle)

# 文本注释
imageText = img.copy()
text = 'I am a Happy dog!'
# 文本起始左顶点
org = (50, 350)
# 文本标注
cv2.putText(imageText, text, org, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5, color=(250, 225, 100))
cv2.imshow("Image Text", imageText)
cv2.waitKey(0)
cv2.destroyAllWindows()
