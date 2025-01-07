import cv2
import numpy as np

"""
剪裁图片

img[start_row:end_row, start_col:end_col]
"""
img = cv2.imread('image.jpg')
print(img.shape)
cv2.imshow("original", img)

# 剪裁图片
cropped_image = img[80:280, 150:330]

# 展示剪裁后的图片
cv2.imshow("cropped", cropped_image)

# 保存剪裁后的图片
cv2.imwrite("Cropped Image.jpg", cropped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
