import argparse

import numpy as np
import matplotlib.pyplot as plt
from skimage import io

AMOGI_DENSITY = 0.01

parser = argparse.ArgumentParser()
parser.add_argument('--input')
args = parser.parse_args()

img = io.imread(args.input) / 255
if img.shape[-1] == 3:
    img = np.concatenate([img, np.ones((img.shape[0], img.shape[1], 1))], axis=2)
out_img = img * np.array([1, 1, 1, 0.9])
img_width, img_height, img_depth = img.shape


AMOGI = np.array([
    [1.0, 1.0, 1.0, 0.0],
    [0.5, 0.5, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 0.0],
    [1.0, 0.0, 1.0, 0.0]
])
AMOGI = np.stack([AMOGI]*4, axis=2)

amogi_count = int(AMOGI_DENSITY * img.size)
randx = np.random.randint(0, img_width - AMOGI.shape[0], amogi_count)
randy = np.random.randint(0, img_height - AMOGI.shape[1], amogi_count)
for x, y in zip(randx, randy):
    if img[x, y][:-1].sum() < 2.9:
        amogi_with_dir = np.flip(AMOGI, axis=1) if np.random.randint(0, 2) else AMOGI
        out_img[x:x+AMOGI.shape[0], y:y+AMOGI.shape[1], :] = amogi_with_dir * img[x, y] + (amogi_with_dir == 0) * out_img[x:x+AMOGI.shape[0], y:y+AMOGI.shape[1], :]

plt.imshow(out_img)
plt.show()