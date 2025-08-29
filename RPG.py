import arcade
import time
from math import floor
from random import random,randint,sample
import numpy as np
WORLDX = 240
WORLDY = 240
worldmap = [[24 for _ in range(WORLDY)] for _ in range(WORLDX)]
worldmap[0][0] = 23

#TODO talk to NPCs

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
people = []
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
            people.append([10*i+3, (10*j-1)%240, 0, 0, 0, 0, randint(1,2)/2])
            while random() > 3/4:
                people.append([10*i+3, (10*j-1)%240, 0, 0, 0, 0, randint(1,2)/2])
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
            people.append([10*i+1, (10*j-1)%240, 0, 0, 0, 0, randint(1,2)/2])
            while random() > 3/4:
                people.append([10*i+1, (10*j-1)%240, 0, 0, 0, 0, randint(1,2)/2])
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
text=[]
text=[lambda s:("NI0",0.5,"Hello! (Press H to continue)",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI1",1,"Game speaking.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI2",2,"Welcome to the simulation.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI3",1.5,"Arrow keys to move.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI4",2,"Space to toggle compass.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI5",3.5,"Keys 1234567890-= to move through inventory",3,s.w/2,2.5*s.tilesize,3*s.tilesize/128),
      lambda s:("NI6",5,"Enter to carry/put down stuff from different slots of your inventory",3,s.w/2,2.5*s.tilesize,s.tilesize/64),
      lambda s:("NI7",2.5,"Shift+Enter to carry only half.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI8",2.5,"Click to place/collect items.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("NI9",4.5,"Press E to interact with an NPC or continue a conversation.",3,s.w/2,2.5*s.tilesize,s.tilesize/64),
      lambda s:("NI10",2.5,"Press H to restart this.",3,s.w/2,2.5*s.tilesize,s.tilesize/32),
      lambda s:("C0",2,"Nice to meet you!",2,s.w/2,4.5*s.tilesize,s.tilesize/32)]
sw = []
 #(start time, write time, display time, text, font, center x, center y, size/16)
#(start time, triggers, options, text, font, center x, center y, size/16)
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
            z.center_x = self.w-1.5*self.tilesize
            z.center_y = self.h/2-5.5*self.tilesize+self.tilesize*i
            z.scale = self.tilesize/16
            z.texture = arcade.load_texture("Tileset-parsed/Hud_Ui/item_box_hud.png/tile0.png")
            self.hspl.append(z)
        self.char.center_x = self.w/2
        self.char.center_y = self.h/2
        self.char.scale = self.tilesize/16
        self.tiles=[arcade.Sprite() for _ in range(int(np.ceil(self.w/self.tilesize+1)*np.ceil(self.h/self.tilesize+1)))]
        self.spl = arcade.SpriteList()
        self.spl.extend(self.tiles)
        self.slct.scale = self.tilesize/16
        self.swch = [-1 for _ in sw]
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
        self.ot = 0
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
        self.slct.texture = arcade.load_texture("Tileset-parsed/Hud_Ui/select_icon_ui.png/tile0.png")
        self.inv = [[3,73],[2,58],[1,73],[2,58],[2,58],[0,73],[3,73],[2,58],[4,73],[0,73],[1,73],[4,58]]
        self.invspl = arcade.SpriteList()
        self.carrying = None
        self.swin = 0
        self.mem = {
            "NI0" : self.start,
            "NI1" : None,
            "NI2" : None,
            "NI3" : None,
            "NI4" : None,
            "NI5" : None,
            "NI6" : None,
            "NI7" : None,
            "NI8" : None,
            "NI9" : None,
            "NI10" : None,
            "C0" : None
        }
        self.npcs = people[:]
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
        for i in self.npcs:
            j = arcade.Sprite()
            a = ((i[0] + i[2]) * self.tilesize - self.x)%(WORLDX*self.tilesize)
            b = ((i[1] + i[3]) * self.tilesize - self.y)%(WORLDY*self.tilesize)
            j.center_x = a
            j.center_y = b
            j.scale = self.tilesize/16 * i[6]
            j.texture = arcade.load_texture("Tileset-parsed/Char_Sprites/char_idle_down_anim_strip_6.png/tile"+str(self.frame)+".png")
            arcade.draw_sprite(j)
        arcade.draw_sprite(self.char)
        self.hspl.draw()
        arcade.draw_sprite(self.slct)
        self.invspl.draw()

    def on_update(self, delta):
        ct = time.time()-self.start
        if ct > self.ot + 0.05:
            self.ot = ct
            for i in range(len(self.npcs)):
                self.npcs[i][4] *= 0.9
                self.npcs[i][5] *= 0.9
                self.npcs[i][4] += random()*1-0.5
                self.npcs[i][5] += random()*1-0.5
        for i in range(len(self.npcs)):
            self.npcs[i][2] += self.npcs[i][4] * delta
            self.npcs[i][3] += self.npcs[i][5] * delta
            if self.npcs[i][2]**2+self.npcs[i][3]**2>9:
                self.npcs[i][2] -= self.npcs[i][4] * delta
                self.npcs[i][3] -= self.npcs[i][5] * delta
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
            t = text[i](self)
            if self.mem[t[0]] != None:
                for j in range(len(t[2])):
                    if (time.time()-self.mem[t[0]])*len(t[2])>=j*t[1]:
                        pos_x = t[4]+16*(-t[6]/2*len(t[2])+t[6]/2+t[6]*j)
                        z = arcade.Sprite()
                        z.scale = t[6]
                        z.center_x = pos_x
                        z.center_y = t[5]
                        z.texture = find_glyph(t[3],t[2][j])
                        self.spls[i].append(z)
                        self.texts[i].append(z)
        for i in range(len(sw)):
            t = sw[i](self)
            if self.mem[t[0]] != None:
                if self.mem[t[0]] > self.swch[i]:
                    te = t[2][self.swin%len(t[2])]
                    for j in range(len(te)):
                        pos_x = t[4]+16*(-t[6]/2*len(te)+t[6]/2+t[6]*j)
                        z = arcade.Sprite()
                        z.scale = t[6]
                        z.center_x = pos_x
                        z.center_y = t[5]
                        z.texture = find_glyph(t[3],te[j])
                        self.spls[i].append(z)
                        self.texts[i].append(z)

                
        if self.comp:
            self.cps = arcade.SpriteList()
            self.cpt = []
            tx = "("+format(str(self.x/self.tilesize+10))+", "+format(str(self.y/self.tilesize+7.5))+")"
            for j in range(len(tx)):
                pos_x = self.w/2+16*(-1/2*self.tilesize/32*len(tx)+1/2+j*self.tilesize/32)
                z = arcade.Sprite()
                z.scale = self.tilesize/32
                z.center_x = pos_x
                z.center_y = 1.25*self.tilesize
                z.texture = find_glyph(3,tx[j])
                self.cps.append(z)
                self.cpt.append(z)
        self.slct.center_y=self.h/2-5.5*self.tilesize+self.tilesize*self.slot
        if self.carrying == None:
            self.slct.center_x = self.w-2.5*self.tilesize
        else:
            self.slct.center_x = self.w-3*self.tilesize
        self.invspl = arcade.SpriteList()
        for i in zip(self.inv,list(range(12))):
            tx = format(float(i[0][0]),2,0)[:-1]
            for j in range(len(tx)):
                pos_x = self.w-1.5*self.tilesize+self.tilesize/2*(-1/4*len(tx)+1/4+j/2)
                z = arcade.Sprite()
                z.scale = self.tilesize/64
                z.center_x = pos_x
                z.center_y = self.h/2-5.5*self.tilesize+self.tilesize*i[1]+self.tilesize/4
                z.texture = find_glyph(1,tx[j])
                self.invspl.append(z)
            if i[0][0] != 0:
                pos_x = self.w-1.5*self.tilesize
                z = arcade.Sprite()
                z.scale = 1
                z.center_x = pos_x
                z.center_y = self.h/2-5.5*self.tilesize+self.tilesize*i[1]
                z.scale = self.tilesize/32
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
        if key == arcade.key.E:
            if self.mem["C0"] != None:
                self.mem["C0"] = None
            for i in self.npcs:
                a = i[0]+i[2]
                b = i[1]+i[3]
                if ((a-self.x/self.tilesize-self.w/2/self.tilesize+120)%240-120)**2+((b-self.y/self.tilesize-self.h/2/self.tilesize+120)%240-120)**2 <= 8:
                    self.mem["C0"]=time.time()
        #SWITCHES
        if key == arcade.key.X:
            self.swin -= 1
        if key == arcade.key.C:
            self.swin += 1
        if key == arcade.key.Z:
            for i in range(len(sw)):
                z = sw[i](self)
                if self.mem[z[0]] != None:
                    if self.mem[z[0]] > self.swch[i]:
                        self.swch[i] = self.mem[z[0]]
                        self.mem[z[1][self.swin%len(z[1])]] = 1
        #MEMORY
        ct = time.time()
        m=self.mem
        if key == arcade.key.H:
            if m["NI10"] != None:
                m["NI10"] = None
            if m["NI9"] != None:
                m["NI9"] = None
                m["NI10"] = ct
            elif m["NI8"] != None:
                m["NI8"] = None
                m["NI9"] = ct
            elif m["NI7"] != None:
                m["NI7"] = None
                m["NI8"] = ct
            elif m["NI6"] != None:
                m["NI6"] = None
                m["NI7"] = ct
            elif m["NI5"] != None:
                m["NI5"] = None
                m["NI6"] = ct
            elif m["NI4"] != None:
                m["NI4"] = None
                m["NI5"] = ct
            elif m["NI3"] != None:
                m["NI3"] = None
                m["NI4"] = ct
            elif m["NI2"] != None:
                m["NI2"] = None
                m["NI3"] = ct
            elif m["NI1"] != None:
                m["NI1"] = None
                m["NI2"] = ct
            elif m["NI0"] != None:
                m["NI0"] = None
                m["NI1"] = ct
            else:
                m["NI0"] = ct
        self.mem = m
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
