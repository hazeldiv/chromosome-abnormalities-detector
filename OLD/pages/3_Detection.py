import streamlit as st
import os
from ultralytics import YOLO
from PIL import Image
import io

st.title("Chromosome Detection")
st.markdown("---")

CLASSES = [
    "A1", "A2", "A3", "B4", "B5", "C10", "C11", "C12", "C6", "C7", "C8", "C9",
    "D13", "D14", "D15", "E16", "E17", "E18", "F19", "F20", "G21", "G22", "X", "Y"
]

@st.cache_resource
def load_model():
    return YOLO("model.pt")

model = load_model()

st.subheader("Upload Chromosome Image")
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png", "bmp"],
    help="Supported formats: JPG, PNG, BMP"
)

conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(uploaded_file, use_container_width=True)

    if st.button("Detect Chromosomes", type="primary"):
        with st.spinner("Running detection..."):
            image = Image.open(uploaded_file)
            results = model.predict(image, conf=conf_threshold, save=False)

            result = results[0]
            annotated_img = result.plot()

            with col2:
                st.subheader("Detection Results")
                st.image(annotated_img, channels="BGR", use_container_width=True)

            st.subheader("Detection Details")
            detections = []
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = CLASSES[cls_id] if cls_id < len(CLASSES) else f"Class_{cls_id}"

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append({
                    "Class": class_name,
                    "Confidence": f"{conf:.2%}",
                    "BBox": f"[{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]"
                })

            if detections:
                st.dataframe(detections, use_container_width=True)
                st.success(f"Detected {len(detections)} chromosome(s)")
            else:
                st.warning("No chromosomes detected. Try lowering the confidence threshold.")

st.markdown("---")
st.caption("For best results, use high-quality G-banded chromosome images.")