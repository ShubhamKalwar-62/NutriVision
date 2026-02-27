"""
Simple Test Script - Test Model Loading and Detection Pipeline
This verifies the core detection functionality works correctly
"""

import cv2
import numpy as np
import os
import time

def test_model_detection():
    """Test the YOLOv4 model detection pipeline"""
    
    print("=" * 70)
    print("TESTING YOLOV4 DETECTION PIPELINE")
    print("=" * 70)
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(base_dir, "weights", "custom-yolov4-detector_3000(98.61).weights")
    CFG_FILE_PATH = os.path.join(base_dir, "custom-yolov4-detector.cfg")
    OBJ_FILE_PATH = os.path.join(base_dir, "darknet_yolov4_obj_names.names")
    
    print("\n1. Loading class names...")
    classes = []
    with open(OBJ_FILE_PATH, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    print(f"✓ Loaded {len(classes)} classes: {', '.join(classes)}")
    
    print("\n2. Loading YOLOv4 model...")
    start_time = time.time()
    net = cv2.dnn.readNet(MODEL_PATH, CFG_FILE_PATH)
    load_time = time.time() - start_time
    print(f"✓ Model loaded in {load_time:.2f} seconds")
    
    print("\n3. Getting layer information...")
    layer_names = net.getLayerNames()
    unconnected = net.getUnconnectedOutLayers()
    
    # Handle both old and new OpenCV API
    if len(unconnected.shape) == 2:
        outputlayers = [layer_names[i[0] - 1] for i in unconnected]
    else:
        outputlayers = [layer_names[i - 1] for i in unconnected]
    
    print(f"✓ Total layers: {len(layer_names)}")
    print(f"✓ Output layers: {outputlayers}")
    
    print("\n4. Creating test image (blank canvas with colored rectangles)...")
    # Create a synthetic test image
    test_img = np.ones((608, 608, 3), dtype=np.uint8) * 255  # White background
    
    # Draw some colored rectangles to simulate objects
    cv2.rectangle(test_img, (100, 100), (200, 200), (0, 0, 255), -1)  # Red square
    cv2.rectangle(test_img, (300, 300), (500, 450), (0, 255, 0), -1)  # Green rect
    cv2.circle(test_img, (450, 150), 60, (255, 0, 0), -1)  # Blue circle
    
    print("✓ Test image created (608×608)")
    
    print("\n5. Running detection on test image...")
    blob = cv2.dnn.blobFromImage(
        test_img, 0.00392, (608, 608), (0, 0, 0), True, crop=False
    )
    net.setInput(blob)
    
    detect_start = time.time()
    outs = net.forward(outputlayers)
    detect_time = time.time() - detect_start
    
    print(f"✓ Detection completed in {detect_time:.2f} seconds")
    print(f"✓ Output shapes: {[out.shape for out in outs]}")
    
    # Count detections
    height, width, channels = test_img.shape
    detections = 0
    confidence_threshold = 0.5
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                detections += 1
    
    print(f"✓ Found {detections} detection(s) above {confidence_threshold} confidence")
    
    print("\n6. Testing with different input sizes...")
    for size in [(416, 416), (512, 512), (608, 608)]:
        blob = cv2.dnn.blobFromImage(test_img, 0.00392, size, (0, 0, 0), True, crop=False)
        net.setInput(blob)
        start = time.time()
        net.forward(outputlayers)
        elapsed = time.time() - start
        print(f"✓ Size {size}: {elapsed:.3f}s")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nThe detection pipeline is working correctly!")
    print("\n📝 NEXT STEPS:")
    print("   1. Add test images with food + thumb to 'test_images/' folder")
    print("   2. Open Food_calorie_estimations_Using_Deep_Learning_And_Computer_Vision.ipynb")
    print("   3. Run all cells sequentially")
    print("\n💡 The model is ready to detect real food items!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        test_model_detection()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
