"""
Complete Food Calorie Estimation Pipeline
Includes: Detection → Segmentation → Volume Calculation → Calorie Estimation
"""

import cv2
import numpy as np
import os
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_IMG_FOLDER_PATH = os.path.join(BASE_DIR, "test_images")
MODEL_PATH = os.path.join(BASE_DIR, "weights", "custom-yolov4-detector_3000(98.61).weights")
CFG_FILE_PATH = os.path.join(BASE_DIR, "custom-yolov4-detector.cfg")
OBJ_FILE_PATH = os.path.join(BASE_DIR, "darknet_yolov4_obj_names.names")
WRITE_CROPPED_IMG_PATH = os.path.join(BASE_DIR, "results", "cropped_img")
IMG_RESULT_PATH = os.path.join(BASE_DIR, "results", "final_result_img")

# Constants
SKIN_MULTIPLIER = 5 * 2.3  # Thumb area in cm²
PIXEL_TO_CM_MULTIPLIER_CONSTANT = 5.0

# Density (g/cm³) and Calories (kcal/100g)
density_dict = {
    "Apple": 0.96, "Banana": 0.94, "Carrot": 0.641,
    "Onion": 0.513, "Orange": 0.482, "Tomato": 0.481, "Qiwi": 0.575
}
calorie_dict = {
    "Apple": 52, "Banana": 89, "Carrot": 41,
    "Onion": 40, "Orange":47, "Tomato": 18, "Qiwi": 44
}
label_list = ["thumb", "Apple", "Banana", "Orange", "Qiwi", "Tomato", "Carrot", "Onion"]


def crop_img(input_img, img_name, bb_cordinate, img_save_path=None, pixel_margin=5):
    """Crop image based on bounding box coordinates"""
    dh, dw, cha = input_img.shape
    
    for i in range(len(bb_cordinate)):
        if bb_cordinate[i] < 0:
            bb_cordinate[i] = abs(bb_cordinate[i])
    
    xmin, ymin, w, h = bb_cordinate
    p = pixel_margin
    
    X_MIN = max(xmin - p, 0)
    Y_MIN = max(ymin - p, 0)
    Y_MAX = min((ymin + h) + p, dh)
    X_MAX = min((xmin + w) + p, dw)
    
    imgCrop = input_img[Y_MIN:Y_MAX, X_MIN:X_MAX]
    
    if img_save_path:
        cv2.imwrite(os.path.join(img_save_path, img_name), imgCrop)
    
    return {"img_name": img_name, "cropped_image": imgCrop}


def image_segmentation(cropped_img_name, cropped_img):
    """Perform image segmentation to extract object contours"""
    cv2_img = cropped_img
    cv2_img_gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    
    adap_thresh = cv2.adaptiveThreshold(
        cv2_img_gray, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2
    )
    
    contours, hierarchy = cv2.findContours(adap_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_areas = sorted(contours, key=cv2.contourArea)
    
    mask = np.zeros(cv2_img_gray.shape, np.uint8)
    img_contour = cv2.drawContours(mask, [largest_areas[-1]], 0, (255, 255, 255, 255), -1)
    
    plt_img = cropped_img
    img_bitcontour = cv2.bitwise_or(plt_img, plt_img, mask=mask)
    hsv_img = cv2.cvtColor(img_bitcontour, cv2.COLOR_BGR2HSV)
    
    mask_plate = cv2.inRange(hsv_img, np.array([0, 0, 50]), np.array([200, 90, 250]))
    mask_not_plate = cv2.bitwise_not(mask_plate)
    mask_fruit = cv2.bitwise_and(img_bitcontour, img_bitcontour, mask=mask_not_plate)
    
    rgb_img = mask_fruit.copy()
    img_gray2 = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    ret, thr = cv2.threshold(img_gray2, 10, 255, cv2.THRESH_BINARY)
    
    contours2, hierarchy2 = cv2.findContours(thr, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_areas2 = sorted(contours2, key=cv2.contourArea)
    
    result = []
    
    # For thumb detection
    if "thumb" in cropped_img_name.lower():
        req_contour = largest_areas2[-2] if len(largest_areas2) >= 2 else largest_areas2[-1]
        req_object_area = cv2.contourArea(req_contour)
        
        rect = cv2.minAreaRect(req_contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)  # Compatible with numpy 2.x
        Thumb_img_min_rectangle = cv2.drawContours(rgb_img.copy(), [box], 0, (255, 255, 0), 2)
        
        width, height = rect[1]
        max_dimension = max(width, height)
        if max_dimension > 0:
            pix_to_cm_multiplier = PIXEL_TO_CM_MULTIPLIER_CONSTANT / max_dimension
        else:
            pix_to_cm_multiplier = 1.0  # Fallback value
        
        result = [req_contour, req_object_area, pix_to_cm_multiplier]
    else:
        # For fruit detection
        req_contour = largest_areas2[-1]
        req_object_area = cv2.contourArea(req_contour)
        result = [req_contour, req_object_area]
    
    return {"segmented_obj_contour_area_pixel": result}


def getVolume(label, area, skin_area, pix_to_cm_multiplier, fruit_contour):
    """Calculate volume based on fruit shape assumptions"""
    area_fruit = (area / skin_area) * SKIN_MULTIPLIER
    volume = 100
    
    # Sphere: Apple, Orange, Kiwi, Tomato, Onion
    if label in ["Apple", "Orange", "Qiwi", "Tomato", "Onion"]:
        radius = np.sqrt(area_fruit / np.pi)
        volume = (4 / 3) * np.pi * radius ** 3
    
    # Cylinder: Banana, Carrot
    elif label in ["Banana", "Carrot"] and area_fruit > 30:
        try:
            fruit_rect = cv2.minAreaRect(fruit_contour)
            height = max(fruit_rect[1]) * pix_to_cm_multiplier
            radius = area_fruit / (2.0 * height)
            volume = np.pi * radius * radius * height
        except:
            volume = area_fruit * 2  
    
    elif label == "Carrot" and area_fruit < 30:
        volume = area_fruit * 0.5
    
    return volume


def getCalorie(label, volume):
    """Calculate calories based on volume and density"""
    calorie = calorie_dict.get(label, 50)
    density = density_dict.get(label, 0.5)
    mass = volume * density
    calorie_tot = (calorie / 100.0) * mass
    return mass, calorie_tot, calorie


def process_image(img_path, net, layer_names, outputlayers, classes, colors):
    """Process a single image through the complete pipeline"""
    print(f"\n{'='*70}")
    print(f"Processing: {os.path.basename(img_path)}")
    print(f"{'='*70}")
    
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Failed to load image")
        return None
    
    # Resize to 608x608
    img_resized = cv2.resize(img, (608, 608))
    height, width, channels = img_resized.shape
    
    # Detect objects
    blob = cv2.dnn.blobFromImage(img_resized, 0.00392, (608, 608), (0, 0, 0), True, crop=False)
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
            
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply NMS
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    print(f"\n✓ Detection completed in {detect_time:.2f}s")
    print(f"✓ Found {len(indexes)} object(s)")
    
    if len(indexes) == 0:
        print("⚠️  No objects detected")
        return None
    
    segmentation_data = {}
    
    for i in indexes.flatten():
        label = classes[class_ids[i]]
        conf = confidences[i]
        box = boxes[i]
        
        img_name = f"{label}({round(conf*100, 2)})_{i}.jpg"
        
        # Crop image
        cropped_data = crop_img(img_resized, img_name, box, WRITE_CROPPED_IMG_PATH)
        cropped_img = cropped_data["cropped_image"]
        
        # Segment
        seg_result = image_segmentation(img_name, cropped_img)
        segmentation_data[img_name] = [seg_result["segmented_obj_contour_area_pixel"], box]
    
    
    print(f"\n{'='*70}")
    print("CALORIE ESTIMATION")
    print(f"{'='*70}")
    
    # Find thumb data
    skin_contour_Area = None
    pix_cm = None
    
    for k in segmentation_data:
        if k.startswith("thumb"):
            skin_contour_Area = segmentation_data[k][0][1]
            pix_cm = segmentation_data[k][0][2]
            print(f"✓ Found thumb reference (area: {skin_contour_Area:.1f} pixels)")
            break
    
    if skin_contour_Area is None:
        print("\n⚠️  WARNING: No thumb detected for size calibration!")
        print("    Calorie estimation requires a visible thumb in the image.")
        print("    Only detection results will be shown.\n")
    
    # Calculate calories
    final_results = {}
    result_img = img_resized.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    for k in segmentation_data:
        name = k.split("_")[0].split("(")[0]
        conf_str = k.split("_")[0]
        bbNum = k.split("_")[1][:-4]
        box = segmentation_data[k][1]
        x, y, w, h = box
        
        if k.startswith("thumb"):
            label_text = f"{conf_str}"
            color = colors[7]  # thumb color
        else:
            if skin_contour_Area is not None and pix_cm is not None:
                fruit_contour = segmentation_data[k][0][0]
                fruit_area = segmentation_data[k][0][1]
                
                volume = getVolume(name, fruit_area, skin_contour_Area, pix_cm, fruit_contour)
                mass, calories, cal_per_100g = getCalorie(name, volume)
                
                print(f"\n{name}:")
                print(f"  Volume: {volume:.2f} cm³")
                print(f"  Mass: {mass:.2f} g")
                print(f"  Calories: {calories:.1f} kcal")
                
                label_text = f"{name} {round(calories)}kcal"
                color = colors[class_ids[int(bbNum)]]
            else:
                label_text = f"{conf_str}"
                color = colors[class_ids[int(bbNum)]]
        
        # Draw on image
        cv2.rectangle(result_img, (x, y), (x + w, y + h), color, 2)
        
        # Label background
        (label_w, label_h), _ = cv2.getTextSize(label_text, font, 0.6, 2)
        cv2.rectangle(result_img, (x, y - label_h - 10), (x + label_w, y), color, -1)
        cv2.putText(result_img, label_text, (x, y - 5), font, 0.6, (255, 255, 255), 2)
    
    # Save result
    output_name = f"result_{os.path.basename(img_path)}"
    output_path = os.path.join(IMG_RESULT_PATH, output_name)
    cv2.imwrite(output_path, result_img)
    print(f"\n✓ Result saved: {output_path}")
    
    return result_img


def main():
    print("="*70)
    print("COMPLETE FOOD CALORIE ESTIMATION PIPELINE")
    print("="*70)
    
    # Load classes
    print("\n1. Loading classes...")
    with open(OBJ_FILE_PATH, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    print(f"✓ Loaded {len(classes)} classes")
    
    # Load model
    print("\n2. Loading YOLOv4 model...")
    start_time = time.time()
    net = cv2.dnn.readNet(MODEL_PATH, CFG_FILE_PATH)
    print(f"✓ Model loaded in {time.time() - start_time:.2f}s")
    
    # Get layer names
    layer_names = net.getLayerNames()
    unconnected = net.getUnconnectedOutLayers()
    if len(unconnected.shape) == 2:
        outputlayers = [layer_names[i[0] - 1] for i in unconnected]
    else:
        outputlayers = [layer_names[i - 1] for i in unconnected]
    
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    
    # Get images
    print("\n3. Finding images...")
    image_files = [f for f in os.listdir(TEST_IMG_FOLDER_PATH) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ No images found in test_images/")
        return 1
    
    print(f"✓ Found {len(image_files)} image(s)")
    
    # Process each image
    print("\n4. Processing images with full calorie estimation...\n")
    
    for img_file in image_files:
        img_path = os.path.join(TEST_IMG_FOLDER_PATH, img_file)
        process_image(img_path, net, layer_names, outputlayers, classes, colors)
    
    print("\n" + "="*70)
    print("✅ ALL IMAGES PROCESSED WITH CALORIE ESTIMATION!")
    print("="*70)
    print(f"\n📁 Results: {IMG_RESULT_PATH}")
    print(f"📁 Cropped: {WRITE_CROPPED_IMG_PATH}")
    print("\n💡 Check results folder for annotated images with calorie information!")
    
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
