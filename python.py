import arcade
import arcade.gui
import numpy as np
import time
from PIL import Image

WIDTH = 200
HEIGHT = 200
FPS = 120

x = 0
y = 0

sp = arcade.Sprite()
sp.center_x = 100
sp.center_y = 100
spl = arcade.spriteList()
spl.append(sp)

class RGBWindow(arcade.Window):
    def __init__(self):
        global tex,sp
        super().__init__(WIDTH, HEIGHT, "RGB Animation", update_rate=1/FPS)
        self.start_time = time.time()
        img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8) # Arcade needs RGBA
        im = Image.fromarray(img)
        tex = arcade.Texture(image=im)

    def on_draw(self):
        global text,sp
        arcade.start_render()

        t = time.time() - self.start_time

        img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8) # Arcade needs RGBA
        img[:, :, 0] = (np.sin(t) * 31 + 224).astype(np.uint8)
        img[:, :, 1] = (np.cos(t) * 31 + 224).astype(np.uint8)
        img[:, :, 2] = ((np.sin(t * 0.5) + 1) * 31 + 224).astype(np.uint8)
        img[:, :, 3] = 255

        img[x:x+20, y:y+20, :] = 0

        im = Image.fromarray(img)

        tex.image = im
        sp.texture = tex
        spl.draw()

    def on_key_press(self,symbol,modifiers):
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
                x -= 1

if __name__ == "__main__":
    RGBWindow()
    arcade.run()
