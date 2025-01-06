import cv2

"""
滑动条

cv2.createTrackbar(trackbarName, windowName, value, count, onChange)
- trackbarName (str): 滑动条的名称
- windowName (str): 滑动条所附着的窗口的名称
- value (int): 滑动条的默认值（整数类型）。创建时，滑块位置由此变量定义
- count (int): 滑动条的最大值。注意，滑动条的最小位置始终为 0
- onChange (callable, optional): 回调函数，每次滑动都会调用该函数。该函数通常都会含有一个默认参数，即滑动条的位置。如果未提供，则默认为 None

"""

maxScaleUp = 100
scaleFactor = 1
windowName = "Resize Image"
trackbarValue = "Scale"

# read the image
image = cv2.imread("image.jpg")

# Create a window to display results and  set the flag to Autosize
cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)


def scale_image(*args):
    # 获取比例系数，范围0-100
    scale_factor = 1 + args[0] / 100.0
    # Resize the image
    scaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    cv2.imshow(windowName, scaled_image)


# 创建滑动条
cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, scale_image)

# Display the image
cv2.imshow(windowName, image)
c = cv2.waitKey(0)
cv2.destroyAllWindows()