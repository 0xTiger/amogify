from skimage import io
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input')
args = parser.parse_args()

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

img = io.imread(args.input) / 255
if img.shape[-1] == 3:
    img = np.concatenate([img, np.ones((img.shape[0], img.shape[1], 1))], axis=2)

contains_amogi_mask = np.zeros_like(img)
out_img = img * np.array([1, 1, 1, 0.9])

img_width, img_height, img_depth = img.shape
amogi = np.array([
    [1, 1, 1, 0],
    [0.5, 0.5, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 0],
    [1, 0, 1, 0]
])
amogi = np.stack([amogi]*4, axis=2)

c = int(0.01 * img.size)
for x, y in zip(np.random.randint(0, img_width - amogi.shape[0], c), np.random.randint(0, img_height - amogi.shape[1], c)):
    amogi_with_dir = np.flip(amogi, axis=1) if np.random.randint(0, 2) else amogi
    if img[x, y][:-1].sum() < 2.9:
        out_img[x:x+amogi.shape[0], y:y+amogi.shape[1], :] = amogi_with_dir * img[x, y] + (amogi_with_dir == 0) * out_img[x:x+amogi.shape[0], y:y+amogi.shape[1], :]


plt.imshow(out_img)
plt.show()