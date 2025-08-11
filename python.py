import cv2
import keyboard
import numpy as np
import time

width, height = 200, 200
fps = 30
delay = 1 / fps

while True:
    # Create a changing RGB image (moving color gradient)
    t = time.time()
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :, 0] = (np.sin(t) * 127 + 128).astype(np.uint8)  # Blue channel
    img[:, :, 1] = (np.cos(t) * 127 + 128).astype(np.uint8)  # Green channel
    img[:, :, 2] = ((np.sin(t * 0.5) + 1) * 127).astype(np.uint8)  # Red channel

    # Show image
    cv2.imshow("RGB Animation", img)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(delay)  # Keep ~30 FPS

cv2.destroyAllWindows()
