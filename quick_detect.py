"""
Quick Detection Runner - Processes all images in test_images folder
This script runs detection without the interactive notebook interface
"""

import cv2
import numpy as np
import os
import time

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_IMG_FOLDER_PATH = os.path.join(BASE_DIR, "test_images")
MODEL_PATH = os.path.join(BASE_DIR, "weights", "custom-yolov4-detector_3000(98.61).weights")
CFG_FILE_PATH = os.path.join(BASE_DIR, "custom-yolov4-detector.cfg")
OBJ_FILE_PATH = os.path.join(BASE_DIR, "darknet_yolov4_obj_names.names")
WRITE_CROPPED_IMG_PATH = os.path.join(BASE_DIR, "results", "cropped_img")
IMG_RESULT_PATH = os.path.join(BASE_DIR, "results", "final_result_img")

def main():
    print("="*70)
    print("FOOD CALORIE ESTIMATION - QUICK DETECTION")
    print("="*70)
    
    # Load classes
    print("\n1. Loading class names...")
    classes = []
    with open(OBJ_FILE_PATH, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    print(f"✓ Loaded {len(classes)} classes: {', '.join(classes)}")
    
    # Load model
    print("\n2. Loading YOLOv4 model...")
    start_time = time.time()
    net = cv2.dnn.readNet(MODEL_PATH, CFG_FILE_PATH)
    print(f"✓ Model loaded in {time.time() - start_time:.2f}s")
    
    # Get output layers
    layer_names = net.getLayerNames()
    unconnected = net.getUnconnectedOutLayers()
    if len(unconnected.shape) == 2:
        outputlayers = [layer_names[i[0] - 1] for i in unconnected]
    else:
        outputlayers = [layer_names[i - 1] for i in unconnected]
    
    # Get images
    print("\n3. Finding images in test_images folder...")
    image_files = [f for f in os.listdir(TEST_IMG_FOLDER_PATH) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ No images found in test_images/ folder!")
        print("\n📸 Please add images with food + thumb to test_images/")
        return 1
    
    print(f"✓ Found {len(image_files)} image(s)")
    for i, img_file in enumerate(image_files):
        print(f"   {i+1}. {img_file}")
    
    # Process each image
    print("\n4. Processing images...\n")
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    
    for img_name in image_files:
        print(f"\n{'='*70}")
        print(f"Processing: {img_name}")
        print(f"{'='*70}")
        
        # Read image
        img_path = os.path.join(TEST_IMG_FOLDER_PATH, img_name)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"❌ Failed to load {img_name}")
            continue
        
        # Resize to 608x608 for detection
        img_resized = cv2.resize(img, (608, 608))
        height, width, channels = img_resized.shape
        
        # Detect objects
        blob = cv2.dnn.blobFromImage(
            img_resized, 0.00392, (608, 608), (0, 0, 0), True, crop=False
        )
        net.setInput(blob)
        
        detect_start = time.time()
        outs = net.forward(outputlayers)
        detect_time = time.time() - detect_start
        
        # Parse detections
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.5:  # 50% confidence threshold
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply Non-Maximum Suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        print(f"\n✓ Detection completed in {detect_time:.2f}s")
        print(f"✓ Found {len(indexes)} object(s):\n")
        
        # Draw boxes and labels
        result_img = img_resized.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = f"{classes[class_ids[i]]}: {confidences[i]*100:.1f}%"
                color = colors[class_ids[i]]
                
                # Draw bounding box
                cv2.rectangle(result_img, (x, y), (x + w, y + h), color, 2)
                
                # Draw label background
                (label_w, label_h), _ = cv2.getTextSize(label, font, 0.6, 2)
                cv2.rectangle(result_img, (x, y - label_h - 10), (x + label_w, y), color, -1)
                
                # Draw label text
                cv2.putText(result_img, label, (x, y - 5), font, 0.6, (255, 255, 255), 2)
                
                print(f"  • {classes[class_ids[i]]:<10} - {confidences[i]*100:>5.1f}% confidence")
        else:
            print("  ⚠️  No objects detected above 50% confidence threshold")
        
        # Save result
        output_path = os.path.join(IMG_RESULT_PATH, f"result_{img_name}")
        cv2.imwrite(output_path, result_img)
        print(f"\n✓ Result saved: {output_path}")
    
    print("\n" + "="*70)
    print("✅ ALL IMAGES PROCESSED!")
    print("="*70)
    print(f"\n📁 Results saved to: {IMG_RESULT_PATH}")
    print("\n💡 Check the results folder to see detected objects!")
    
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
