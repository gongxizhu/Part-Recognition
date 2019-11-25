# Part_Recognition
Proof of Concept for Volvo Bus Poland Factory, targeting at recognizing Vehicle Parts in the Factory.

# Model
Using InceptionResV2 as a encoder to convert images to 128-vectors, and train a SVM to classify.

# Requirements
  1. Python >=3.6
  2. Tensorflow >=1.8
  3. OpenCV
  4. numpy
  5. PIL
  6. PyQT5

# UI
python desktop_ui/main_ui.py

# Web API
python web_api/app.py

# Convert video to images
python convert_video_to_images.py

# Prepare Dataset
python prepare_dataset.py
