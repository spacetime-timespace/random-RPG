from PIL import Image,ImageSequence
import numpy as np
from pathlib import Path
def scan(path):
    img = Image.open("Tileset"+path)
    img_array = np.array(img)
    Path("Tileset-parsed"+path).mkdir()
    for i in range(0,img.size[1],16):
        for j in range(0,img.size[0],16):
            tile = img_array[i:i+16, j:j+16]
            x = Image.fromarray(tile)
            x.save("Tileset-parsed"+path+"/tile"+str(int(i/16)*int(img.size[0]/16)+int(j/16))+".png")
def scangif(path):
    img = Image.open("Tileset"+path)
    h,w = img.size
    Path("Tileset-parsed"+path).mkdir()
    for i in range(0,w,16):
        for j in range(0,h,16):
            frames=[]
            it=[f.convert("RGBA") for f in ImageSequence.Iterator(img)]
            for f in it[:-1]:
                tile = np.array(f)[i:i+16,j:j+16]
                frames.append(Image.fromarray(tile))
            frames[0].save("Tileset-parsed"+path+"/tile"+str(int(i/16)*int(img.size[0]/16)+int(j/16))+".gif",save_all=True,append_images=frames[1:],optimize=False,duration=100,loop=0)
def scandir(path):
    target = Path("Tileset"+path)
    for item in target.iterdir():
        if item.suffix == ".png":
            scan(path+"/"+item.name)
        elif item.suffix == ".gif":
            scangif(path+"/"+item.name)
        elif item.suffix == ".txt":
            pass
        else:
            Path("Tileset-parsed"+path+"/"+item.name).mkdir()
            scandir(path+"/"+item.name)
scandir("")