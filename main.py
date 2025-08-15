import arcade
import arcade.gui
import numpy as np
import time
from PIL import Image

WIDTH = 200
HEIGHT = 200
FPS = 120

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "RGB Animation", update_rate=1/FPS)
        self.start_time = time.time()
        self.tex = arcade.Texture(image = Image.fromarray(np.zeros((HEIGHT,WIDTH,4),dtype = np.uint8)))
        self.x = 0
        self.y = 0
        t0 = time.time() - self.start_time
        self.img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8) # Arcade needs RGBA
        self.img[:, :, 0] = (np.sin(np.pi*t0) * 31 + 224).astype(np.uint8)
        self.img[:, :, 1] = (np.sin(np.pi*2/3+np.pi*t0*3/4) * 31 + 224).astype(np.uint8)
        self.img[:, :, 2] = (np.sin(np.pi*4/3+np.pi*t0*3/5) * 31 + 224).astype(np.uint8)
        self.img[:, :, 3] = 255
        x = int(self.x)
        y = int(self.y)
        self.img[x:x+20, y:y+20, :3] = 0

        self.im = Image.fromarray(self.img)
        self.sp = arcade.Sprite(self.im,1)
        self.sp.center_x = 100
        self.sp.center_y = 100
        self.spl = arcade.SpriteList()
        self.spl.append(self.sp)
        self.key = []

    def on_draw(self):

        t0 = time.time() - self.start_time
        self.img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8) # Arcade needs RGBA
        self.img[:, :, 0] = (np.sin(np.pi*t0) * 31 + 224).astype(np.uint8)
        self.img[:, :, 1] = (np.sin(np.pi*2/3+np.pi*t0*3/4) * 31 + 224).astype(np.uint8)
        self.img[:, :, 2] = (np.sin(np.pi*4/3+np.pi*t0*3/5) * 31 + 224).astype(np.uint8)
        self.img[:, :, 3] = 255
        x = int(self.x)
        y = int(self.y)
        self.img[x:x+20, y:y+20, :3] = 0

        self.im = Image.fromarray(self.img)
        self.tex = arcade.Texture(self.im)
        self.sp.texture = self.tex
        self.clear()
        self.spl.draw()

    def on_key_press(self,key,modifiers):
        self.key.append(key)
    def on_key_release(self,key,modifiers):
        self.key.remove(key)
    def on_update(self,delta_time):
        key = self.key
        if arcade.key.LEFT in key:
            if self.y > 100*delta_time:
                self.y -= 100*delta_time
        if arcade.key.RIGHT in key:
            if self.y < 180-100*delta_time:
                self.y += 100*delta_time
        if arcade.key.DOWN in key:
            if self.x < 180-100*delta_time:
                self.x += 100*delta_time
        if arcade.key.UP in key:
            if self.x > 100*delta_time:
                self.x -= 100*delta_time
def main():
    window = Game()
    arcade.run()
main()
