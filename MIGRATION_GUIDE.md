# 🔄 Migration Guide — Upgrading to Latest Versions

This guide helps you upgrade the NutriVision project from older versions of Python and dependencies to the latest compatible versions.

---

## 📋 What's Changed

### Python Version
- **Old:** Python 3.10+
- **New:** Python 3.12+
- **Why:** Better performance, improved error messages, and latest features

### Updated Dependencies

| Package | Old Version | New Version | Changes |
|---------|-------------|-------------|---------|
| Flask | 3.0.0 | 3.1.0 | Enhanced security, bug fixes |
| flask-cors | 4.0.0 | 5.0.0 | Improved CORS handling |
| Werkzeug | 3.0.1 | 3.1.0 | Security updates |
| opencv-python | 4.9.0.80 | 4.10.0.84 | Performance improvements |
| numpy | 1.26.3 | 2.1.0 | **Major update** - NumPy 2.x with better performance |
| pytest | 7.4.3 | 8.3.0 | Enhanced testing features |
| pillow | *(new)* | 11.0.0 | Added for better image handling |

---

## 🚀 Quick Migration (5-10 minutes)

### For Existing Installations

If you already have the project set up, follow these steps:

#### 1. Update Python (if needed)

**Check your current Python version:**
```bash
python --version
```

**If you have Python 3.10 or 3.11:**
- The project will work, but Python 3.12+ is recommended
- Download Python 3.12 from [python.org/downloads](https://www.python.org/downloads/)
- Install it and ensure it's added to PATH

#### 2. Clean Up Old Virtual Environment

**Deactivate current environment (if active):**
```bash
deactivate  # On Windows/Mac/Linux
```

**Remove old virtual environment:**
```bash
# Windows
rmdir /s venv

# Mac/Linux
rm -rf venv
```

#### 3. Create Fresh Virtual Environment

**Create new environment with Python 3.12:**
```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

**Activate the new environment:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

#### 4. Install Updated Dependencies

**Install all dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Update Frontend Dependencies (optional)

The frontend already uses latest versions, but you can update:
```bash
cd frontend
npm update
cd ..
```

#### 6. Test the Installation

**Validate setup:**
```bash
python validate_setup.py
```

**Run quick test:**
```bash
python test_detection.py
```

---

## 🔧 Troubleshooting Migration Issues

### Issue: NumPy 2.x Compatibility Errors

**Problem:** Code fails with errors like `AttributeError: module 'numpy' has no attribute 'int0'`

**Solution:** The code has already been updated for NumPy 2.x compatibility. Make sure you:
1. Pulled the latest code from the repository
2. Installed the correct version: `pip install numpy==2.1.0`

**What changed in NumPy 2.x:**
- `np.int0` → `np.intp` (already fixed in code)
- `np.int` → `int` or `np.int64`
- `np.float` → `float` or `np.float64`

### Issue: Flask Import Errors

**Problem:** `ImportError: cannot import name 'xxx' from 'flask'`

**Solution:**
```bash
pip uninstall flask flask-cors werkzeug
pip install flask==3.1.0 flask-cors==5.0.0 werkzeug==3.1.0
```

### Issue: OpenCV DNN Module Not Available

**Problem:** `AttributeError: module 'cv2' has no attribute 'dnn'`

**Solution:**
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python==4.10.0.84
```

### Issue: Virtual Environment Conflicts

**Problem:** Mixed package versions or import errors

**Solution:** Fresh reinstall:
```bash
# Deactivate and remove old environment
deactivate
rm -rf venv  # or rmdir /s venv on Windows

# Create fresh environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install clean dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📝 Breaking Changes & Code Updates

### 1. NumPy Type Aliases (Already Fixed)

**Old code (deprecated):**
```python
box = np.int0(box)
```

**New code (compatible with NumPy 2.x):**
```python
box = np.intp(box)
```

**Status:** ✅ Already updated in all project files

### 2. Flask Import Patterns

All Flask imports remain the same. No code changes needed.

### 3. OpenCV DNN API

The OpenCV DNN API is backward compatible. No changes needed.

---

## ✅ Verification Checklist

After migration, verify everything works:

- [ ] Python version is 3.12+ (`python --version`)
- [ ] Virtual environment is activated (prompt shows `(venv)`)
- [ ] All packages installed without errors (`pip list`)
- [ ] NumPy version is 2.1.0 (`pip show numpy`)
- [ ] Flask version is 3.1.0 (`pip show flask`)
- [ ] OpenCV version is 4.10.0.84 (`pip show opencv-python`)
- [ ] Validation script passes (`python validate_setup.py`)
- [ ] Test detection works (`python test_detection.py`)
- [ ] Backend server starts (`python api_server.py`)
- [ ] Frontend builds (`cd frontend && npm run build`)

---

## 🆕 For New Users

If you're setting up the project for the first time, simply follow the main setup guides:

1. **Quick Start:** See [QUICKSTART.md](QUICKSTART.md) for experienced developers
2. **Complete Guide:** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions
3. **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

All guides have been updated to reflect the latest versions.

---

## 💡 Why Upgrade?

### Performance Improvements
- **NumPy 2.x:** Up to 2x faster for some operations
- **Python 3.12:** ~10-15% faster than Python 3.10
- **OpenCV 4.10:** Better DNN module performance

### Security
- Flask 3.1 includes security patches
- Werkzeug 3.1 fixes several CVEs
- Latest packages have fewer vulnerabilities

### Compatibility
- Better support for modern operating systems
- Improved Windows 11 compatibility
- Native Apple Silicon (M1/M2/M3) support

### Developer Experience
- Better error messages in Python 3.12
- Improved type hints support
- More robust package dependency resolution

---

## 📞 Need Help?

If you encounter issues during migration:

1. **Check Troubleshooting Guide:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Review Error Messages:** Often contain hints about missing dependencies
3. **Search GitHub Issues:** Others may have faced similar issues
4. **Create New Issue:** Include error message, OS, and Python version

---

## 📅 Maintenance

**Last Updated:** March 2026  
**Compatible With:**
- Python 3.12+
- NumPy 2.1.0
- Flask 3.1.0
- OpenCV 4.10.0.84

**Recommended Review:** Every 6 months to ensure dependencies stay current
