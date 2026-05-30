import streamlit as st
import os
from pathlib import Path


# ── Helper: display an image if the path exists, else show a placeholder ──────
def _img_or_placeholder(path, caption, CLR_SURFACE2, CLR_BORDER, CLR_TEXT_MUTED, CLR_PURPLE_LIGHT):
    if path and os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.markdown(f"""
        <div style='background:{CLR_SURFACE2};border:1px dashed {CLR_BORDER};
                    border-radius:10px;padding:2.5rem 1rem;text-align:center;
                    color:{CLR_TEXT_MUTED};font-size:0.85rem;margin-bottom:0.5rem;'>
            <div style='font-size:1.5rem;margin-bottom:0.4rem;'>🖼️</div>
            <div style='color:{CLR_PURPLE_LIGHT};font-family:Space Mono,monospace;
                        font-size:0.78rem;margin-bottom:0.3rem;'>{caption}</div>
            Place the image file at:<br>
            <code style='font-size:0.75rem;color:{CLR_TEXT_MUTED};'>{path or "(path not set)"}</code>
        </div>
        """, unsafe_allow_html=True)


def render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM):

    st.markdown(f"""
    <div style='padding:2rem 0 1.5rem 0;'>
        <div style='font-size:0.75rem;letter-spacing:0.18em;text-transform:uppercase;
                    color:{CLR_GREEN};font-family:Space Mono,monospace;margin-bottom:0.5rem;'>
            Evaluation
        </div>
        <div class='grad-title-sm'>Model Performance</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Test-set metric cards ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:0.9rem;
                color:{CLR_PURPLE_LIGHT};margin-bottom:1rem;'>
        01 - Test-Set Metrics
    </div>
    """, unsafe_allow_html=True)

    # Editable metric placeholders — replace values with real results
    METRICS = {
        "mAP50-95": "0.8231",
        "mAP50":    "0.9912",
        "Precision": "0.9771",
        "Recall":    "0.9699",
    }

    cols = st.columns(len(METRICS))
    for col, (label, val) in zip(cols, METRICS.items()):
        with col:
            st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-num'>{val}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # ── Training visualisations ───────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:0.9rem;
                color:{CLR_PURPLE_LIGHT};margin-bottom:1rem;'>
        02 - Training & Validation Curves
    </div>
    """, unsafe_allow_html=True)

    TRAIN_IMAGES = [
        ("assets/train/confusion_matrix_normalized.png", "Confusion Matrix (Normalised)"),
        ("assets/train/confusion_matrix.png",            "Confusion Matrix"),
        ("assets/train/PR_curve.png",                    "Precision-Recall Curve"),
        ("assets/train/F1_curve.png",                    "F1-Confidence Curve"),
    ]

    col_a, col_b = st.columns(2, gap="large")
    for i, (path, caption) in enumerate(TRAIN_IMAGES):
        with (col_a if i % 2 == 0 else col_b):
            _img_or_placeholder(path, caption, CLR_SURFACE2, CLR_BORDER,
                                CLR_TEXT_MUTED, CLR_PURPLE_LIGHT)

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # ── Validation visualisations ─────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:0.9rem;
                color:{CLR_PURPLE_LIGHT};margin-bottom:1rem;'>
        03 - Validation Batch Predictions
    </div>
    """, unsafe_allow_html=True)

    VAL_IMAGES = [
        ("assets/val/val_batch0_labels.jpg",  "Validation Batch — Ground Truth Labels"),
        ("assets/val/val_batch0_pred.jpg",    "Validation Batch — Model Predictions"),
    ]

    col_c, col_d = st.columns(2, gap="large")
    for i, (path, caption) in enumerate(VAL_IMAGES):
        with (col_c if i % 2 == 0 else col_d):
            _img_or_placeholder(path, caption, CLR_SURFACE2, CLR_BORDER,
                                CLR_TEXT_MUTED, CLR_PURPLE_LIGHT)

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)
