# bulk_image_process_script_

Background: Background removal · Beautify · Blemish removal · Face detection · Batch photo processing (Python)

Overview
This repository provides a Python script for batch image processing. Features include: automatic resizing to a target width, optional face-based beautification (skin smoothing, blemish removal, whitening/brightness tweaks), preserving and writing back original EXIF metadata, and more.

A. Environment & Requirements
- Tested on:
  - Windows 10
  - Ubuntu Server 22.04 LTS
- Supported Python versions:
  - Python 3.10
  - Python 3.11
- Dependencies (see `requirements.txt`, install with `pip install -r requirements.txt`):
  - Pillow (image I/O)
  - opencv-python (image processing)
  - numpy (numerical operations)
  - face_recognition (face detection/recognition; relies on dlib)
  - dlib (required by face_recognition)
  - rembg (optional — background removal / matting)
  - piexif (read/write EXIF)
  - tqdm (progress bars)
  - scikit-image (optional additional image algorithms)

Note: dlib may require CMake and a C/C++ build toolchain on some platforms or prebuilt wheels. If you encounter installation problems, consult the dlib/face_recognition installation instructions or use conda for prebuilt packages.

B. Usage / What it does
What the script can do:
- Read image files in a folder (supports common formats including HEIC where available);
- Resize images proportionally to a target width (e.g. 1920 px);
- Apply face-based beautification when faces are detected (smoothing, blemish removal, brightness/whitening adjustments);
- Optionally remove background / perform foreground matting when enabled;
- Read original EXIF metadata and write EXIF back to processed images (preserving capture time, camera info, GPS, etc.);
- Save processed files to a `new/` subfolder inside the input directory (original files are kept unchanged).

Quick start (recommended):
1. Install dependencies:
   pip install -r requirements.txt
2. Place the repository or the script in any folder where you want to run it (for example, put `beauty_ult.py` in the folder with your images).
3. Run the script:
   python beauty_ult.py
   - The script will scan the current directory and its subfolders for images and list folders it can process;
   - You can also manually input the path to process when prompted by the script.
4. After processing completes, a `new/` folder will be created in the chosen path and all processed images will be saved there.

(Default parameters are used inside the script. To change target width or beautification strength, edit variables such as `target_width`, `dist`, `brighten_factor` inside the script.)

C. Process / Flow / Key variables
Typical processing flow:
1. Scan the input directory and enumerate supported image formats (jpg, jpeg, png, webp, HEIC, etc.).
2. For each image:
   - Read and preserve original EXIF (if present);
   - Resize proportionally to the target width (`target_width`, default 1920);
   - Face detection: if faces are detected, locate face regions and apply beautification (smoothing, blemish removal, brightness adjustments). If no face is detected, beautification is skipped for that image;
   - Optionally perform background removal / matting when enabled;
   - Write modified EXIF back to the output image;
   - Save the output image under `output/new/` (or another directory you configure).
3. Produce processing logs / progress output.

Example default configuration values:
- target_width = 1920
- dist = 20              # smoothing strength (larger values = stronger smoothing; exact scale depends on implementation)
- brighten_factor = 1.15 # whitening/brightness multiplier (1.0 = unchanged, 1.15 = +15%)

D. Advantages
- EXIF preservation: processed images retain capture time, camera information, GPS data, etc., which is useful when importing into photo managers such as immich or PhotoPrism;
- Face-driven beautification: only detected faces are processed to avoid altering animals or landscape photos incorrectly;
- One-step beautify + blemish removal + whitening: automates repetitive editing and saves manual time;
- Low-spec friendly: defaults work on most ordinary PCs/laptops without a GPU (GPU acceleration is supported when available);
- Time saver: suitable for large photo sets (travel, weddings, social media content) or anyone who needs to batch-edit many images.

E. Motivation
The goal of this script is to save time on repetitive manual retouching while preserving original EXIF metadata for later use (for example in PhotoPrism or Immich). There were no readily available open-source tools that matched the need for batch beautification while preserving EXIF, so this project was created to fill that gap.

FAQ & Notes
- EXIF cannot be written back or is lost: make sure the source file actually contains EXIF and that the target format supports EXIF (JPEG supports EXIF; PNG/WEBP have different EXIF support across tools).
- face_recognition / dlib install issues: try installing prebuilt wheels via conda, or follow platform-specific build instructions for dlib.
- Background removal quality depends on the chosen tool (rembg, etc.) and may not perform well on complex backgrounds. Test with a small batch first and adjust parameters.

License
This project is licensed under the MIT License (see the LICENSE file in the repository root).

Contributing
Contributions, issues and pull requests are welcome. If you improve beautification algorithms or add acceleration options, please keep the README usage instructions and add examples where applicable.
