from PIL import Image
from resizeimage import resizeimage
import numpy as np
from .model import predict_one


def detect(src):
    with open(src, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [128, 128])
            pix = np.array(cover.convert("RGB"))
            pred, _ = predict_one(pix)
            return pred == 0
