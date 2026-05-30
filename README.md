# KaryoScan — Chromosomal Abnormality Detection

A Streamlit application for detecting and classifying chromosomal abnormalities
from karyotype images using YOLO26 and Dynamic Time Warping.

## Model

- **Architecture**: YOLO26
- **Classes**: 24 karyotype groups (A1-A3, B4-B5, C6-C12, D13-D15, E16-E18, F19-F20, G21-G22, X, Y)

## Project Structure

```
.
├── app.py                    # Main entry point (multi-page router)
├── pages/
│   ├── __init__.py
│   ├── home.py               # Page 1 — Home
│   ├── how_it_works.py       # Page 2 — How It Works
│   ├── model_performance.py  # Page 3 — Model Performance
│   └── detect.py             # Page 4 — Let's Detect
├── classifier.py             # ChromosomeClassifier
├── dtw_similarity.py         # ChromosomeDTW
├── best.pt                   # ← Place your trained YOLO weights here
├── requirements.txt
└── assets/
    ├── train/                # ← Place training curve images here
    │   ├── results.png
    │   ├── confusion_matrix.png
    │   ├── PR_curve.png
    │   └── F1_curve.png
    ├── val/                  # ← Place validation batch images here
    │   ├── val_batch0_labels.jpg
    │   └── val_batch0_pred.jpg
    └── showcase/             # ← Place showcase images here
        ├── original.jpg
        ├── detected.jpg
        └── classification_table.png   (optional)
```

## Setup

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```
