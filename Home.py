import streamlit as st

st.set_page_config(
    page_title="Chromosome Abnormality Detector",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Navigation")
st.sidebar.info("Use the pages above to navigate through the app.")

st.title("Chromosome Abnormality Detector")
st.markdown("---")
st.header("Welcome to the Chromosome Abnormality Detection App")
st.write("This application uses a deep learning model (YOLOv8) to detect and classify chromosomes from microscope images.")
st.write("It can identify 24 different chromosome types based on the standard karyotype classification system.")

st.markdown("### Quick Links")
col1, col2 = st.columns(2)
with col1:
    if st.button("How It Works", use_container_width=True):
        st.switch_page("pages/2_How_It_Works.py")
with col2:
    if st.button("Start Detection", use_container_width=True):
        st.switch_page("pages/3_Detection.py")

st.markdown("---")
st.caption("Upload a chromosome image to detect abnormalities and classify chromosome types.")