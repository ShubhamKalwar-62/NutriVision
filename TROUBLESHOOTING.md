# 🔧 Troubleshooting Guide

Common issues and their solutions when running NutriVision.

---

## Backend Issues

### ❌ Error: "Python is not recognized as an internal or external command"

**Cause:** Python is not in your system PATH

**Solutions:**
1. **Quick fix:** Use full path to Python:
   ```bash
   C:\Python310\python.exe -m venv .venv
   ```

2. **Permanent fix:** 
   - Reinstall Python from https://python.org/downloads/
   - During installation, CHECK the box "Add Python to PATH"
   - Restart your terminal/command prompt

### ❌ Error: "No module named 'cv2'" or "No module named 'flask'"

**Cause:** Dependencies not installed or wrong Python environment

**Solution:**
```bash
# Make sure you see (.venv) in your prompt
.venv\Scripts\activate

# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# If still fails, install individually:
pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install opencv-python==4.9.0.80
pip install numpy==1.26.3
```

### ❌ Error: "FileNotFoundError: Model file not found"

**Cause:** YOLOv4 weights file missing or in wrong location

**Solution:**
1. Download weights from: https://drive.google.com/drive/folders/13kAvdJRTdD1-EBWndrdziyN0sXqczoZU?usp=sharing
2. Ensure filename is EXACTLY: `custom-yolov4-detector_3000(98.61).weights`
3. Place in `weights/` folder
4. Verify path structure:
   ```
   NutriVision/
   └── weights/
       └── custom-yolov4-detector_3000(98.61).weights
   ```

### ❌ Error: "Address already in use" or "Port 5000 is in use"

**Cause:** Another application is using port 5000

**Solution 1 (Change port):**
Edit `api_server.py` (last line):
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```
Then update frontend API calls to use port 5001.

**Solution 2 (Kill process using port):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### ❌ Error: "cannot activate virtual environment" (PowerShell)

**Cause:** PowerShell execution policy restriction

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.venv\Scripts\Activate.ps1
```

### ❌ Model loads but detection takes forever (>30 seconds)

**Cause:** Running on CPU without optimization

**Solutions:**
- This is normal for CPU inference
- First inference is always slower (model initialization)
- Subsequent detections should be ~3-5 seconds
- For faster inference, use a machine with dedicated GPU

---

## Frontend Issues

### ❌ Error: "npm: command not found" or "'npm' is not recognized"

**Cause:** Node.js not installed or not in PATH

**Solution:**
1. Download Node.js LTS from https://nodejs.org/
2. Install with default options
3. Restart your terminal
4. Verify: `node --version` and `npm --version`

### ❌ Error: "Port 5173 already in use"

**Cause:** Another Vite/dev server is running

**Solution 1 (Use different port):**
```bash
npm run dev -- --port 5174
```
Then access at http://localhost:5174

**Solution 2 (Kill existing process):**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5173 | xargs kill -9
```

### ❌ Error: "Cannot find module" after npm install

**Cause:** Corrupted node_modules or package-lock.json

**Solution:**
```bash
cd frontend

# Remove existing installations
rm -rf node_modules
rm package-lock.json

# Reinstall
npm install
```

Windows users can delete folders manually:
1. Delete `node_modules` folder
2. Delete `package-lock.json` file
3. Run `npm install` again

### ❌ Frontend shows blank white page

**Possible causes & solutions:**

1. **Backend not running:**
   - Ensure Flask server is running on port 5000
   - Check Terminal 1 for backend status

2. **Check browser console (F12):**
   - Look for error messages
   - Common errors:
     - "Network Error" → Backend not running
     - "CORS policy" → Flask-CORS not installed
     - "404 Not Found" → Check API endpoint URLs

3. **Clear browser cache:**
   - Press Ctrl+Shift+R (hard reload)
   - Or clear cache in browser settings

4. **Check frontend logs:**
   - Look at terminal where you ran `npm run dev`
   - Check for compilation errors

### ❌ Login/Signup not working - no error shown

**Possible causes:**

1. **Backend not running:** Start Flask server in Terminal 1

2. **Wrong API URL:** 
   - Check `frontend/src` for API base URL
   - Should be `http://localhost:5000`

3. **CORS issue:**
   ```bash
   # In backend virtual environment
   pip install flask-cors
   
   # Restart backend server
   ```

---

## Image Upload & Detection Issues

### ❌ "No food items detected" even with valid food image

**Possible causes:**

1. **Food not in trained categories:**
   - Only detects: apple, banana, carrot, onion, orange, tomato, kiwi
   - Try with one of these foods

2. **Poor image quality:**
   - Use well-lit images
   - Avoid blurry photos
   - Ensure food is clearly visible

3. **No thumb reference:**
   - System needs thumb in image for scale
   - Include your thumb next to food

4. **Model not loaded:**
   - Check backend terminal for model loading success message
   - Verify weights file is present and correct

### ❌ Upload shows error: "File too large"

**Cause:** Image exceeds 10MB limit

**Solution:**
- Compress image before uploading
- Use lower resolution photo
- Or edit `api_server.py` to increase limit (not recommended)

### ❌ Calories seem incorrect

**Possible causes:**

1. **No thumb reference:** Estimation uses default scale
2. **Thumb too far/close:** Affects scale calculation
3. **Irregular food shape:** Volume approximation may be off
4. **Multiple overlapping items:** May confuse detection

**Tips for better accuracy:**
- Include thumb clearly in frame
- Place thumb close to food items
- Avoid overlapping foods
- Use well-lit, clear photos
- Take photo from top-down angle

---

## Database Issues

### ❌ Error: "database is locked"

**Cause:** Multiple instances accessing SQLite database

**Solution:**
1. Stop all running instances of the backend
2. Delete `nutrivision.db` file (will recreate automatically)
3. Start backend again

### ❌ User signup/login data lost after restart

**Cause:** Database file location issue

**Solution:**
- Check if `nutrivision.db` file exists in project root
- Don't delete this file if you want to keep user data
- Backup this file for data persistence

---

## Performance Issues

### ❌ Backend uses too much RAM (>2GB)

**Normal behavior:**
- YOLOv4 model is memory-intensive
- ~1-2GB RAM usage is normal
- First inference uses more memory

**If excessive:**
- Close other applications
- Restart backend server periodically

### ❌ Frontend build/dev server is slow

**Solutions:**
```bash
cd frontend

# Clear cache
rm -rf node_modules/.vite

# Restart dev server
npm run dev
```

---

## Connection Issues

### ❌ "Network Error" or "Failed to fetch" in browser

**Checklist:**
1. ✅ Backend running? Check Terminal 1
2. ✅ Backend shows "Running on http://localhost:5000"?
3. ✅ No error messages in backend terminal?
4. ✅ Can you access http://localhost:5000 in browser?
5. ✅ Firewall blocking connections?

**Test backend directly:**
```bash
# In browser or using curl
curl http://localhost:5000/api/health
```

### ❌ CORS errors in browser console

**Error:** "Access to XMLHttpRequest at ... has been blocked by CORS policy"

**Solution:**
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install Flask-CORS
pip install flask-cors

# Verify it's in api_server.py
# Should have: from flask_cors import CORS
#              CORS(app)

# Restart backend server
python api_server.py
```

---

## Operating System Specific Issues

### Windows

**PowerShell Script Execution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Long path issues:**
- Enable long paths in Windows 10/11
- Or move project closer to C:\ drive (e.g., `C:\NutriVision`)

**Antivirus blocking:**
- Some antivirus software may block Flask server
- Add project folder to exceptions if needed

### macOS

**Python command:**
- Use `python3` instead of `python`
- Use `pip3` instead of `pip`

**Permission issues:**
```bash
# Don't use sudo for pip install
# Create virtual environment first
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Linux

**Python/pip not found:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora/RHEL
sudo dnf install python3 python3-pip
```

**Permission errors:**
```bash
# Don't use sudo with pip when in virtual environment
# Always activate .venv first
source .venv/bin/activate
```

---

## Still Having Issues?

### Before Asking for Help:

1. **Read error messages carefully** - They often tell you exactly what's wrong
2. **Check all terminals** - Look for errors in both backend and frontend terminals
3. **Verify file locations** - Especially the model weights file
4. **Restart everything** - Close all terminals, restart both servers
5. **Check versions:**
   ```bash
   python --version    # Should be 3.12+
   node --version      # Should be 18+
   npm --version       # Should be 9+
   ```

### Debugging Steps:

1. **Backend test:**
   ```bash
   # Activate venv
   .venv\Scripts\activate
   
   # Test Python import
   python -c "import cv2, flask, numpy; print('All imports OK')"
   
   # Check if weights file exists
   dir weights  # Windows
   ls weights/  # Mac/Linux
   ```

2. **Frontend test:**
   ```bash
   cd frontend
   
   # Check if node_modules exists
   dir node_modules  # Windows
   ls node_modules/  # Mac/Linux
   
   # Reinstall if needed
   npm install
   ```

3. **Network test:**
   - Open http://localhost:5000 (backend)
   - Open http://localhost:5173 (frontend)
   - Check browser console (F12) for errors

### Get Help:

1. **GitHub Issues:** https://github.com/ShubhamKalwar-62/NutriVision/issues
2. **Include in your report:**
   - Operating System (Windows 10/11, macOS, Linux)
   - Python version (`python --version`)
   - Node.js version (`node --version`)
   - Exact error message
   - Steps you tried
   - Screenshots if relevant

---

## Quick Reset (Last Resort)

If nothing works, start fresh:

```bash
# 1. Delete virtual environment
rm -rf .venv

# 2. Delete node_modules
cd frontend
rm -rf node_modules package-lock.json
cd ..

# 3. Start setup from scratch
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

cd frontend
npm install
cd ..

# 4. Verify weights file is present
# Download again if needed

# 5. Start servers
# Terminal 1: python api_server.py
# Terminal 2: cd frontend && npm run dev
```

---

**Remember:** Most issues are simple fixes. Read error messages carefully, and check the basics first (file locations, installations, servers running)!
