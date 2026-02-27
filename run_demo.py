"""
Demo Runner - Downloads sample food images and runs detection
This script helps you test the project without requiring your own images
"""

import os
import sys
import urllib.request
import ssl

def download_sample_images():
    """Download sample food images from the internet"""
    print("=" * 60)
    print("DOWNLOADING SAMPLE IMAGES")
    print("=" * 60)
    
    # Create SSL context to handle HTTPS
    ssl._create_default_https_context = ssl._create_unverified_context
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_images_dir = os.path.join(base_dir, 'test_images')
    
    # Sample images URLs (these are examples - you'll need actual URLs with food + hands)
    sample_images = [
        {
            'name': 'sample_apple.jpg',
            'url': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=800',
            'description': 'Apple with hand reference'
        },
        {
            'name': 'sample_banana.jpg',
            'url': 'https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=800',
            'description': 'Banana with hand reference'
        }
    ]
    
    print("\n⚠️  NOTE: For accurate results, images should include:")
    print("   - Food items (Apple, Banana, Carrot, Onion, Orange, Kiwi, Tomato)")
    print("   - Visible THUMB for size calibration (5 × 2.3 cm)")
    print()
    
    downloaded = 0
    for img_info in sample_images:
        output_path = os.path.join(test_images_dir, img_info['name'])
        
        if os.path.exists(output_path):
            print(f"✓ {img_info['name']} already exists")
            downloaded += 1
            continue
        
        try:
            print(f"Downloading {img_info['description']}...")
            urllib.request.urlretrieve(img_info['url'], output_path)
            print(f"✓ Saved: {img_info['name']}")
            downloaded += 1
        except Exception as e:
            print(f"✗ Failed to download {img_info['name']}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Downloaded {downloaded} image(s) to test_images/")
    print(f"{'='*60}\n")
    
    return downloaded > 0

def show_instructions():
    """Show instructions for running the notebook"""
    print("\n" + "=" * 60)
    print("NEXT STEPS - RUN THE NOTEBOOK")
    print("=" * 60)
    print("""
1. Open the notebook:
   Food_calorie_estimations_Using_Deep_Learning_And_Computer_Vision.ipynb

2. Run cells in order:
   - Cell 1: Import libraries
   - Cell 2: Configure paths (already set!)
   - Cells 3-9: Load model and functions
   - Last cell: Main execution loop

3. When prompted:
   - Select image number (e.g., 0)
   - Choose scaling option (recommended: 1 for 608×608)

4. Results will be saved to:
   - results/final_result_img/ (annotated images)
   - results/cropped_img/ (cropped objects)

5. The notebook will show:
   - Detected objects with confidence
   - Calculated areas and volumes
   - Estimated calories per food item

⚠️  IMPORTANT:
   The model requires THUMB detection for size calibration.
   If you're using your own images, make sure your thumb is
   clearly visible next to the food items!
""")
    print("=" * 60)

def main():
    print("\n" + "=" * 60)
    print("FOOD CALORIE ESTIMATION - DEMO SETUP")
    print("=" * 60)
    print("\nThis script will help you test the project.\n")
    
    # Check if test_images directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_images_dir = os.path.join(base_dir, 'test_images')
    
    if not os.path.exists(test_images_dir):
        print(f"Creating test_images directory...")
        os.makedirs(test_images_dir)
    
    # Check if there are already images
    existing_images = [f for f in os.listdir(test_images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if existing_images:
        print(f"\n✓ Found {len(existing_images)} existing image(s) in test_images/:")
        for img in existing_images[:5]:  # Show first 5
            print(f"  - {img}")
        if len(existing_images) > 5:
            print(f"  ... and {len(existing_images) - 5} more")
        print("\n✅ You can proceed directly to running the notebook!")
        show_instructions()
        return 0
    
    # No images found - guide user
    print("\n⚠️  No images found in test_images/ folder")
    print("\nTo test this project, you need images with:")
    print("  1. Food items (Apple, Banana, Carrot, Onion, Orange, Kiwi, Tomato)")
    print("  2. Your THUMB visible for size calibration")
    print()
    
    choice = input("Options:\n"
                  "  [1] I'll add my own images manually\n"
                  "  [2] Show me how to get sample images\n"
                  "  [3] Exit\n"
                  "Choose (1-3): ").strip()
    
    if choice == '1':
        print("\n📸 Great! Please:")
        print(f"   1. Add food images to: {test_images_dir}")
        print("   2. Ensure thumb is visible in each image")
        print("   3. Then run the main notebook")
        show_instructions()
        
    elif choice == '2':
        print("\n💡 HOW TO GET TEST IMAGES:")
        print("\nOption A - Take Your Own Photos:")
        print("  1. Place food items on a table")
        print("  2. Put your thumb next to them")
        print("  3. Take clear photos")
        print(f"  4. Save to: {test_images_dir}")
        print("\nOption B - Search Online:")
        print("  1. Search: 'apple with hand' or 'fruits with size reference'")
        print("  2. Download images")
        print(f"  3. Save to: {test_images_dir}")
        print("\nOption C - Use Dataset:")
        print("  1. Visit: https://app.roboflow.com/chetan-projects-object-detcions/fruits--and-thumb-detection")
        print("  2. Download sample images from the project dataset")
        print(f"  3. Save to: {test_images_dir}")
        show_instructions()
        
    else:
        print("\nExiting. Add images to test_images/ folder when ready!")
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
