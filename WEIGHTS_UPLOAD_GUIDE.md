# Model Weights Upload Guide

This guide explains how to upload your model weights to Google Drive or Hugging Face.

## Option 1: Google Drive (Current Setup)

### Steps:
1. **Go to Google Drive**: https://drive.google.com
2. **Create a folder** (or use existing): `NutriVision-Weights`
3. **Upload the weight file**: 
   - `custom-yolov4-detector_3000(98.61).weights`
4. **Make it public**:
   - Right-click the file or folder
   - Click **Share**
   - Change to **"Anyone with the link"** can view
   - Click **Copy link**
5. **Update README.md**: Replace the Google Drive link with your new link

### Current Status:
✅ Already set up at: https://drive.google.com/drive/folders/13kAvdJRTdD1-EBWndrdziyN0sXqczoZU?usp=sharing

---

## Option 2: Hugging Face (Recommended for ML Projects)

### Why Hugging Face?
- ✅ Built for ML models
- ✅ Version control (Git LFS)
- ✅ Better download speeds
- ✅ Automatic model card generation
- ✅ Integration with ML community

### Steps:

#### 1. Create Hugging Face Account
- Sign up at: https://huggingface.co/join
- Verify your email

#### 2. Create a Model Repository
- Go to: https://huggingface.co/new
- **Owner**: Your username
- **Model name**: `nutrivision-yolov4-weights`
- **License**: `cc-by-nc-4.0` (to match your project)
- **Visibility**: Public
- Click **Create model**

#### 3. Upload via Web UI (Easiest)
1. In your new repo, click **Files** → **Add file** → **Upload files**
2. Drag and drop: `custom-yolov4-detector_3000(98.61).weights`
3. Add a commit message: "Add YOLOv4 weights (98.61% mAP)"
4. Click **Commit changes**

#### 4. Create Model Card
Create a README.md in the repo with:

```markdown
---
license: cc-by-nc-4.0
tags:
- computer-vision
- object-detection
- yolov4
- food-recognition
---

# NutriVision YOLOv4 Weights

YOLOv4 model weights for food detection and calorie estimation.

## Model Details
- **Model**: YOLOv4 (Darknet)
- **Accuracy**: 98.61% mAP on validation set
- **Classes**: Apple, Banana, Carrot, Onion, Orange, Kiwi, Tomato, Thumb
- **Training**: Custom trained on Roboflow dataset

## Usage
Download and place in `weights/` directory:
```bash
wget https://huggingface.co/YOUR-USERNAME/nutrivision-yolov4-weights/resolve/main/custom-yolov4-detector_3000(98.61).weights
```

## Project
Part of [NutriVision](https://github.com/ShubhamKalwar-62/NutriVision) - Food calorie estimation using deep learning.
```

#### 5. Update Your Project README
Replace the Hugging Face link in your main README.md:
```markdown
[Hugging Face](https://huggingface.co/YOUR-USERNAME/nutrivision-yolov4-weights)
```

---

## Option 3: Git LFS (For Advanced Users)

If you want to keep weights in your GitHub repo using Git LFS:

### Steps:
1. **Install Git LFS**: https://git-lfs.github.com/
2. **Initialize Git LFS**:
   ```bash
   git lfs install
   ```
3. **Track weight files**:
   ```bash
   git lfs track "weights/*.weights"
   git add .gitattributes
   ```
4. **Add and commit weights**:
   ```bash
   git add weights/custom-yolov4-detector_3000(98.61).weights
   git commit -m "Add model weights via Git LFS"
   git push
   ```

**Note**: Git LFS has bandwidth limits on free accounts (1 GB/month).

---

## Recommended Approach

For the best experience, we recommend:

1. **Google Drive** for quick setup and sharing (current setup ✅)
2. **Hugging Face** for professional ML project hosting and better integration
3. **Both** for redundancy and faster worldwide downloads

---

## After Uploading

Update the download links in:
- `README.md` - Main documentation
- Social media posts
- Project presentations

Test the download link in an incognito/private browser window to ensure it's publicly accessible.
