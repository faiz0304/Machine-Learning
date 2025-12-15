# util.py
# Utility functions for face detection, preprocessing,
# feature extraction, and classification

import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import w2d
import sklearn.preprocessing
import sys

# ----------------------------------------------------
# Fix for sklearn backward compatibility issue
# (Older models expect sklearn.preprocessing.data)
# ----------------------------------------------------
sys.modules["sklearn.preprocessing.data"] = sklearn.preprocessing


# ----------------------------------------------------
# Global variables to store model and class mappings
# ----------------------------------------------------
__class_name_to_number = {}  # e.g. {"virat": 0, "federer": 1}
__class_number_to_name = {}  # e.g. {0: "virat", 1: "federer"}
__model = None  # Trained ML model


def classify_image(image_base64_data, file_path=None):
    """
    Classify a face image and return predicted celebrity name
    with probabilities.

    Parameters:
    image_base64_data : Base64 encoded image (used for API calls)
    file_path         : Local image path (used for testing)

    Returns:
    result : List of classification results for detected faces
    """

    # Step 1: Detect face(s) with at least two eyes
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)

    result = []

    # Step 2: Process each detected face
    for img in imgs:

        # Resize original face image to 32x32
        scalled_raw_img = cv2.resize(img, (32, 32))

        # Extract wavelet (edge/texture) features
        img_har = w2d(img, "db1", 5)

        # Resize wavelet image to 32x32
        scalled_img_har = cv2.resize(img_har, (32, 32))

        # ----------------------------------------------------
        # Combine raw RGB image + wavelet image
        # Raw image shape    = 32 x 32 x 3
        # Wavelet image shape = 32 x 32
        # ----------------------------------------------------
        combined_img = np.vstack(
            (
                scalled_raw_img.reshape(32 * 32 * 3, 1),
                scalled_img_har.reshape(32 * 32, 1),
            )
        )

        # Total feature length
        len_image_array = 32 * 32 * 3 + 32 * 32

        # Reshape to model input format
        final = combined_img.reshape(1, len_image_array).astype(float)

        # Step 3: Predict class and probability
        result.append(
            {
                "class": class_number_to_name(__model.predict(final)[0]),
                "class_probability": np.around(
                    __model.predict_proba(final) * 100, 2
                ).tolist()[0],
                "class_dictionary": __class_name_to_number,
            }
        )

    return result


def class_number_to_name(class_num):
    """
    Convert numeric class label to celebrity name
    """
    return __class_number_to_name[class_num]


def load_saved_artifacts():
    """
    Load trained model and class dictionary from disk
    """
    print("loading saved artifacts...start")

    global __class_name_to_number
    global __class_number_to_name
    global __model

    # Load class dictionary
    with open(
        "D:/Machine_Learning_Codebasics/Face_Recognition/server/artifacts/class_dictionary.json",
        "r",
    ) as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

    # Load trained model (only once)
    if __model is None:
        with open(
            "D:/Machine_Learning_Codebasics/Face_Recognition/server/artifacts/saved_model.pkl",
            "rb",
        ) as f:
            __model = joblib.load(f)

    print("loading saved artifacts...done")


def get_cv2_image_from_base64_string(b64str):
    """
    Convert Base64 image string to OpenCV image

    Source:
    https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    """

    # Remove metadata header
    encoded_data = b64str.split(",")[1]

    # Decode base64 string
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)

    # Convert to OpenCV image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img


def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    """
    Detect faces and return cropped face images
    only if at least two eyes are detected
    """

    # Load Haar Cascade classifiers
    face_cascade = cv2.CascadeClassifier(
        "D:/Machine_Learning_Codebasics/Face_Recognition/server/opencv/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        "D:/Machine_Learning_Codebasics/Face_Recognition/server/opencv/haarcascades/haarcascade_eye.xml"
    )

    # Read image from file or base64
    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []

    # Loop through detected faces
    for x, y, w, h in faces:

        # Region of Interest (ROI)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = img[y : y + h, x : x + w]

        # Detect eyes inside face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Accept face only if two or more eyes are detected
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)

    return cropped_faces


def get_b64_test_image_for_virat():
    """
    Load base64 test image for debugging/testing
    """
    with open("D:/Machine_Learning_Codebasics/Face_Recognition/server/b64.txt") as f:
        return f.read()


# ----------------------------------------------------
# Local testing
# ----------------------------------------------------
if __name__ == "__main__":

    load_saved_artifacts()

    print(classify_image(get_b64_test_image_for_virat(), None))

    print(
        classify_image(
            None,
            "D:/Machine_Learning_Codebasics/Face_Recognition/server/test_images/federer1.jpg",
        )
    )
