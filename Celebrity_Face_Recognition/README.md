# 🎯 Sports Celebrity Face Recognition System

A complete **Machine Learning + Computer Vision** project that detects a face from an image and classifies it as a known sports celebrity using **OpenCV, Wavelet Transform, and Scikit-learn**, exposed via a **Flask API**.

---

## 📌 Project Overview

This system:
- Detects faces using **Haar Cascade Classifier**
- Ensures face validity by detecting **at least two eyes**
- Extracts **raw RGB features** and **wavelet (edge/texture) features**
- Combines features into a single vector
- Classifies the face using a **trained ML model**
- Exposes prediction via a **Flask REST API**

---

## 🧠 Technologies Used

- Python
- OpenCV
- NumPy
- PyWavelets
- Scikit-learn
- Flask
- Joblib

---

## 🗂️ Project Structure

```
Face_Recognition/
│
├── server/
│   ├── server.py              # Flask API
│   ├── util.py                # Core logic (detection + classification)
│   ├── wavelet.py             # Wavelet feature extraction
│   │
│   ├── artifacts/
│   │   ├── saved_model.pkl    # Trained ML model
│   │   └── class_dictionary.json
│   │
│   ├── opencv/
│   │   └── haarcascades/
│   │       ├── haarcascade_frontalface_default.xml
│   │       └── haarcascade_eye.xml
│   │
│   ├── test_images/
│   └── b64.txt
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd Face_Recognition
```

### 2️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Flask Server

```bash
python server/server.py
```

Server will start at:
```
http://127.0.0.1:5000
```

---

## 🔌 API Usage

### Endpoint
```
POST /classify_image
```

### Request
- `form-data`
  - `image_data` → Base64 encoded image

### Response (JSON)
```json
[
  {
    "class": "virat",
    "class_probability": [85.21, 10.34, 4.45],
    "class_dictionary": {
      "virat": 0,
      "federer": 1,
      "serena": 2
    }
  }
]
```

---

## 🧪 Local Testing

You can test directly using image files:

```python
classify_image(
    None,
    "server/test_images/federer1.jpg"
)
```

---

## 🧠 Feature Engineering Details

- **Raw Image Features**
  - RGB image resized to `32 x 32`
- **Wavelet Features**
  - Haar/DB1 wavelet
  - Captures edges and texture
- **Final Feature Vector Size**
  ```
  32*32*3 + 32*32 = 4096 features
  ```

---

## 📈 Model

- Classical ML model trained using **Scikit-learn**
- Saved using `joblib`
- Probabilistic predictions using `predict_proba()`

---

## 🔐 Notes & Limitations

- Haar cascades are sensitive to lighting and pose
- Performance depends on image quality
- Designed for **educational & portfolio purposes**

---

## 🌱 Future Improvements

- Replace Haar Cascade with **MTCNN / MediaPipe**
- Add face alignment
- Use **CNN / Deep Learning**
- Add authentication & logging
- Deploy using **Docker + AWS / Render**

---

## 👤 Author

**Faiz Ur Rehman Ashrafi**  
Electronics Engineering | Machine Learning Enthusiast  

---

## ⭐ If you like this project
Give it a ⭐ on GitHub and feel free to contribute!
