from PIL import Image
from resizeimage import resizeimage
import numpy as np
from .model import predict_one


def detect(src):
    '''
    Detect an image

    **Parameters**

        src: *str*
            The file path of the image

    **Returns**

        detection: *bool*
            Return True if detecting violation

    '''
    with open(src, 'r+b') as f:
        with Image.open(f) as image:
            # Central scaling crop the image to 128x128
            cover = resizeimage.resize_cover(image, [128, 128])
            # Covert PIL image to RGB numpy array (3 color channels)
            pix = np.array(cover.convert("RGB"))
            pred, _ = predict_one(pix)
            # Prediction 0 means detection
            return pred == 0
