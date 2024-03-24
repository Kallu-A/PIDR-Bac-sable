import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('./img.png')
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


assert img is not None, "file could not be read, check with os.path.exists()"
# hist = cv2.calcHist([img],[0],None,[256],[0,256])
# plt.hist(img.ravel(),256,[0,256]); plt.show()


ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

cv2.imshow('thresh', thresh)
cv2.waitKey()



