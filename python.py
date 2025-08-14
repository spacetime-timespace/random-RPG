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
        self.sp = arcade.Sprite()
        self.sp.center_x = 100
        self.sp.center_y = 100
        arcade.start_render()
        self.spl = arcade.SpriteList()
        self.spl.append(self.sp)
        self.x = 0
        self.y = 0

    def on_draw(self):

        t = time.time() - self.start_time
        self.img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8) # Arcade needs RGBA
        self.img[:, :, 0] = (np.sin(t) * 31 + 224).astype(np.uint8)
        self.img[:, :, 1] = (np.cos(t) * 31 + 224).astype(np.uint8)
        self.img[:, :, 2] = ((np.sin(t * 0.5) + 1) * 31 + 224).astype(np.uint8)
        self.img[:, :, 3] = 255

        self.img[self.x:self.x+20, self.y:self.y+20, :3] = 0

        self.im = Image.fromarray(self.img)

        self.tex.image = self.im
        self.sp.texture = self.tex
        self.spl.draw()

    def on_key_press(self,symbol,modifiers):
        if symbol == arcade.key.LEFT:
            if self.x > 0:
                self.x -= 1
        if symbol == arcade.key.RIGHT:
            if self.x < 180:
                self.x += 1  
        if symbol == arcade.key.UP:
            if self.y < 180:
                self.y += 1
        if symbol == arcade.key.DOWN:
            if self.y > 0:
                self.y -= 1
def main():
    window = Game()
    arcade.run()
main()
