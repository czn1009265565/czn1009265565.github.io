import cv2

"""
鼠标与轨迹条

设置鼠标回调函数
cv2.setMouseCallback(windowName, onMouse, param=None)
- windowName: 窗口名称，需要先通过 cv2.namedWindow() 函数创建
- onMouse: 回调函数，用于处理鼠标事件。当在 windowName 指定的窗口中发生鼠标事件时，该函数将被调用。
  该函数需要接收五个参数
  - event: 整数类型，表示鼠标事件类型（如左键点击、右键点击等）
  - x: 整数类型，表示鼠标事件发生的 x 坐标（以像素为单位）
  - y: 整数类型，表示鼠标事件发生的 y 坐标（以像素为单位）
  - flags: 整数类型，表示鼠标事件的标志（如鼠标按键状态、鼠标拖动状态等）
  - param: 可选参数，传递给回调函数的附加数据（如果有的话）
"""
top_left_corner = []
bottom_right_corner = []


def draw_rectangle(action, x, y, flags, *userdata):
    """
    绘制矩形
    """
    global top_left_corner, bottom_right_corner
    # Mark the top left corner when left mouse button is pressed
    if action == cv2.EVENT_LBUTTONDOWN:
        top_left_corner = [(x, y)]
        # When left mouse button is released, mark bottom right corner
    elif action == cv2.EVENT_LBUTTONUP:
        bottom_right_corner = [(x, y)]
        # Draw the rectangle
        cv2.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0, 255, 0), 2, 8)
        cv2.imshow("Window", image)


def click_annotate(action, x, y, flags, *userdata):
    """
    绘制点击的坐标点
    """
    if action == cv2.EVENT_LBUTTONDOWN:
        xy = "[%d,%d]" % (x, y)
        cv2.circle(image, (x, y), 3, (0, 0, 255), thickness=-1)
        cv2.putText(image, xy, (x, y), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=[0, 0, 255])
        cv2.imshow("Window", image)


# 读取图片
image = cv2.imread("image.jpg")
# 拷贝图片作为备份
backup = image.copy()
# 创建名为Window的窗口
cv2.namedWindow("Window")
# 设置鼠标回调函数
cv2.setMouseCallback("Window", draw_rectangle)

k = 0
# 按q关闭窗口
while k != 113:
    # 展示图片
    cv2.imshow("Window", image)
    k = cv2.waitKey(0)
    # 按c复原图片
    if k == 99:
        image = backup.copy()
        cv2.imshow("Window", image)

cv2.destroyAllWindows()
