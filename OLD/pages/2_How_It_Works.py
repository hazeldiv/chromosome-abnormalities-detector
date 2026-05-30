import streamlit as st

st.title("How It Works")
st.markdown("---")

st.header("YOLO26 Model")
st.write("The application uses a YOLO26 model trained on chromosome images. This is a object detection architecture optimized for accuracy and speed.")

st.subheader("24-Class Karyotype Classification")
st.write("The model classifies chromosomes into 24 categories based on standard karyotype groups:")

classes = [
    ("A1, A2, A3", "Chromosome group 1 (largest)"),
    ("B4, B5", "Chromosome group 2 (large)"),
    ("C6-C12", "Chromosome group 3 (medium-large, includes sex chromosomes)"),
    ("D13-D15", "Chromosome group 4 (medium, acrocentric)"),
    ("E16-E18", "Chromosome group 5 (medium-small)"),
    ("F19, F20", "Chromosome group 6 (small)"),
    ("G21, G22", "Chromosome group 7 (smallest, acrocentric)"),
    ("X, Y", "Sex chromosomes"),
]

for group, description in classes:
    st.markdown(f"- **{group}**: {description}")

st.subheader("Detection Workflow")
st.write("1. **Upload Image**: User uploads a chromosome microscopy image")
st.write("2. **Preprocessing**: Image is resized to 640x640 pixels")
st.write("3. **Inference**: YOLO26 model performs object detection")
st.write("4. **Post-processing**: Bounding boxes and class labels are generated")
st.write("5. **Results Display**: Detections shown with confidence scores")

st.header("Limitations")
st.info("- Model accuracy depends on image quality and resolution")
st.info("- Best results with G-banded chromosome images")
st.info("- Detection confidence threshold can be adjusted")