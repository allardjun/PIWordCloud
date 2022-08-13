from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw
from os.path import exists
import math
from random import randint, choice
import glob

from piwc_PIWordCloud import PI

image_path_list = glob.glob("results/vignettes/*.png")

print(image_path_list)

image_list = []
for image_path in image_path_list:
    image_tmp = Image.open(image_path)
    image = image_tmp.convert("RGB")
    image_list.append(image)

image.save("combined.pdf",save_all=True,append_images=image_list)

