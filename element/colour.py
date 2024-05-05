from PIL import Image, ImageDraw, ImageFont

import requests
import numpy as np
from io import BytesIO


async def colour_f(image_url):
    with Image.open(BytesIO(requests.get(image_url).content)) as f:
        mean_color = np.mean(np.array(f), axis=(0,1))
        if isinstance(mean_color, np.ndarray) and len(mean_color) >= 3:
            return tuple(map(int, mean_color[:3]))
        else:
            return None
