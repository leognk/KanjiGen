import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import os


def plot_img(filepath):
    image = mpimg.imread(filepath)
    height, width = image.shape[:2]
    dpi = plt.rcParams['figure.dpi']
    fig_size = width / float(dpi), height / float(dpi)
    plt.figure(figsize=fig_size)
    plt.imshow(image)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()


indices = range(100)
data_dir = 'data'


filepath = os.path.join(data_dir, 'attributes.json')
with open(filepath, 'r') as f:
    attributes = json.load(f)
kanji_ids = list(attributes.keys())

for i in indices:
    kanji_id = kanji_ids[i]
    attr = attributes[kanji_id]
    img_path = os.path.join(data_dir, 'images', f'{kanji_id}.png')
    plot_img(img_path)
    print(
        f"readings: {attr['readings']}"
        f"\nmeanings: {attr['meanings']}"
    )