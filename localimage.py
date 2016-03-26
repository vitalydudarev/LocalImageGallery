import fnmatch
import os
import config
from PIL import Image

def thumb(file_name, output_file_name, thumb_size):
    img = Image.open(file_name)
    width, height = img.size

    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(thumb_size, Image.ANTIALIAS)
    img.save(output_file_name)