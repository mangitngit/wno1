from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import *

postac_im = Image.open("hehe2.png").convert("RGB")
postac_y, postac_x = postac_im.size

postac = np.array(postac_im)
mhistA, mhistAbins = np.histogram(postac, bins=255*3)

im = Image.open('img3.png')
im_y, im_x = im.size

print(postac_x, postac_y)
print(im_x, im_y)

xjump, yjump = int(postac_x/4), int(postac_y/5)

im_array = np.array(im)
value = np.zeros([ceil(im_x/xjump), ceil(im_y/yjump)])

for x in range(0, im_x, xjump):
    for y in range(0, im_y, yjump):
        bmp = im_array[x:x+postac_x, y:y+postac_y]
        h, hbins = np.histogram(bmp, bins=255*3)
        roznica = np.array(h) - np.array(mhistA)
        value[int(x/xjump), int(y/yjump)] = np.dot(roznica, roznica)

posx, posy = np.unravel_index(value.argmin(), value.shape)

fig1, ax1 = plt.subplots(1, sharex='col', sharey='row')

ax1.imshow(im)

x1, y1, x2, y2 = (posy*yjump, posx*xjump, posy*yjump+postac_y, posx*xjump+postac_x)
width = x2 - x1
height = y2 - y1

ax1.add_patch(patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='green', facecolor='none'))

plt.show()
