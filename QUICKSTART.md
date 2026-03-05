# 🚀 Quick Start Guide (For Experienced Developers)

If you're familiar with Python/Node.js projects, follow these quick steps:

## Prerequisites
- Python 3.12+
- Node.js 18+
- Git

## Setup (5 minutes)

### 1. Clone & Download Weights
```bash
git clone https://github.com/ShubhamKalwar-62/NutriVision.git
cd NutriVision
```

**⚠️ CRITICAL:** Download model weights (244 MB):
- Link: https://drive.google.com/drive/folders/13kAvdJRTdD1-EBWndrdziyN0sXqczoZU?usp=sharing
- Place: `weights/custom-yolov4-detector_3000(98.61).weights`

### 2. Backend Setup
```bash
python -m venv .venv
.venv\Scripts\activate              # Windows
# source .venv/bin/activate         # Mac/Linux

pip install -r requirements.txt
python api_server.py                # Runs on http://localhost:5000
```

### 3. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm run dev                         # Runs on http://localhost:5173
```

### 4. Access
Open http://localhost:5173 in your browser

## Tech Stack
- **Backend:** Flask 3.0, OpenCV 4.9, YOLOv4, SQLite
- **Frontend:** React 19, Vite 5, Framer Motion
- **AI/ML:** YOLOv4 (98.6% mAP), Custom trained on 7 food classes

## Test
- Signup/Login at http://localhost:5173
- Upload food image with thumb reference
- View nutrition analysis

## Troubleshooting
- **Model not found:** Ensure weights file is in `weights/` folder
- **Port conflicts:** Change ports in `api_server.py` (Flask) or use `npm run dev -- --port 5174`
- **CORS errors:** Ensure Flask-CORS is installed: `pip install flask-cors`

## For Detailed Instructions
See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step beginner-friendly instructions.
