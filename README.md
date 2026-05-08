# AI Traffic Sign Recognition

A CNN-based traffic sign classification system trained on the GTSRB dataset, with Grad-CAM explainability and an interactive Streamlit interface.

**Live Demo:** [Hugging Face Spaces](https://huggingface.co/spaces/agstyn/ai-traffic-sign-recognition) &nbsp;·&nbsp; **Source:** [GitHub](https://github.com/agstyn/ai-traffic-sign-recognition)

---

## Overview

This project classifies road traffic signs across 43 categories using a Convolutional Neural Network trained on the German Traffic Sign Recognition Benchmark (GTSRB). Beyond classification, the system integrates Grad-CAM heatmaps to make predictions interpretable — highlighting the image regions the model actually relies on when making a decision.

The interface is built in Streamlit and supports real-time inference, confidence visualization, and category filtering.

---

## Model Performance

| Metric              | Value  |
|---------------------|--------|
| Validation Accuracy | 99.87% |
| Training Images     | 39,209 |
| Classes             | 43     |
| Dataset             | GTSRB  |

---

## Features

- 43-class traffic sign classification
- Grad-CAM explainability heatmaps to visualize CNN attention regions
- Confidence score visualization per prediction
- Category filtering for focused inference
- Modern dark-themed Streamlit UI
- Deployable on Hugging Face Spaces

---

## Tech Stack

- **Language:** Python
- **Deep Learning:** TensorFlow / Keras
- **Explainability:** Grad-CAM (gradient-weighted class activation mapping)
- **UI:** Streamlit
- **Image Processing:** OpenCV, Pillow
- **Utilities:** NumPy

---

## Project Structure

```
ai-traffic-sign-recognition/
├── app.py
├── requirements.txt
├── models/
└── src/
    ├── constants.py
    ├── gradcam.py
    ├── image_utils.py
    ├── model_utils.py
    ├── slideshow.py
    └── ui_components.py
```

---

## Grad-CAM Explainability

Grad-CAM (Gradient-weighted Class Activation Mapping) generates a heatmap by computing the gradient of the predicted class score with respect to the final convolutional layer's feature maps. This makes the model's decision process interpretable — useful for validating that the network is focusing on the sign itself rather than background noise.

---

## Screenshots

### Homepage
<p align="center">
  <img src="assets/screenshots/home.png" width="900"/>
</p>

### Prediction Dashboard
<p align="center">
  <img src="assets/screenshots/home2.png" width="900"/>
</p>

### Prediction Output
<p align="center">
  <img src="assets/screenshots/prediction.png" width="450"/>
</p>

### Grad-CAM Heatmap
<p align="center">
  <img src="assets/screenshots/maps.png" width="450"/>
</p>

---

## Author

Agasthyan S &nbsp;·&nbsp; [LinkedIn](https://linkedin.com/in/agasthyan) &nbsp;·&nbsp; [GitHub](https://github.com/agstyn)