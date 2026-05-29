# Chromosome Abnormality Detector

A Streamlit application that detects and classifies chromosomes from microscope images using YOLOv8.

## Model

- **Architecture**: YOLOv8 Nano (yolo26n)
- **Classes**: 24 karyotype groups (A1-A3, B4-B5, C6-C12, D13-D15, E16-E18, F19-F20, G21-G22, X, Y)

## Installation

```bash
# Clone and setup
uv venv --python 3.12
uv pip install -r requirements.txt

# Run the app
streamlit run Home.py
```

## Pages

- **Home**: Welcome page with quick navigation
- **How It Works**: Explanation of the detection model and workflow
- **Detection**: Upload images to detect and classify chromosomes
