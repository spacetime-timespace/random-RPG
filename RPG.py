import arcade
import time
from math import floor
from random import random
import numpy as np
WORLDX = 240
WORLDY = 240
worldmap = [[24 for _ in range(WORLDY)] for _ in range(WORLDX)]
worldmap[0][0] = 23

house1 = [list(range(153+i,81+i,-18)) for i in range(5)]
house2 = [list(range(84+i,-6+i,-18)) for i in range(6)]


for i in range(24):
    for j in range(24):
        prob = np.e**(-0.01*((i-12)**2+(j-12)**2))/2
        x = random()
        if x < prob:
            for i1 in range(5):
                for j1 in range(4):
                    worldmap[10*i+i1][10*j+j1] = house1[i1][j1]
        elif x < 2 * prob:
            for i1 in range(6):
                for j1 in range(5):
                    worldmap[10*i+i1][10*j+j1] = house2[i1][j1]



def find_texture(dir,frame,pos):
    return arcade.load_texture("Tileset-parsed/Char_Sprites/char_"+pos+"_"+dir+"_anim_strip_6.png/tile"+str(frame)+".png")
def find_tile(idx):
    return arcade.load_texture("Tileset-parsed/Overworld_Tileset.png/tile"+str(idx)+".png")
class GameView(arcade.Window):
    def __init__(self):
        super().__init__(640,480,"RPG")
    def setup(self):
        self.x = 0
        self.y = 0
        self.xv = 0
        self.yv = 0
        self.char = arcade.Sprite()
        self.char.center_x = 320
        self.char.center_y = 240
        self.char.scale = 2
        self.dir = "down"
        self.pos = "idle"
        self.start = time.time()
        self.frame = 0
        self.tiles=[arcade.Sprite() for _ in range(21*16)]
        for i in self.tiles:
            i.scale = 2
        self.spl = arcade.SpriteList()
        self.spl.extend(self.tiles)
    def on_draw(self):
        self.clear()
        self.char.texture = find_texture(self.dir,self.frame,self.pos)
        for i in zip(range(21*16),self.tiles):
            idx = i[0]
            t = i[1]
            t.center_x = idx%21*32+16-self.x%32
            t.center_y = int(idx//21)*32+16-self.y%32
            t.texture = find_tile(24)
        self.spl.draw()
        for i in zip(range(21*16),self.tiles):
            idx = i[0]
            t = i[1]
            t.texture = find_tile(worldmap[(idx%21+floor(self.x//32))%WORLDX][(int(idx//21)+floor(self.y//32))%WORLDY])
        self.spl.draw()
        arcade.draw_sprite(self.char)
    def on_update(self, delta):
        self.x += (160 * self.xv * delta) % (WORLDX * 32)
        self.y += (160 * self.yv * delta) % (WORLDY * 32)
        self.frame = int(((time.time()-self.start)*12)%6)
        if self.xv == 0 and self.yv == 0:
            self.pos = "idle"
        else:
            self.pos = "run"
            if self.xv == -1:
                self.dir = "left"
            elif self.xv == 1:
                self.dir = "right"
            elif self.yv == -1:
                self.dir = "down"
            elif self.yv == 1:
                self.dir = "up"
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.xv-=1
        if key == arcade.key.RIGHT:
            self.xv+=1
        if key == arcade.key.DOWN:
            self.yv-=1
        if key == arcade.key.UP:
            self.yv+=1
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.xv+=1
        if key == arcade.key.RIGHT:
            self.xv-=1
        if key == arcade.key.DOWN:
            self.yv+=1
        if key == arcade.key.UP:
            self.yv-=1

def main():
    window = GameView()
    window.setup()
    arcade.run()

    
main()
