"""
Setup Validation Script for Food Calorie Estimation Project
This script validates that all components are properly installed and configured.
"""

import sys
import os

def check_imports():
    """Check if all required packages are installed"""
    print("=" * 60)
    print("1. Checking Python Packages...")
    print("=" * 60)
    
    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'flask': 'Flask',
        'flask_cors': 'flask-cors'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All required packages are installed!")
        return True

def check_opencv_version():
    """Check OpenCV version and DNN module"""
    print("\n" + "=" * 60)
    print("2. Checking OpenCV Configuration...")
    print("=" * 60)
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        
        # Check if DNN module is available
        if hasattr(cv2, 'dnn'):
            print("✓ OpenCV DNN module is available")
            return True
        else:
            print("✗ OpenCV DNN module is NOT available")
            return False
    except Exception as e:
        print(f"✗ Error checking OpenCV: {e}")
        return False

def check_files():
    """Check if required files exist"""
    print("\n" + "=" * 60)
    print("3. Checking Required Files...")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_files = {
        'Config file': os.path.join(base_dir, 'custom-yolov4-detector.cfg'),
        'Class names': os.path.join(base_dir, 'darknet_yolov4_obj_names.names'),
        'Main notebook': os.path.join(base_dir, 'Food_calorie_estimations_Using_Deep_Learning_And_Computer_Vision.ipynb')
    }
    
    all_exist = True
    
    for name, path in required_files.items():
        if os.path.exists(path):
            print(f"✓ {name}: Found")
        else:
            print(f"✗ {name}: NOT found at {path}")
            all_exist = False
    
    return all_exist

def check_weights():
    """Check if model weights exist"""
    print("\n" + "=" * 60)
    print("4. Checking Model Weights...")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    weights_dir = os.path.join(base_dir, 'weights')
    
    if not os.path.exists(weights_dir):
        print(f"✗ Weights directory not found: {weights_dir}")
        return False
    
    weights_files = [f for f in os.listdir(weights_dir) if f.endswith('.weights')]
    
    if weights_files:
        print(f"✓ Found {len(weights_files)} weight file(s):")
        for wf in weights_files:
            size_mb = os.path.getsize(os.path.join(weights_dir, wf)) / (1024 * 1024)
            print(f"  - {wf} ({size_mb:.1f} MB)")
        return True
    else:
        print("✗ No .weights files found")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n" + "=" * 60)
    print("5. Checking Required Directories...")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_dirs = {
        'Test images': os.path.join(base_dir, 'test_images'),
        'Cropped output': os.path.join(base_dir, 'results', 'cropped_img'),
        'Final results': os.path.join(base_dir, 'results', 'final_result_img')
    }
    
    all_exist = True
    
    for name, path in required_dirs.items():
        if os.path.exists(path):
            file_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            print(f"✓ {name}: Exists ({file_count} files)")
        else:
            print(f"✗ {name}: NOT found")
            all_exist = False
    
    return all_exist

def test_model_loading():
    """Test if the model can be loaded"""
    print("\n" + "=" * 60)
    print("6. Testing Model Loading...")
    print("=" * 60)
    
    try:
        import cv2
        import numpy as np
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Use the best weights file
        weights_dir = os.path.join(base_dir, 'weights')
        weights_files = [f for f in os.listdir(weights_dir) if f.endswith('.weights')]
        
        if not weights_files:
            print("✗ No weights files found")
            return False
        
        # Pick the best or first available weights
        weights_file = None
        for pref in ['3000(98.61)', 'best', 'last', '1000']:
            for wf in weights_files:
                if pref in wf:
                    weights_file = wf
                    break
            if weights_file:
                break
        
        if not weights_file:
            weights_file = weights_files[0]
        
        model_path = os.path.join(weights_dir, weights_file)
        cfg_path = os.path.join(base_dir, 'custom-yolov4-detector.cfg')
        
        print(f"Loading model: {weights_file}")
        net = cv2.dnn.readNet(model_path, cfg_path)
        
        print("✓ Model loaded successfully!")
        
        # Check layer names
        layer_names = net.getLayerNames()
        print(f"✓ Model has {len(layer_names)} layers")
        
        # Check output layers
        unconnected = net.getUnconnectedOutLayers()
        print(f"✓ Model has {len(unconnected)} output layer(s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

def main():
    """Run all validation checks"""
    print("\n" + "=" * 60)
    print("FOOD CALORIE ESTIMATION - SETUP VALIDATION")
    print("=" * 60)
    
    checks = []
    
    checks.append(("Packages", check_imports()))
    checks.append(("OpenCV", check_opencv_version()))
    checks.append(("Files", check_files()))
    checks.append(("Weights", check_weights()))
    checks.append(("Directories", check_directories()))
    checks.append(("Model Loading", test_model_loading()))
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! The project is ready to use.")
        print("\n📝 NEXT STEPS:")
        print("   1. Add test images (with food + thumb) to 'test_images' folder")
        print("   2. Open Food_calorie_estimations_Using_Deep_Learning_And_Computer_Vision.ipynb")
        print("   3. Run all cells in the notebook")
        print("\n💡 TIP: Place your thumb next to food items in photos for accurate size calibration!")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
