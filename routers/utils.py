import cv2
import base64
import numpy as np
from urllib.request import urlopen, Request


async def decode_image(image):
    image_data = await image.read()
    name = image.filename

    if name == "base64":
        image_data = base64.b64decode(image_data)

    file_bytes = np.fromstring(image_data, np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    return image


async def decode_image_url(image_url: str):
    request = Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
    respone = urlopen(request, timeout=5)

    image_data = respone.read()
    image = np.asarray(bytearray(image_data), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image
