import cv2
import numpy as np

#reading image pixel values
pixels = cv2.imread('image.png')
print(pixels)

# creating image using pixels GBR value
array = np.array([
 [[255,0 , 0],
  [255 ,255 ,255],
  [255, 255 ,255],
  [187,41 ,160]],
[[255,0 , 0],
  [0 ,255 ,255],
  [21, 255 ,74],
  [4,0 ,89]],

])

cv2.imwrite('crearted_img.png',array)