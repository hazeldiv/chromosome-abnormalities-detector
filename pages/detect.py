import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io


CHROMOSOME_NAMES = {
    0: 'A1',  1: 'A2',  2: 'A3',  3: 'B4',  4: 'B5',
    5: 'C10', 6: 'C11', 7: 'C12', 8: 'C6',  9: 'C7',
   10: 'C8', 11: 'C9', 12: 'D13', 13: 'D14', 14: 'D15',
   15: 'E16', 16: 'E17', 17: 'E18', 18: 'F19', 19: 'F20',
   20: 'G21', 21: 'G22', 22: 'X',  23: 'Y'
}

MAX_UPLOAD_MB = 200
ALLOWED_TYPES = ["jpg", "jpeg", "png", "bmp"]


def _pil_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)


def _cv2_to_pil(cv2_img):
    return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))


def _run_detection(image_cv2, model, conf_threshold, dtw_threshold):
    from dtw_similarity import ChromosomeDTW
    from classifier import ChromosomeClassifier

    dtw_engine = ChromosomeDTW(threshold=dtw_threshold)
    classifier = ChromosomeClassifier(dtw_engine)

    predictions = model.predict(image_cv2, conf=conf_threshold, verbose=False)

    # Draw bounding boxes on a copy
    annotated = image_cv2.copy()
    detections = {}

    if predictions and predictions[0].boxes is not None:
        boxes   = predictions[0].boxes.xyxy.cpu().numpy()
        classes = predictions[0].boxes.cls.cpu().numpy()
        confs   = predictions[0].boxes.conf.cpu().numpy()

        for box, cls, conf in zip(boxes, classes, confs):
            cls_id = int(cls)
            x1, y1, x2, y2 = map(int, box)
            name = CHROMOSOME_NAMES.get(cls_id, f"cls_{cls_id}")

            # Crop
            pad = 5
            h, w = image_cv2.shape[:2]
            cx1 = max(0, x1 - pad); cy1 = max(0, y1 - pad)
            cx2 = min(w, x2 + pad); cy2 = min(h, y2 + pad)
            crop = image_cv2[cy1:cy2, cx1:cx2]

            if cls_id not in detections:
                detections[cls_id] = []
            detections[cls_id].append({"box": box.tolist(), "image": crop})

            # Draw box + label
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (124, 58, 237), 2)
            label = f"{name} {conf:.2f}"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            cv2.rectangle(annotated, (x1, y1 - lh - 6), (x1 + lw + 4, y1), (124, 58, 237), -1)
            cv2.putText(annotated, label, (x1 + 2, y1 - 3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    classification = classifier.classify(detections)
    return annotated, detections, classification


def render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM):

    st.markdown(f"""
    <div style='padding:2rem 0 1.5rem 0;'>
        <div style='font-size:0.75rem;letter-spacing:0.18em;text-transform:uppercase;
                    color:{CLR_GREEN};font-family:Space Mono,monospace;margin-bottom:0.5rem;'>
            Inference
        </div>
        <div class='grad-title-sm'>Let's Detect</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Slider controls ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:0.9rem;
                color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
        01 - Detection Parameters
    </div>
    """, unsafe_allow_html=True)

    s_col1, s_col2, _ = st.columns([1, 1, 1])
    with s_col1:
        conf_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.05, max_value=0.95, value=0.25, step=0.05,
            help="Minimum YOLO confidence score to accept a detection."
        )
    with s_col2:
        dtw_threshold = st.slider(
            "DTW Similarity Threshold",
            min_value=0.50, max_value=1.00, value=0.85, step=0.05,
            help="Minimum DTW similarity for a chromosome pair to be classified as normal."
        )

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # ── File upload ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:0.9rem;
                color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
        02 - Upload Karyotype Image
    </div>
    <div style='color:{CLR_TEXT_MUTED};font-size:0.85rem;margin-bottom:1rem;'>
        Accepted formats: <b>JPG · JPEG · PNG · BMP</b> &nbsp;|&nbsp;
        Max size: <b>200 MB</b>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        label="Upload karyotype image",
        type=ALLOWED_TYPES,
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    if uploaded is not None:
        file_mb = uploaded.size / (1024 * 1024)
        if file_mb > MAX_UPLOAD_MB:
            st.error(f"File exceeds the {MAX_UPLOAD_MB} MB limit ({file_mb:.1f} MB).")
            return

        pil_image = Image.open(uploaded)
        image_cv2 = _pil_to_cv2(pil_image)

        st.markdown(f"""
        <div style='background:{CLR_GREEN_DIM};border:1px solid {CLR_GREEN};
                    border-radius:8px;padding:0.6rem 1rem;margin:0.75rem 0;
                    font-size:0.88rem;color:{CLR_GREEN_LIGHT};'>
            ✓ &nbsp;<b>{uploaded.name}</b> uploaded successfully
            &nbsp;·&nbsp; {pil_image.width}×{pil_image.height} px
            &nbsp;·&nbsp; {file_mb:.2f} MB
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

        # ── Detect button ─────────────────────────────────────────────────────
        detect_clicked = st.button(
            "🔬  Run Detection",
            type="primary",
            use_container_width=False,
        )

        if detect_clicked:
            # ── Load model ────────────────────────────────────────────────────
            try:
                from ultralytics import YOLO
                if "yolo_model" not in st.session_state:
                    with st.spinner("Loading model weights (best.pt)…"):
                        st.session_state["yolo_model"] = YOLO("best.pt")
                model = st.session_state["yolo_model"]
            except Exception as e:
                st.error(f"Could not load YOLO model: {e}\n\nEnsure `best.pt` is in the working directory.")
                return

            # ── Run inference ─────────────────────────────────────────────────
            with st.spinner("Running YOLO detection + DTW classification…"):
                try:
                    annotated_cv2, detections, classification = _run_detection(
                        image_cv2, model, conf_threshold, dtw_threshold
                    )
                except Exception as e:
                    st.error(f"Detection failed: {e}")
                    return

            st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='font-family:Space Mono,monospace;font-size:0.9rem;
                        color:{CLR_PURPLE_LIGHT};margin-bottom:1rem;'>
                03 - Results
            </div>
            """, unsafe_allow_html=True)

            # ── Image comparison ──────────────────────────────────────────────
            img_col1, img_col2 = st.columns(2, gap="large")
            with img_col1:
                st.markdown(f"<div class='muted mono' style='margin-bottom:0.4rem;'>ORIGINAL IMAGE</div>",
                            unsafe_allow_html=True)
                st.image(pil_image, use_container_width=True)

            with img_col2:
                st.markdown(f"<div class='muted mono' style='margin-bottom:0.4rem;'>DETECTION OUTPUT</div>",
                            unsafe_allow_html=True)
                st.image(_cv2_to_pil(annotated_cv2), use_container_width=True)

            st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

            # ── Summary stats ─────────────────────────────────────────────────
            total_detected   = sum(len(v) for v in detections.values())
            normal_count     = len(classification["normal"])
            ambiguous_count  = len(classification["ambiguous"])

            sc1, sc2, sc3 = st.columns(3)
            for col, val, label in zip(
                [sc1, sc2, sc3],
                [total_detected, normal_count, ambiguous_count],
                ["Total Chromosomes Detected", "Normal Classes", "Ambiguous Classes"]
            ):
                with col:
                    colour = CLR_GREEN_LIGHT if label != "Ambiguous Classes" else CLR_PURPLE_LIGHT
                    st.markdown(f"""
                    <div class='stat-box'>
                        <div class='stat-num' style='color:{colour};'>{val}</div>
                        <div class='stat-label'>{label}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

            # ── Full results table ────────────────────────────────────────────
            st.markdown(f"""
            <div style='font-family:Space Mono,monospace;font-size:0.78rem;
                        color:{CLR_TEXT_MUTED};letter-spacing:0.08em;margin-bottom:0.75rem;'>
                DETAILED RESULTS TABLE
            </div>
            """, unsafe_allow_html=True)

            all_results = (
                [(r, "normal")   for r in classification["normal"]] +
                [(r, "ambiguous") for r in classification["ambiguous"]]
            )
            all_results.sort(key=lambda x: x[0]["class_id"])

            header_bg  = CLR_SURFACE2
            header_col = CLR_GREEN_LIGHT

            _th = f'padding:0.6rem 0.75rem;font-family:Space Mono,monospace;color:{header_col};'
            table_html = (
                '<table style="width:100%;border-collapse:collapse;font-size:0.86rem;">'
                '<thead>'
                f'<tr style="background:{header_bg};border-bottom:2px solid {CLR_BORDER};">'
                f'<th style="{_th}text-align:left;">Name</th>'
                f'<th style="{_th}text-align:center;">Class ID</th>'
                f'<th style="{_th}text-align:center;">Count</th>'
                f'<th style="{_th}text-align:center;">Status</th>'
                f'<th style="{_th}text-align:left;">DTW Score</th>'
                f'<th style="{_th}text-align:left;">Description</th>'
                '</tr>'
                '</thead>'
                '<tbody>'
            )

            for i, (item, cat) in enumerate(all_results):
                bg = CLR_SURFACE2 if i % 2 == 0 else "transparent"

                # Pre-extract values to avoid dict-key single-quote conflicts inside f-strings
                item_name     = item["name"]
                item_class_id = item["class_id"]
                item_count    = item["count"]

                if cat == "normal":
                    badge = '<span class="pill-normal">\u2713 Normal</span>'
                    desc  = "\u2014"
                else:
                    badge = '<span class="pill-ambig">\u26a0 Ambiguous</span>'
                    desc  = item.get("description", item.get("reason", "\u2014"))

                dtw_val = item.get("dtw_similarity")
                dtw_str = f"{dtw_val:.4f}" if dtw_val is not None else "\u2014"

                # Sex chromosomes: show X/Y counts instead
                if item_class_id in [22, 23]:
                    x_c = item.get("x_count", "?")
                    y_c = item.get("y_count", "?")
                    dtw_str = f"X={x_c} Y={y_c}"

                row = (
                    "<tr style=\"background:{bg};border-bottom:1px solid {border};\">"
                    "<td style=\"padding:0.55rem 0.75rem;font-family:Space Mono,monospace;"
                    "color:{text};font-weight:600;\">{name}</td>"
                    "<td style=\"padding:0.55rem 0.75rem;text-align:center;"
                    "color:{muted};\">{cls_id}</td>"
                    "<td style=\"padding:0.55rem 0.75rem;text-align:center;"
                    "color:{text};\">{count}</td>"
                    "<td style=\"padding:0.55rem 0.75rem;text-align:center;\">{badge}</td>"
                    "<td style=\"padding:0.55rem 0.75rem;color:{muted};"
                    "font-family:Space Mono,monospace;font-size:0.82rem;\">{dtw}</td>"
                    "<td style=\"padding:0.55rem 0.75rem;color:{muted};"
                    "font-size:0.84rem;\">{desc}</td>"
                    "</tr>"
                ).format(
                    bg=bg, border=CLR_BORDER, text=CLR_TEXT, muted=CLR_TEXT_MUTED,
                    name=item_name, cls_id=item_class_id, count=item_count,
                    badge=badge, dtw=dtw_str, desc=desc,
                )
                table_html += row

            table_html += "</tbody></table>"
            st.markdown("<div class='kcard' style='padding:0;overflow:hidden;'>" + table_html + "</div>",
                        unsafe_allow_html=True)

            st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

            # ── Categorised detail cards ──────────────────────────────────────
            det_col1, det_col2 = st.columns(2, gap="large")

            with det_col1:
                st.markdown(f"""
                <div style='font-family:Space Mono,monospace;font-size:0.85rem;
                            color:{CLR_GREEN_LIGHT};margin-bottom:0.75rem;'>
                    ✓ Normal &nbsp;({len(classification['normal'])} types)
                </div>
                """, unsafe_allow_html=True)

                if classification["normal"]:
                    for item in classification["normal"]:
                        dtw_disp = (f"DTW: {item['dtw_similarity']:.4f}"
                                    if "dtw_similarity" in item
                                    else f"X={item.get('x_count','?')} Y={item.get('y_count','?')}")
                        st.markdown(f"""
                        <div style='display:flex;justify-content:space-between;align-items:center;
                                    background:{CLR_GREEN_DIM};border:1px solid {CLR_GREEN};
                                    border-radius:8px;padding:0.5rem 0.9rem;margin-bottom:0.5rem;'>
                            <span style='font-family:Space Mono,monospace;font-weight:700;
                                         color:{CLR_GREEN_LIGHT};font-size:0.9rem;'>{item['name']}</span>
                            <span style='font-size:0.78rem;color:{CLR_GREEN};
                                         font-family:Space Mono,monospace;'>
                                {item['count']} detected &nbsp;·&nbsp; {dtw_disp}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='muted'>No normal chromosomes detected.</div>",
                                unsafe_allow_html=True)

            with det_col2:
                st.markdown(f"""
                <div style='font-family:Space Mono,monospace;font-size:0.85rem;
                            color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
                    ⚠ Ambiguous &nbsp;({len(classification['ambiguous'])} types)
                </div>
                """, unsafe_allow_html=True)

                if classification["ambiguous"]:
                    for item in classification["ambiguous"]:
                        desc = item.get("description", item.get("reason", "See description"))
                        st.markdown(f"""
                        <div style='background:{CLR_PURPLE_DIM};border:1px solid {CLR_PURPLE};
                                    border-radius:8px;padding:0.5rem 0.9rem;margin-bottom:0.5rem;'>
                            <div style='display:flex;justify-content:space-between;
                                        align-items:center;'>
                                <span style='font-family:Space Mono,monospace;font-weight:700;
                                             color:{CLR_PURPLE_LIGHT};font-size:0.9rem;'>
                                    {item['name']}
                                </span>
                                <span style='font-size:0.78rem;color:{CLR_PURPLE_LIGHT};
                                             font-family:Space Mono,monospace;'>
                                    {item['count']} detected
                                </span>
                            </div>
                            <div style='font-size:0.82rem;color:{CLR_TEXT_MUTED};
                                        margin-top:0.25rem;'>{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='muted'>No ambiguous chromosomes flagged.</div>",
                                unsafe_allow_html=True)

            # ── Download annotated image ──────────────────────────────────────
            st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)
            buf = io.BytesIO()
            _cv2_to_pil(annotated_cv2).save(buf, format="PNG")
            st.download_button(
                label="⬇️  Download Annotated Image",
                data=buf.getvalue(),
                file_name=f"karyoscan_{uploaded.name.rsplit('.',1)[0]}.png",
                mime="image/png",
            )