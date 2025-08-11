import cv2
import keyboard
import numpy as np
import time

width, height = 200, 200
fps = 120
delay = 1 / fps

while True:
    t = time.time()
    img = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(len(img)):
        for j in range(len(img)):
            img[i][j] = np.sin(i/height) + np.sin(j/width) + np.sin((time.time()/5) % (2*np.pi) )
    cv2.imshow("gyatt", img)
    if keyboard.is_pressed('x')
        break

    time.sleep(delay)

cv2.destroyAllWindows()
