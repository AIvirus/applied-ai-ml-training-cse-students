# Lesson 03 - Computer Vision

**Time:** 35 minutes  |  **Notebook:** `notebooks/03_Computer_Vision.ipynb`

---

## Goal

By the end of this lesson you can explain and try:

- images as **pixels**,
- **image preprocessing**,
- **image classification**, **object detection** and **image segmentation**,
- how **CNN** filters work and what **transfer learning** is,
- the difference between **face detection** and **face recognition**,
- **OCR** (reading text from images),
- **video analytics** and real applications.

---

## Understand

### 1. What is Computer Vision?

**Computer Vision (CV)** is the part of AI that helps computers **see and understand images and videos**.

Examples: face unlock, Google Lens, number-plate reading at toll booths, crop disease apps, X-ray analysis, self-driving cars, counting people in a shop, scanning documents.

### 2. Images are just numbers (pixels)

A digital image is a **grid of tiny dots** called **pixels**. Each pixel is a number.

- **Grayscale image:** one number per pixel, from **0 (black)** to **255 (white)**.
- **Colour image:** three numbers per pixel - **Red, Green, Blue (RGB)** - each 0 to 255. These are called **channels**.

```text
A 3 x 3 grayscale image:        A colour pixel:
[[  0, 128, 255],               [255, 0, 0] = pure red
 [ 50, 200,  30],               [0, 0, 255] = pure blue
 [255, 255,   0]]               [255, 255, 255] = white
```

A phone photo of 4000 x 3000 pixels x 3 channels = **36 million numbers**. Note: OpenCV stores colours in the order **BGR** (blue, green, red), not RGB.

### 3. Image preprocessing

Getting images ready before the AI looks at them:

| Step | Why |
|---|---|
| **Resize** | Models need a fixed size (for example 224 x 224) |
| **Convert to grayscale** | Less data when colour does not matter |
| **Normalise** | Divide by 255 so values are 0 to 1 (helps learning) |
| **Blur** | Remove noise (tiny random dots) |
| **Threshold** | Turn into pure black and white (useful for documents) |
| **Edge detection** | Find outlines of objects |
| **Augmentation** | Make extra training images by flipping, rotating or changing brightness |

### 4. The main Computer Vision tasks

| Task | Question it answers | Output | Example |
|---|---|---|---|
| **Image classification** | What is in this image? | One label | "This is a cat" |
| **Object detection** | What objects are here, and **where**? | Labels + **boxes** | Boxes around every car and person on a road |
| **Image segmentation** | Which **exact pixels** belong to each object? | A colour mask per pixel | Separate road, sky and cars pixel by pixel (self-driving) |

```text
Classification:  "dog"
Detection:       [ box around the dog ]  "dog 0.98"
Segmentation:    every dog pixel painted red
```

Popular models: **ResNet** and **EfficientNet** (classification), **YOLO** (fast detection), **U-Net** and **SAM** (segmentation).

### 5. CNNs - how computers learn to see

You met CNNs in Lesson 01. A **filter** (kernel) is a small grid of numbers, for example 3 x 3. It slides over the image and multiplies-and-adds at every position. Different filters highlight different things - an edge filter makes edges bright. A CNN **learns** its own filters during training.

### 6. Transfer learning

Training a big vision model from zero needs millions of images and expensive GPUs. **Transfer learning** = take a model that is **already trained** on a huge dataset (like ImageNet, 14 million images) and **re-train only the last layer** on your small dataset.

Example: a model that already knows edges, fur, eyes and wheels can learn "healthy leaf" vs "diseased leaf" from just a few hundred photos. This is how most real CV projects start.

### 7. Face detection vs face recognition

These are **different**:

| | Face detection | Face recognition |
|---|---|---|
| Question | **Is there a face**, and where? | **Whose** face is it? |
| Output | A box around each face | A name or ID |
| Example | Camera app focusing on faces | Phone face unlock, attendance systems |
| Privacy risk | Lower | **High** - it identifies people. Needs consent and legal care. |

### 8. OCR - Optical Character Recognition

**OCR** reads **text inside images** and turns it into real, editable text. Examples: scanning documents, reading number plates, Google Lens copying text from a photo, digitising old books.

Steps: clean the image (grayscale, threshold) -> find text areas -> recognise characters -> output text. Tools: **Tesseract** (free, from Google), **EasyOCR**, and cloud services. Modern multimodal LLMs (Lesson 05) can also read text from images.

### 9. Video analytics

A video is just **many images per second** (frames, usually 24 to 60 per second). Video analytics runs CV on each frame and also tracks things **over time**: counting people entering a shop, detecting a fall in a hospital, checking helmets on a construction site, traffic counting.

---

## Do it now

Open `notebooks/03_Computer_Vision.ipynb`, select the `.venv` kernel and run every cell. You will:

- make an image from numbers and look at real photo pixels,
- preprocess a photo (grayscale, resize, blur, threshold, edges),
- apply a CNN-style filter by hand,
- train an image classifier on handwritten digits,
- detect objects (shapes) and draw boxes around them,
- do simple segmentation by colour,
- try OCR (optional - needs Tesseract) and face detection on your own photo (optional).

---

## Check

- [ ] You see the small 5 x 5 image and its pixel numbers.
- [ ] You see the photo in 6 versions (original, gray, blurred, threshold, edges, filter).
- [ ] The digit classifier shows predictions above test images, with about 97 percent or higher accuracy.
- [ ] The shapes image shows green boxes around every shape.
- [ ] The OCR cell either reads the text or prints clear install steps.

---

## What just happened?

- Images are arrays of numbers, so all the maths from Day 1 works on them.
- Preprocessing with **OpenCV** (`cv2`) prepared images.
- A filter made edges bright - exactly what the first layer of a CNN learns to do.
- You did classification (digits), detection (boxes) and segmentation (colour groups).

---

## Try it yourself

1. Change the Canny edge thresholds `(100, 200)` to `(50, 100)`. More or fewer edges?
2. In the segmentation cell, change `K = 4` to `K = 2` and `K = 8`.
3. Put a photo of yourself (or anyone who agrees) as `data/my_photo.jpg` and run the face detection cell.

---

## Optional: install Tesseract for OCR

The `pytesseract` package is already installed, but it needs the **Tesseract program** too.

- **Windows:** download the installer from https://github.com/UB-Mannheim/tesseract/wiki, install with default options (it goes to `C:\Program Files\Tesseract-OCR`). Then restart VS Code.
- **macOS:** install Homebrew from https://brew.sh, then run `brew install tesseract`.
- **Linux (Ubuntu):** `sudo apt install tesseract-ocr`

The notebook finds the Windows default location automatically.

---

## If it does not work

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'cv2'` | Wrong kernel, or run `pip install opencv-python` in the activated terminal. |
| Colours look strange (blue faces) | OpenCV uses BGR. Convert with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` before showing with matplotlib. |
| `TesseractNotFoundError` | Tesseract program is not installed or not found. See the optional section above. It is fine to skip. |
| Face detection finds nothing | Use a clear, front-facing, well-lit photo. Haar detection is old and simple. |

Next: **[Lesson 04 - Other AI domains](04_OTHER_AI_DOMAINS.md)**
