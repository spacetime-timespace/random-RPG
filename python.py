import arcade
import numpy as np
import time

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

        # Time for animation
        t = time.time() - self.start_time

        # Create a NumPy RGB array
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        img[:, :, 0] = (np.sin(t) * 31 + 224).astype(np.uint8)  # Red
        img[:, :, 1] = (np.cos(t) * 31 + 224).astype(np.uint8)  # Green
        img[:, :, 2] = ((np.sin(t * 0.5) + 1) * 31 + 224).astype(np.uint8)  # Blue

        img[x:x+20, y:y+20, :] = 0

        # Convert to Arcade texture and draw
        texture = arcade.Texture(name="rgb_frame", image=arcade.ImageData(WIDTH, HEIGHT, img))
        texture.draw_scaled(WIDTH//2, HEIGHT//2, 1, 1)

    def on_key_press(self,symbol,modifiers):
        if symbol = arcade.key.LEFT:
            if x > 0:
                x -= 1
        if symbol = arcade.key.RIGHT:
            if x < 180:
                x += 1  
        if symbol = arcade.key.UP:
            if y < 180:
                x += 1
        if symbol = arcade.key.DOWN:
            if y > 0:
                x -= 1

if __name__ == "__main__":
    RGBWindow()
    arcade.run()
