import arcade
import time
from math import floor
from random import random,randint,sample
import numpy as np
WORLDX = 240
WORLDY = 240
worldmap = [[24 for _ in range(WORLDY)] for _ in range(WORLDX)]
worldmap[0][0] = 23

house1 = [list(range(153+i,81+i,-18)) for i in range(5)]
house2 = [list(range(84+i,-6+i,-18)) for i in range(6)]
g = 5
roads = {
    0:24,
    1:28,
    2:29,
    3:26,
    4:10,
    5:46,
    6:9,
    7:44,
    8:11,
    9:27,
    10:47,
    11:62,
    12:8,
    13:45,
    14:63,
    15:24,
}
items = [23,56,57,58,59,60,61,72,73,74,75,76,77,78,90,91,92,93,94]
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-=\\!@#$%^&*()_+|[]{};:'\",.<>/?~` "
key=dict(zip(list(chars),list(range(len(chars)))))

for i in range(24):
    for j in range(240):
        worldmap[10*i+8][j] = roads[5]
for i in range(24):
    for j in range(240):
        if 0 < (j+2)%20 < 10:
            worldmap[j][10*i+6]=roads[10]
        if 10 < (j+2)%20 < 20:
            worldmap[j][10*i+7]=roads[10]
        if (j+2)%20==0:
            worldmap[j][10*i+7]=roads[13]
            worldmap[j][10*i+6]=roads[7]
        if (j+2)%20==10:
            worldmap[j][10*i+6]=roads[13]
            worldmap[j][10*i+7]=roads[7]

for i in range(24):
    for j in range(24):
        prob = np.e**(-0.01*((i-12)**2+(j-12)**2))/2
        x = random()
        if x < prob:
            for i1 in range(5):
                for j1 in range(4):
                    worldmap[10*i+i1][10*j+j1] = house1[i1][j1]
            worldmap[10*i+3][(10*j-1)%240] = roads[4]
            worldmap[10*i+3][(10*j-2)%240] = roads[5]
            if i%2==0:
                worldmap[10*i+3][(10*j-3)%240] = roads[5]
                worldmap[10*i+3][(10*j-4)%240] = roads[11]
            else:
                worldmap[10*i+3][(10*j-3)%240] = roads[11]
            while random()>0.2:
                k = sample(items,1)[0]
                xp = randint(5,7)
                yp = randint(-1,5)
                worldmap[10*i+xp][(10*j+yp)%240]=k
        elif x < 2 * prob:
            for i1 in range(6):
                for j1 in range(5):
                    worldmap[10*i+i1][10*j+j1] = house2[i1][j1]
            worldmap[10*i+1][(10*j-1)%240] = roads[4]
            worldmap[10*i+1][(10*j-2)%240] = roads[5]
            if i%2==0:
                worldmap[10*i+1][(10*j-3)%240] = roads[5]
                worldmap[10*i+1][(10*j-4)%240] = roads[11]
            else:
                worldmap[10*i+1][(10*j-3)%240] = roads[11]
            while random()>0.2:
                k = sample(items,1)[0]
                xp = randint(6,7)
                yp = randint(-1,5)
                worldmap[10*i+xp][(10*j+yp)%240]=k
text=[(0,0.5,g,"Hello!",3,320,80,1),
      (1+g,1,g,"Game speaking.",3,320,80,1),
      (2.5+2*g,2,g,"Welcome to the simulation.",3,320,80,1),
      (5+3*g,1.5,g,"Arrow keys to move.",3,320,80,1),
      (7+4*g,2,g,"Space to toggle compass.",3,320,80,1),
      (9.5+5*g,3.5,g,"Keys 1234567890-= to move through inventory",3,320,80,0.75),
      (13.5+6*g,5,g,"Enter to carry/put down stuff from different slots of your inventory",3,320,80,0.5),
      (19+7*g,2.5,g,"Shift+Enter to carry only half.",3,320,80,1),
      (22+8*g,2.5,g,"Click to place/collect items.",3,320,80,1)]
 #(start time, write time, display time, text, font, center x, center y, size/16)
def format(n,sp=3,dp=2):
    x = str(n).split(".")
    if len(x[0])>sp:
        p1 = x[0][-sp:]
    else:
        p1 = "0"*(sp-len(x[0]))+x[0]
    if len(x[1])>dp:
        p2 = x[1][:dp]
    else:
        p2 = x[1]+"0"*(dp-len(x[1]))
    return p1+"."+p2
def find_texture(dir,frame,pos):
    return arcade.load_texture("Tileset-parsed/Char_Sprites/char_"+pos+"_"+dir+"_anim_strip_6.png/tile"+str(frame)+".png")
def find_tile(idx):
    return arcade.load_texture("Tileset-parsed/Overworld_Tileset.png/tile"+str(idx)+".png")
def find_glyph(font,char):
    return arcade.load_texture("Fonts-parsed/B"+str(font)+".png/tile"+str(key[char])+".png")
class GameView(arcade.Window):
    def __init__(self):
        super().__init__(640,480,"RPG",resizable=True)
    def on_resize(self,width,height):
        self.w = width
        self.h = height
        self.x *= (self.w+self.h)/35/self.tilesize
        self.y *= (self.w+self.h)/35/self.tilesize
        self.tilesize = (self.w+self.h)/35
        self.hspl = arcade.SpriteList()
        for i in range(12):
            z = arcade.Sprite()
            z.center_x = self.w-48
            z.center_y = self.h/2-176+32*i
            z.scale = 2
            z.texture = arcade.load_texture("Tileset-parsed/Hud_Ui/item_box_hud.png/tile0.png")
            self.hspl.append(z)
        self.char.center_x = self.w/2
        self.char.center_y = self.h/2
        self.char.scale = self.tilesize/16
        self.tiles=[arcade.Sprite() for _ in range(int(np.ceil(self.w/self.tilesize+1)*np.ceil(self.h/self.tilesize+1)))]
        self.spl = arcade.SpriteList()
        self.spl.extend(self.tiles)
    def setup(self):
        self.tilesize = 32
        self.w = 640
        self.h = 480
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
        self.texts = [[] for _ in text]
        self.spls = [arcade.SpriteList() for _ in text]
        self.comp = False
        self.cpt = []
        self.cts = arcade.SpriteList()
        self.slot = 0
        self.slct = arcade.Sprite()
        self.slct.center_x = 560
        self.slct.scale = 2
        self.slct.texture = arcade.load_texture("Tileset-parsed/Hud_Ui/select_icon_ui.png/tile0.png")
        self.inv = [[3,73],[2,58],[1,73],[2,58],[2,58],[0,73],[3,73],[2,58],[4,73],[0,73],[1,73],[4,58]]
        self.invspl = arcade.SpriteList()
        self.carrying = None
    def on_draw(self):
        self.clear()
        self.char.texture = find_texture(self.dir,self.frame,self.pos)
        for i in zip(range(int(np.ceil(self.w/self.tilesize+1)*np.ceil(self.h/self.tilesize+1))),self.tiles):
            idx = i[0]
            t = i[1]
            t.center_x = idx%int(np.ceil(self.w/self.tilesize+1))*self.tilesize+(self.tilesize/2)-self.x%self.tilesize
            t.center_y = int(idx//int(np.ceil(self.w/self.tilesize+1)))*self.tilesize+(self.tilesize/2)-self.y%self.tilesize
            t.scale = self.tilesize/16
            t.texture = find_tile(24)
        self.spl.draw()
        for i in zip(range(int(np.ceil(self.w/self.tilesize+1)*np.ceil(self.h/self.tilesize+1))),self.tiles):
            idx = i[0]
            t = i[1]
            t.center_x = idx%int(np.ceil(self.w/self.tilesize+1))*self.tilesize+(self.tilesize/2)-self.x%self.tilesize
            t.center_y = int(idx//int(np.ceil(self.w/self.tilesize+1)))*self.tilesize+(self.tilesize/2)-self.y%self.tilesize
            t.scale = self.tilesize/16
            t.texture = find_tile(worldmap[int(np.round(idx%int(np.ceil(self.w/self.tilesize+1))+self.x//self.tilesize)%WORLDX)][int(np.round(int(idx//int(np.ceil(self.w/self.tilesize+1)))+self.y//self.tilesize)%WORLDY)])
        self.spl.draw()
        for i in self.spls:
            i.draw()
        if self.comp:
            self.cps.draw()
        arcade.draw_sprite(self.char)
        self.hspl.draw()
        arcade.draw_sprite(self.slct)
        self.invspl.draw()
    def on_update(self, delta):
        ct = time.time()-self.start
        self.x = (self.x+5*self.tilesize * self.xv * delta) % (WORLDX * self.tilesize)
        self.y = (self.y+5*self.tilesize * self.yv * delta) % (WORLDY * self.tilesize)
        ts = [worldmap[floor(i[0]+np.ceil(self.w/self.tilesize+1)/2-1/2+self.x//self.tilesize)%WORLDX][floor(i[1]+np.ceil(self.h/self.tilesize+1)/2-1/2+self.y//self.tilesize)%WORLDY] for i in zip(range(-1,2),range(-1,2))]
        target = set([8,9,10,11,26,27,28,29,44,45,46,47,62,63])
        if len(set(ts).intersection(target)) != 0:
            self.x = (self.x+5*self.tilesize * self.xv * delta) % (WORLDX * self.tilesize)
            self.y = (self.y+5*self.tilesize * self.yv * delta) % (WORLDY * self.tilesize)
        self.frame = int((ct*12)%6)
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
        for i in range(len(text)):
            self.spls[i] = arcade.SpriteList()
            self.texts[i]=[]
            if ct < text[i][0] or ct > text[i][0]+text[i][1]+text[i][2]:
                pass
            else:
                for j in range(len(text[i][3])):
                    if (ct-text[i][0])*len(text[i][3])>=j*text[i][1]:
                        pos_x = text[i][5]+16*(-text[i][7]/2*len(text[i][3])+text[i][7]/2+text[i][7]*j)
                        z = arcade.Sprite()
                        z.scale = text[i][7]
                        z.center_x = pos_x
                        z.center_y = text[i][6]
                        z.texture = find_glyph(text[i][4],text[i][3][j])
                        self.spls[i].append(z)
                        self.texts[i].append(z)
        if self.comp:
            self.cps = arcade.SpriteList()
            self.cpt = []
            tx = "("+format(str(self.x/32+10))+", "+format(str(self.y/32+7.5))+")"
            for j in range(len(tx)):
                pos_x = self.w/2+16*(-1/2*len(tx)+1/2+j)
                z = arcade.Sprite()
                z.scale = 1
                z.center_x = pos_x
                z.center_y = 40
                z.texture = find_glyph(3,tx[j])
                self.cps.append(z)
                self.cpt.append(z)
        self.slct.center_y=self.h/2-176+32*self.slot
        if self.carrying == None:
            self.slct.center_x = self.w-80
        else:
            self.slct.center_x = self.w-96
        self.invspl = arcade.SpriteList()
        for i in zip(self.inv,list(range(12))):
            tx = format(float(i[0][0]),2,0)[:-1]
            for j in range(len(tx)):
                pos_x = self.w-48+16*(-1/4*len(tx)+1/4+j/2)
                z = arcade.Sprite()
                z.scale = 0.5
                z.center_x = pos_x
                z.center_y = self.h/2-168+32*i[1]
                z.texture = find_glyph(1,tx[j])
                self.invspl.append(z)
            if i[0][0] != 0:
                z = arcade.Sprite()
                z.scale = 1
                z.center_x = pos_x
                z.center_y = self.h/2-176+32*i[1]
                z.texture = find_tile(i[0][1])
                self.invspl.append(z)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.xv-=1
        if key == arcade.key.RIGHT:
            self.xv+=1
        if key == arcade.key.DOWN:
            self.yv-=1
        if key == arcade.key.UP:
            self.yv+=1
        if key == arcade.key.SPACE:
            self.comp = not self.comp
        if key == arcade.key.KEY_1:
            self.slot = 0
        if key == arcade.key.KEY_2:
            self.slot = 1
        if key == arcade.key.KEY_3:
            self.slot = 2
        if key == arcade.key.KEY_4:
            self.slot = 3
        if key == arcade.key.KEY_5:
            self.slot = 4
        if key == arcade.key.KEY_6:
            self.slot = 5
        if key == arcade.key.KEY_7:
            self.slot = 6
        if key == arcade.key.KEY_8:
            self.slot = 7
        if key == arcade.key.KEY_9:
            self.slot = 8
        if key == arcade.key.KEY_0:
            self.slot = 9
        if key == arcade.key.MINUS:
            self.slot = 10
        if key == arcade.key.EQUAL:
            self.slot = 11
        if key == arcade.key.ENTER:
            if modifiers == arcade.key.MOD_SHIFT:
                if self.carrying == None:
                    self.carrying = (np.floor(self.inv[self.slot][0]/2),self.inv[self.slot][1])
                    self.inv[self.slot] = [np.ceil(self.inv[self.slot][0]/2),self.inv[self.slot][1]]
                elif self.carrying[1] == self.inv[self.slot][1] or self.inv[self.slot][0] == 0:
                    n1 = (self.inv[self.slot][0]+np.floor(self.carrying[0]/2),self.carrying[1])
                    self.carrying = [np.ceil(self.inv[self.slot][0]/2),self.carrying[1]]
                    self.inv[self.slot] = n1
            else:
                if self.carrying == None:
                    self.carrying = (self.inv[self.slot][0],self.inv[self.slot][1])
                    self.inv[self.slot] = [0,self.inv[self.slot][1]]
                elif self.carrying[1] == self.inv[self.slot][1] or self.inv[self.slot][0] == 0:
                    self.inv[self.slot] = [self.inv[self.slot][0]+self.carrying[0],self.carrying[1]]
                    self.carrying = None
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.xv+=1
        if key == arcade.key.RIGHT:
            self.xv-=1
        if key == arcade.key.DOWN:
            self.yv+=1
        if key == arcade.key.UP:
            self.yv-=1
    def on_mouse_press(self,x,y,button,modifiers):
        mouse_x = int(np.floor((self.x+x)/self.tilesize))%WORLDX
        mouse_y = int(np.floor((self.y+y)/self.tilesize))%WORLDY
        if worldmap[mouse_x][mouse_y] == 24 and self.inv[self.slot][0] > 0:
            self.inv[self.slot][0] -= 1
            worldmap[mouse_x][mouse_y] = self.inv[self.slot][1]
        elif worldmap[mouse_x][mouse_y] in items and (self.inv[self.slot][0] == 0 or self.inv[self.slot][1] == worldmap[mouse_x][mouse_y]):
            self.inv[self.slot][0] += 1
            self.inv[self.slot][1] = worldmap[mouse_x][mouse_y]
            worldmap[mouse_x][mouse_y] = 24

def main():
    window = GameView()
    window.setup()
    arcade.run()

    
main()
