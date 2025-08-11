import arcade
import numpy as np
import time
from PIL import Image

WIDTH = 200
HEIGHT = 200
FPS = 120

x = 0
y = 0

class RGBWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "RGB Animation", update_rate=1/FPS)
        self.start_time = time.time()

    def on_draw(self):
        arcade.start_render()

        t = time.time() - self.start_time

        img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8) # Arcade needs RGBA
        img[:, :, 0] = (np.sin(t) * 31 + 224).astype(np.uint8)
        img[:, :, 1] = (np.cos(t) * 31 + 224).astype(np.uint8)
        img[:, :, 2] = ((np.sin(t * 0.5) + 1) * 31 + 224).astype(np.uint8)
        img[:, :, 3] = 0.astype(np.uint8)

        img[x:x+20, y:y+20, :] = 0

        im = Image.fromarray(img)

        texture = arcade.Texture(name="thing", image=im)
        texture.draw_scaled(WIDTH//2, HEIGHT//2, 1, 1)

    '''def on_key_press(self,symbol,modifiers):
        global x,y
        if symbol == arcade.key.LEFT:
            if x > 0:
                x -= 1
        if symbol == arcade.key.RIGHT:
            if x < 180:
                x += 1  
        if symbol == arcade.key.UP:
            if y < 180:
                x += 1
        if symbol == arcade.key.DOWN:
            if y > 0:
                x -= 1'''

if __name__ == "__main__":
    RGBWindow()
    arcade.run()
