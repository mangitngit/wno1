from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature

# otworzenie obrazu
obraz = Image.open("aas.jpg")
obraz_dane = np.array(obraz)

# przypisanie odpowiednich wartosci RGB
czerwony, czerw_ilosc = np.unique(obraz_dane[:, :, 0], return_counts=True)
zielony, ziel_ilosc = np.unique(obraz_dane[:, :, 1], return_counts=True)
niebieski, nieb_ilosc = np.unique(obraz_dane[:, :, 2], return_counts=True)

# Model YUV
szary_czerwony = np.array(obraz)[:, :, 0] * 0.299
szary_zielony = np.array(obraz)[:, :, 1] * 0.587
szary_niebieski = np.array(obraz)[:, :, 2] * 0.114
skala_szarosci = szary_czerwony + szary_zielony + szary_niebieski

szary, szar_ilosc = np.unique(skala_szarosci, return_counts=True)
szary_obraz = Image.fromarray(skala_szarosci)

# Canny
canny = feature.canny(skala_szarosci, sigma=20)

# Krzyż Robertsa
in_im_x_y = np.delete(np.delete(skala_szarosci, 1, axis=0), 1, axis=1)
in_im_x1_y1 = np.delete(np.delete(skala_szarosci, -1, axis=0), -1, axis=1)

in_im_x1_y = np.delete(np.delete(skala_szarosci, 1, axis=0), -1, axis=1)
in_im_x_y1 = np.delete(np.delete(skala_szarosci, -1, axis=0), 1, axis=1)

tmp1 = in_im_x_y - in_im_x1_y1
tmp2 = in_im_x1_y - in_im_x_y1
krzyz = np.abs(tmp1) + np.abs(tmp2)

# rysowanie wykresow
fig, ax = plt.subplots(2, 3)

ax[0, 0].set_title("Oryginalny obraz")
ax[0, 0].imshow(obraz)
ax[0, 0].axis("off")

ax[0, 1].set_title("Obraz czarno-biały")
ax[0, 1].imshow(szary_obraz)
ax[0, 1].axis("off")

ax[0, 2].set_title("Canny")
ax[0, 2].imshow(canny, cmap=plt.cm.gray)
ax[0, 2].axis("off")

# obliczenie liczby pikseli, do znormalizowania histogramu
width, high = obraz.size
ilosc_pixeli = width * high

ax[1, 0].set_title("Histogram RGB")
ax[1, 0].plot(czerwony, czerw_ilosc / ilosc_pixeli, "r")
ax[1, 0].plot(zielony, ziel_ilosc / ilosc_pixeli, "g")
ax[1, 0].plot(niebieski, nieb_ilosc / ilosc_pixeli, "b")

ax[1, 1].set_title("Histogram odcieni szarosci")
ax[1, 1].plot(szary, szar_ilosc / ilosc_pixeli, "k")

ax[1, 2].set_title("Krzyż Robertsa")
ax[1, 2].imshow(krzyz, cmap=plt.cm.gray)
ax[1, 2].axis("off")

plt.show()
