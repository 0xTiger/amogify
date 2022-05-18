import os
import argparse

import numpy as np
from skimage import io


parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='path to the input image to be converted')
parser.add_argument('--output', help='path to the output image to be saved')
parser.add_argument('--density', type=float, default=0.01, help='number of amogi to add per pixel')
parser.add_argument('--show', action='store_true', 
    help='this flag specified whether to plot a comparison of the image & it\'s conversion')
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

amogi_count = int(args.density * img.size)
randx = np.random.randint(0, img_width - AMOGI.shape[0], amogi_count)
randy = np.random.randint(0, img_height - AMOGI.shape[1], amogi_count)
for x, y in zip(randx, randy):
    if img[x, y][:-1].sum() < 2.9:
        flip = np.random.randint(0, 2)
        amogi_with_dir = np.flip(AMOGI, axis=1) if flip else AMOGI
        out_img[x:x+AMOGI.shape[0], y:y+AMOGI.shape[1], :] = amogi_with_dir * img[x, y] + (amogi_with_dir == 0) * out_img[x:x+AMOGI.shape[0], y:y+AMOGI.shape[1], :]
        eye_start, eye_end = (y+2, y+4) if flip else (y, y+2)
        grey= img[x, y][:-1].mean() * 1.1

        out_img[x+1, eye_start:eye_end, :] = np.vstack([[grey, grey, grey, 1.0]]*2)

input_filename, input_ext = os.path.splitext(args.input)
out_filepath = f'{input_filename}_amogified.png' if args.output is None else args.output
io.imsave(out_filepath, out_img)

if args.show:
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
    axs[0].imshow(img)
    axs[0].set_xticks([])
    axs[0].set_yticks([])
    axs[1].imshow(out_img)
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    plt.show()