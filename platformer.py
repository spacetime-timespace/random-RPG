import arcade

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(480,360,"RPG")
    def setup(self):
        pass
    def on_draw(self):
        self.clear()
    def on_update(self, delta):
        pass
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