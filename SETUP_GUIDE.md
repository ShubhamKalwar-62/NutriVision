# 🚀 NutriVision - Complete Setup Guide for Beginners

This guide will help you set up and run the NutriVision project on your computer, even if you're new to Python or Node.js projects.

---

## 📋 Table of Contents
1. [Prerequisites & Installation](#prerequisites--installation)
2. [Project Setup](#project-setup)
3. [Running the Application](#running-the-application)
4. [Common Issues & Solutions](#common-issues--solutions)
5. [Testing the Application](#testing-the-application)

---

## 🛠️ Prerequisites & Installation

### Step 1: Install Required Software

#### A. Python 3.12 or higher
1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.12 or newer (Python 3.12+ recommended for best compatibility)

2. **Install Python:**
   - **IMPORTANT:** During installation, CHECK the box "Add Python to PATH"
   - Click "Install Now"

3. **Verify Installation:**
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Type: `python --version`
   - You should see: `Python 3.12.x` or higher

#### B. Node.js 18 or higher
1. **Download Node.js:**
   - Visit: https://nodejs.org/
   - Download the LTS (Long Term Support) version

2. **Install Node.js:**
   - Run the installer
   - Follow the installation wizard (use default settings)

3. **Verify Installation:**
   - Open Command Prompt or Terminal
   - Type: `node --version`
   - You should see: `v18.x.x` or higher
   - Type: `npm --version`
   - You should see npm version (e.g., `9.x.x` or higher)

#### C. Git (Optional but recommended)
1. **Download Git:**
   - Visit: https://git-scm.com/downloads
   - Download for your operating system

2. **Install Git:**
   - Run the installer with default settings

---

## 📦 Project Setup

### Step 1: Get the Project Files

**Option A - From GitHub (Recommended):**
```bash
git clone https://github.com/ShubhamKalwar-62/NutriVision.git
cd NutriVision
```

**Option B - From ZIP file:**
1. Extract the ZIP file you received
2. Open Command Prompt/Terminal
3. Navigate to the extracted folder:
   ```bash
   cd path/to/Food-calorie-estimations-Using-Deep-Learning-And-Computer-Vision-main
   ```
   Replace `path/to/` with the actual location of your extracted folder

### Step 2: Download Model Weights (CRITICAL!)

⚠️ **The project CANNOT run without this file!**

1. **Download the model file:**
   - Go to: https://drive.google.com/drive/folders/13kAvdJRTdD1-EBWndrdziyN0sXqczoZU?usp=sharing
   - Download: `custom-yolov4-detector_3000(98.61).weights` (244 MB)

2. **Place the file correctly:**
   - Create a `weights` folder in the project directory if it doesn't exist
   - Move the downloaded `.weights` file into this folder
   - Final path should be: `weights/custom-yolov4-detector_3000(98.61).weights`

3. **Verify:**
   ```bash
   # Windows
   dir weights
   
   # Mac/Linux
   ls weights/
   ```
   You should see the `.weights` file listed

### Step 3: Set Up Backend (Python/Flask)

1. **Navigate to project root** (if not already there)

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   
   # Mac/Linux
   python3 -m venv .venv
   ```
   This creates an isolated Python environment for the project.

3. **Activate the virtual environment:**
   ```bash
   # Windows (Command Prompt)
   .venv\Scripts\activate
   
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   
   # Mac/Linux
   source .venv/bin/activate
   ```
   
   ✅ **Success indicator:** You should see `(.venv)` at the start of your command prompt

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This will install Flask, OpenCV, NumPy, and other required libraries.
   
   ⏱️ **Wait time:** 2-5 minutes depending on your internet speed

### Step 4: Set Up Frontend (React/Vite)

1. **Open a NEW terminal/command prompt** (keep the backend terminal open)

2. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   
   ⏱️ **Wait time:** 2-5 minutes. You'll see many packages being downloaded.

---

## ▶️ Running the Application

You need to run BOTH backend and frontend simultaneously in separate terminals.

### Terminal 1: Start Backend Server

1. **Open first terminal** in project root directory

2. **Activate virtual environment** (if not already activated):
   ```bash
   # Windows (Command Prompt)
   .venv\Scripts\activate
   
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Start the Flask server:**
   ```bash
   python api_server.py
   ```

4. **✅ Success indicators:**
   - You should see:
     ```
     * Running on http://127.0.0.1:5000
     * Running on http://localhost:5000
     ```
   - No error messages
   - The YOLOv4 model loading message

5. **⚠️ Keep this terminal open!** Don't close it while using the app.

### Terminal 2: Start Frontend Server

1. **Open a SECOND terminal/command prompt**

2. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```
   (If you're in the project root, otherwise adjust path accordingly)

3. **Start the Vite development server:**
   ```bash
   npm run dev
   ```

4. **✅ Success indicators:**
   - You should see:
     ```
     VITE v5.x.x  ready in xxx ms
     
     ➜  Local:   http://localhost:5173/
     ➜  Network: use --host to expose
     ```

5. **⚠️ Keep this terminal open too!**

### Access the Application

1. **Open your web browser** (Chrome, Firefox, Edge, or Safari)

2. **Go to:** http://localhost:5173

3. **You should see:** The NutriVision home page with navigation and features

---

## 🎯 Testing the Application

### First-Time Usage:

1. **Sign Up:**
   - Click "Login" or "Get Started"
   - Click "Sign Up" if you don't have an account
   - Enter any email (e.g., test@example.com)
   - Create a password
   - Click "Sign Up"

2. **Upload a Food Image:**
   - Go to "Analyze" page
   - **IMPORTANT:** Your image must include:
     - One or more food items (apple, banana, carrot, onion, orange, tomato, or kiwi)
     - Your THUMB in the image (for scale reference)
   - Drag & drop the image or click to browse
   - Click "Analyze Food"

3. **View Results:**
   - Wait 3-5 seconds for processing
   - See the annotated image with bounding boxes
   - View nutrition breakdown table with calories

4. **Check History:**
   - Click "History" in navigation
   - See all your previous scans

### Test Images:

Sample test images are provided in the `test_images/` folder. Use these to test the application!

---

## ❗ Common Issues & Solutions

### Issue 1: "Python is not recognized"
**Problem:** Python not in system PATH

**Solution:**
- Reinstall Python and CHECK "Add Python to PATH"
- OR manually add Python to PATH in system environment variables

### Issue 2: "python: command not found" (Mac/Linux)
**Solution:** Try using `python3` instead of `python`:
```bash
python3 --version
python3 -m venv .venv
```

### Issue 3: "Cannot activate virtual environment (PowerShell)"
**Problem:** PowerShell execution policy restriction

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

### Issue 4: "Port 5000 already in use"
**Problem:** Another application is using port 5000

**Solution:**
- Find and close the other application
- OR change the port in `api_server.py` (last line):
  ```python
  app.run(host='0.0.0.0', port=5001, debug=True)
  ```
  Then access at http://localhost:5001

### Issue 5: "Port 5173 already in use"
**Solution:** Kill the process or use a different port:
```bash
npm run dev -- --port 5174
```
Then access at http://localhost:5174

### Issue 6: "Model weights not found"
**Error:** `FileNotFoundError: Model file not found`

**Solution:**
- Ensure you downloaded the `.weights` file (244 MB)
- Place it in the `weights/` folder
- Check the filename matches exactly: `custom-yolov4-detector_3000(98.61).weights`

### Issue 7: "No module named 'cv2'" or similar import errors
**Solution:**
```bash
# Make sure virtual environment is activated (you see .venv in prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue 8: "npm not found"
**Solution:**
- Reinstall Node.js from https://nodejs.org/
- Restart your terminal after installation

### Issue 9: Frontend shows blank page
**Solutions:**
1. Check browser console (F12) for errors
2. Ensure backend is running on port 5000
3. Clear browser cache and reload (Ctrl+F5)

### Issue 10: CORS errors in browser console
**Solution:**
- Make sure Flask-CORS is installed: `pip install flask-cors`
- Restart the backend server

### Issue 11: "Address already in use" (Mac/Linux)
**Solution:**
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process (replace PID with the number from above)
kill -9 PID
```

---

## 📱 What Should You See?

### When Backend Starts Successfully:
```
Loading YOLOv4 model...
Model loaded successfully!
 * Serving Flask app 'api_server'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### When Frontend Starts Successfully:
```
VITE v5.1.0  ready in 523 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### In Your Browser:
- Home page with NutriVision branding
- Navigation: Home, Analyze, History, Login
- Clean, modern UI with animations

---

## 🔧 Project Structure Quick Reference

```
NutriVision/
├── api_server.py               # Backend API (must be running)
├── requirements.txt            # Python dependencies
├── weights/                    # Model weights (download required!)
│   └── custom-yolov4-detector_3000(98.61).weights
├── uploads/                    # Temporary image storage (auto-created)
├── results/                    # Processed images (auto-created)
├── test_images/                # Sample images for testing
├── frontend/                   # React application
│   ├── package.json           # Node dependencies
│   ├── src/                   # React source code
│   └── public/                # Static assets
└── .venv/                     # Python virtual environment (created by you)
```

---

## 🎓 Quick Command Reference

### Backend Commands:
```bash
# Activate virtual environment
.venv\Scripts\activate              # Windows CMD
.venv\Scripts\Activate.ps1          # Windows PowerShell
source .venv/bin/activate           # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run server
python api_server.py

# Stop server: Ctrl+C
```

### Frontend Commands:
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production (optional)
npm run build

# Stop server: Ctrl+C
```

---

## 📞 Need More Help?

1. **Check the main README.md** for additional technical details
2. **Read error messages carefully** - they often tell you what's wrong
3. **Google the error message** - most common issues have solutions online
4. **Check GitHub Issues** on the repository

---

## ✅ Success Checklist

Before running the app, make sure:
- [ ] Python 3.12+ installed and in PATH
- [ ] Node.js 18+ installed
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Model weights file downloaded and placed in `weights/` folder
- [ ] Frontend dependencies installed (`npm install` in frontend folder)
- [ ] Backend server running (Terminal 1)
- [ ] Frontend server running (Terminal 2)
- [ ] Browser open at http://localhost:5173

---

## 🎉 You're All Set!

Once both servers are running and you can access the application in your browser, you're ready to start analyzing food images and tracking nutrition!

**Enjoy using NutriVision! 🍎🍌🥕**
