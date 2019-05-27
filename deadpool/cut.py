from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import *

im = Image.open("src_0.png")
szer, wys = im.size

image_without = np.array(Image.open("src_0.png").convert("RGBA"))
image_with = np.array(Image.open("src_1.png").convert("RGBA"))

maska = image_without
result = image_with

for i in range(wys):
    for j in range(szer):
        if maska[i, j, 0] != image_with[i, j, 0] or maska[i, j, 1] != image_with[i, j, 1] or maska[i, j, 2] != \
                image_with[i, j, 2]:
            maska[i, j] = image_with[i, j]
            maska[i, j, 3] = 255

            result[i, j] = 255
            result[i, j, 3] = 255
        else:
            maska[i, j] = 0
            result[i, j] = 0

wsp_post = Image.fromarray(maska).getbbox()

postac = maska[wsp_post[1]:wsp_post[3], wsp_post[0]:wsp_post[2]]
result = result[wsp_post[1]:wsp_post[3] + 1, wsp_post[0]:wsp_post[2] + 1]

he = Image.fromarray(postac)
he.save("hehe.png", "PNG")

x1, y1, x2, y2 = (wsp_post[0], wsp_post[1], wsp_post[2], wsp_post[3])
width = x2 - x1
height = y2 - y1

for i in range(height):
    for j in range(width):
        postac[i, j] = result[i, j - 1] * postac[i, j]
        postac[i, j] = result[i, j + 1] * postac[i, j]
        postac[i, j] = result[i - 1, j] * postac[i, j]
        postac[i, j] = result[i + 1, j] * postac[i, j]

he = Image.fromarray(postac)
he.save("hehe2.png", "PNG")

# plt.figure(1)
# plt.imshow(postac)

##############################
# fig, ax = plt.subplots(1, sharex='col', sharey='row')

# im = Image.open("src_1.png")
# ax.imshow(im)
# ax.add_patch(patches.Rectangle((x1, y1), width, height, linewidth=4, edgecolor='white', facecolor='none'))


######################################################################
######################################################################


heroR, heroG, heroB, heroA = Image.fromarray(postac).split()

mhist = Image.fromarray(postac).histogram(mask=heroR)
mhistA, mhistAbins = np.histogram(postac, bins=255 * 3)

im = Image.open('img5.png')

sizey, sizex = im.size
xjump, yjump = int(width / 2), int(height / 2)
imA = np.array(im)
value = np.zeros([ceil(sizex / xjump), ceil(sizey / yjump)])
for x in range(0, sizex, xjump):
    for y in range(0, sizey, yjump):
        bmp = imA[x:x + width, y:y + height]
        h, hbins = np.histogram(bmp, bins=255 * 3)
        r = np.array(h) - np.array(mhistA)
        p = np.dot(r, r)
        value[int(x / xjump), int(y / yjump)] = p

posx, posy = np.unravel_index(value.argmin(), value.shape)

fig1, ax1 = plt.subplots(1, sharex='col', sharey='row')
# Display the image
ax1.imshow(im)
# Add a Rectangle patch
x1, y1, x2, y2 = (posy * yjump, posx * xjump, posy * yjump + height, posx * xjump + width)
width = x2 - x1
height = y2 - y1
ax1.add_patch(patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='green', facecolor='none'))

plt.show()
