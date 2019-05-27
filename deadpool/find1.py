import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from PIL import Image

obrazek = 'img3.png'

img = cv.imread(obrazek, 0)
img2 = img.copy()
template = cv.imread('img.png', 0)
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR_NORMED',  'cv.TM_SQDIFF_NORMED']


img = img2.copy()
method = eval('cv.TM_CCOEFF')
# Apply template Matching
res = cv.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    top_left = min_loc
else:
    top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv.rectangle(img, top_left, bottom_right, 255, 2)

im = Image.open(obrazek)

fig, ax = plt.subplots(1, sharex='col', sharey='row')
ax.imshow(im)
ax.add_patch(patches.Rectangle((top_left[0], top_left[1]), 150, 125, linewidth=4, edgecolor='green', facecolor='none'))
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])

plt.show()
