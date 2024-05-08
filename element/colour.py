from PIL import Image, ImageDraw, ImageFont

import requests
import numpy as np
from io import BytesIO


async def colour_f(image_url):
    with Image.open(BytesIO(requests.get(image_url).content)) as f:
        f = f.convert('RGBA')
        mean_color = np.mean(np.array(f)[..., :3], axis=(0,1))
        return tuple(map(int, mean_color))
