
import numpy as np
# import os
# import cv2
from PIL import Image, ImageFilter

#     Parameters
# ----------
# image : ndarray
#     Input image data. Will be converted to float.
# mode : str
#     One of the following strings, selecting the type of noise to add:

#     'gauss'     Gaussian-distributed additive noise.
#     'poisson'   Poisson-distributed noise generated from the data.
#     's&p'       Replaces random pixels with 0 or 1.
#     'speckle'   Multiplicative noise using out = image + n*image,where
#                 n is uniform noise with specified mean & variance.
noisytypes = ["poisson"]
# noisytypes = ["gauss", "s&p", "poisson", "speckle"]


def Noisy_random(img):
    noisyidx = np.random.randint(0, len(noisytypes))
    noisytype = noisytypes[noisyidx]
    return noisy(noisytype, np.array(img, dtype="float32"))


def get_image_shape(image):
    # print("\nimage info: ", image)

    if hasattr(image, "shape"):
        return image.shape
    else:
        imgarray = np.array(image, dtype="float32")
        return imgarray.shape


def out_to_image(np_array):
    return Image.fromarray(np.asarray(np.clip(np_array, 0, 255), dtype="uint8"))


def noisy(noise_typ, image):
    # print("\nimage info: ", image)
    # imgarray = np.array(image, dtype="float32")
    # print("\nimgarray shape: ", imgarray.shape)

    if noise_typ == "gauss":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return out_to_image(noisy)
    elif noise_typ == "s&p":
        row, col, ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0
        # return Image.fromarray(out)
        return out_to_image(noisy)
    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return out_to_image(noisy)
    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        return out_to_image(noisy)
