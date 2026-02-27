# NutriVision — Food Calorie Estimation Using Deep Learning & Computer Vision

> Detect food items from a photo, estimate portion size using a thumb reference, and get instant calorie breakdowns — powered by YOLOv4 + a React/Vite frontend.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Download Model Weights](#download-model-weights)
- [Training](#training)
- [Dataset](#dataset)
- [Attribution & Academic Use](#attribution--academic-use)
- [License](#license)

---

## Overview
NutriVision uses a custom-trained **YOLOv4** model to detect food items (apple, banana, carrot, onion, orange, tomato, kiwi) and a **thumb** in the same photo.
The thumb acts as a scale reference — from its known size (~5 cm) the system calculates each food item's physical dimensions, estimated volume, weight, and calorie count.

A **Flask REST API** serves predictions and handles user auth + scan history.
A **React + Vite** frontend provides the full web UI.

---

## Features
- Real-time food detection with YOLOv4 (98.6% mAP on validation set)
- Thumb-based physical scale calibration
- Per-item: volume (cm³), weight (g), calories (kcal)
- User authentication (signup / login / JWT)
- Persistent scan history per user
- Colour-based Apple vs Orange disambiguation

---

## Tech Stack

| Layer | Technology |
|---|---|
| Object detection | YOLOv4 (Darknet, via OpenCV DNN) |
| Backend API | Python · Flask · SQLite |
| Frontend | React 19 · Vite · Framer Motion |
| Auth | JWT (custom, stateless) |

---

## Project Structure

```
├── api_server.py                          # Flask API — detection, auth, history
├── custom-yolov4-detector.cfg             # YOLOv4 model config
├── darknet_yolov4_obj_names.names         # Class labels
├── weights/                               # Place downloaded .weights file here
├── uploads/                               # Temporary upload storage (git-ignored)
├── results/                               # Output annotated images (git-ignored)
├── test_images/                           # Drop test images here
├── frontend/                              # React + Vite web app
│   ├── src/
│   └── public/
└── Extra_components/                      # Training notebooks (YOLOv4 & YOLOv5)
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1 — Clone the repo
```bash
git clone https://github.com/ShubhamKalwar-62/NutriVision.git
cd NutriVision
```

### 2 — Download model weights
See [Download Model Weights](#download-model-weights) below and place the file inside `weights/`.

### 3 — Backend
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux

# Install dependencies
pip install flask flask-cors opencv-python numpy

# (Optional) copy and edit the env file
cp .env.example .env

# Start the API server
python api_server.py
```
API runs at `http://localhost:5000`

### 4 — Frontend
```bash
cd frontend
npm install
npm run dev
```
UI runs at `http://localhost:5173`

Open your browser at **http://localhost:5173**

---

## Download Model Weights

The weights files are ~244 MB each and exceed GitHub's 100 MB file size limit.
They are hosted on Google Drive.

**Download:** [YOLOv4 Weights — Google Drive](https://drive.google.com/drive/folders/13kAvdJRTdD1-EBWndrdziyN0sXqczoZU?usp=sharing)

Place the downloaded file at:
```
weights/custom-yolov4-detector_3000(98.61).weights
```

---

## Training

Training notebooks are in `Extra_components/`:

| Model | Notebook |
|---|---|
| YOLOv4 (Darknet) | `Extra_components/Training_Custom_YOLOV4/Train_Custom_YOLOv4_Darknet_Roboflow.ipynb` |
| YOLOv5 | `Extra_components/Training_Custom_YOLOV5/CJ_Roboflow_Train_Custom_YOLOv5.ipynb` |

---

## Dataset

- **Roboflow:** [Fruits & Thumb Detection Dataset](https://app.roboflow.com/chetan-projects-object-detcions/fruits--and-thumb-detection)
- **Classes:** `Apple`, `Banana`, `Carrot`, `Onion`, `Orange`, `Qiwi`, `Tomato`, `thumb`

---

## Attribution & Academic Use

This project is originally developed by **Chetan Jarande, Mukta Bhagwat, Vishakha Patil, and Diya Ukirde** and is available as an open-source project on [GitHub](https://github.com/chetan-jarande/Food-calorie-estimations-Using-Deep-Learning-And-Computer-Vision).

This repository is a **refined and extended fork** of that original work. The following additional contributions have been made:

- Built a complete **full-stack web application** (Flask REST API + React/Vite frontend) with user authentication, JWT sessions, and scan history — none of which existed in the original project.
- Rewrote the **volume & calorie estimation pipeline** to use YOLO bounding-box dimensions as the physical scale reference, fixing a critical bug that produced astronomically wrong calorie values (e.g. 1.4 million kcal for a banana).
- Added **colour-based Apple / Orange post-classification** to correct frequent model misidentification between the two fruits.
- Added the **logo asset**.
- General code cleanup, error handling, and GitHub preparation.

If you are using this project for **academic purposes** — such as a final year project — it is **mandatory** that you:

1. Acknowledge the original authors: **Chetan Jarande, Mukta Bhagwat, Vishakha Patil, and Diya Ukirde**.
2. Credit this fork for the additional full-stack and bug-fix contributions described above.
3. State clearly that your work is **based on an existing open-source project** and describe what modifications you have made.
4. **Not claim the project as entirely your own original work.**

Failure to adhere to these conditions violates both the project's license and academic integrity standards.

---

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).