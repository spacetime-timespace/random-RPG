import arcade

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(480,360,"RPG")
    def setup(self):
        pass
    def on_draw(self):
        self.clear()
    def on_update(self, delta):
        passimport arcade
import time
def find_texture(dir,frame,pos):
    return arcade.load_texture("Tileset-parsed/Char_Sprites/char_"+pos+"_"+dir+"_anim_strip_6.png/tile"+str(frame)+".png")
class GameView(arcade.Window):
    def __init__(self):
        super().__init__(480,360,"RPG")
    def setup(self):
        self.x = 0
        self.y = 0
        self.xv = 0
        self.yv = 0
        self.char = arcade.Sprite()
        self.char.center_x = 240
        self.char.center_y = 180
        self.char.scale = 4
        self.dir = "down"
        self.pos = "idle"
        self.start = time.time()
        self.frame = 0
    def on_draw(self):
        self.clear()
        self.char.texture = find_texture(self.dir,self.frame,self.pos)
        arcade.draw_sprite(self.char)
    def on_update(self, delta):
        self.x += 3 * self.xv * delta
        self.y += 3 * self.yv * delta
        self.frame = int(((time.time()-self.start)*6)%6)
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
    def on_key_press(self, key, modifiers):
        pass
    def on_key_release(self, key, modifiers):
        pass

def main():
    window = GameView()
    window.setup()
    arcade.run()

    
if __name__ == "__main__":
    main()
