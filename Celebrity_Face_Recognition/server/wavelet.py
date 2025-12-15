# wavelet.py
# This file contains a helper function to apply 2D Wavelet Transform
# on an image and extract high-frequency (edge/texture) information.

import numpy as np
import pywt  # PyWavelets library for wavelet transforms
import cv2  # OpenCV for image processing


def w2d(img, mode="haar", level=1):
    """
    Apply 2D Wavelet Transform on an image and return the
    high-frequency component image.

    Parameters:
    img   : Input image (RGB image)
    mode  : Type of wavelet (default = 'haar')
    level : Decomposition level (default = 1)

    Returns:
    imArray_H : Image reconstructed using only high-frequency components
    """

    # Copy input image
    imArray = img

    # -----------------------------
    # STEP 1: Convert image to grayscale
    # Wavelet transform works on single channel images
    # -----------------------------
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)

    # -----------------------------
    # STEP 2: Convert image to float
    # Normalize pixel values between 0 and 1
    # -----------------------------
    imArray = np.float32(imArray)
    imArray /= 255

    # -----------------------------
    # STEP 3: Perform 2D Wavelet Decomposition
    # wavedec2 returns:
    # [cA, (cH, cV, cD), ...] depending on level
    # cA = Approximation (low-frequency info)
    # cH, cV, cD = Detail coefficients (edges & textures)
    # -----------------------------
    coeffs = pywt.wavedec2(imArray, mode, level=level)

    # -----------------------------
    # STEP 4: Remove low-frequency component
    # This keeps only edge and texture information
    # -----------------------------
    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0  # Zero out approximation coefficients

    # -----------------------------
    # STEP 5: Reconstruct image using only
    # high-frequency wavelet coefficients
    # -----------------------------
    imArray_H = pywt.waverec2(coeffs_H, mode)

    # -----------------------------
    # STEP 6: Convert image back to 8-bit format
    # -----------------------------
    imArray_H *= 255
    imArray_H = np.uint8(imArray_H)

    return imArray_H
