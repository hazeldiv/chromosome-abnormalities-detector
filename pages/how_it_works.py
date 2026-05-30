import streamlit as st
import pandas as pd


def render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM):

    st.markdown(f"""
    <div style='padding:2rem 0 1.5rem 0;'>
        <div style='font-size:0.75rem;letter-spacing:0.18em;text-transform:uppercase;
                    color:{CLR_GREEN};font-family:Space Mono,monospace;margin-bottom:0.5rem;'>
            Methodology
        </div>
        <div class='grad-title-sm'>How It Works</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Section 1: Denver Classification ─────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:1rem;
                color:{CLR_PURPLE_LIGHT};margin:1.5rem 0 0.75rem 0;'>
        01 - Denver Classification System
    </div>
    <div style='color:{CLR_TEXT_MUTED};font-size:0.92rem;line-height:1.75;max-width:760px;
                margin-bottom:1.25rem;'>
        The Denver system organises human autosomes into seven groups (A-G)
        based on size and centromere position, supplemented by the sex chromosomes X and Y.
        Each chromosome pair is assigned a standardised numeric or alphanumeric label
        that allows cytogeneticists worldwide to communicate findings unambiguously.
    </div>
    """, unsafe_allow_html=True)

    # Chromosome annotation table — placeholder rows for user to fill
    CHROMOSOME_ANNOTATIONS = [
        ("A", "A1, A2, A3", "Chromosome group 1 (largest)"),
        ("B", "B4, B5", "Chromosome group 2 (large)"),
        ("C", "C6-C12", "Chromosome group 3 (medium-large, includes sex chromosomes)"),
        ("D", "D13-D15", "Chromosome group 4 (medium, acrocentric)"),
        ("E", "E16-E18", "Chromosome group 5 (medium-small)"),
        ("F", "F19, F20", "Chromosome group 6 (small)"),
        ("G", "G21, G22", "Chromosome group 7 (smallest, acrocentric)"),
        ("Sex", "X, Y", "Sex chromosomes"),
    ]

    # Build all rows using flexbox divs (Streamlit strips <table>/<tr>/<td> tags)
    df_annotations = pd.DataFrame(
        CHROMOSOME_ANNOTATIONS,
        columns=[
            "Group",
            "Chromosomes",
            "Description / Annotation"
        ]
    )

    # Build styled HTML table matching the detect.py results table style
    _th = f'padding:0.6rem 0.75rem;font-family:Space Mono,monospace;color:{CLR_GREEN_LIGHT};'
    table_html = (
        '<table style="width:100%;border-collapse:collapse;font-size:0.86rem;">'
        '<thead>'
        f'<tr style="background:{CLR_SURFACE2};border-bottom:2px solid {CLR_BORDER};">'
        f'<th style="{_th}text-align:left;">Group</th>'
        f'<th style="{_th}text-align:left;">Chromosomes</th>'
        f'<th style="{_th}text-align:left;">Description / Annotation</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
    )

    for i, (group, chroms, desc) in enumerate(CHROMOSOME_ANNOTATIONS):
        bg = CLR_SURFACE2 if i % 2 == 0 else "transparent"
        td_base = "padding:0.55rem 0.75rem;"
        row = (
            '<tr style="background:{bg};border-bottom:1px solid {border};">'
            '<td style="' + td_base + 'font-family:Space Mono,monospace;'
            'color:{green};font-weight:600;">{group}</td>'
            '<td style="' + td_base + 'font-family:Space Mono,monospace;'
            'color:{text};">{chroms}</td>'
            '<td style="' + td_base + 'color:{muted};font-size:0.84rem;">{desc}</td>'
            '</tr>'
        ).format(
            bg=bg, border=CLR_BORDER, green=CLR_GREEN_LIGHT,
            text=CLR_TEXT, muted=CLR_TEXT_MUTED,
            group=group, chroms=chroms, desc=desc,
        )
        table_html += row

    table_html += "</tbody></table>"

    st.markdown(
        "<div style='font-family:Space Mono,monospace;font-size:0.78rem;"
        f"color:{CLR_TEXT_MUTED};letter-spacing:0.08em;margin-bottom:0.75rem;'>"
        "CHROMOSOME GROUP ANNOTATIONS - DENVER SYSTEM</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='kcard' style='padding:0;overflow:hidden;'>" + table_html + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # ── Section 2: Pipeline ───────────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:1rem;
                color:{CLR_PURPLE_LIGHT};margin:0.5rem 0 1.25rem 0;'>
        02 - Detection & Classification Pipeline
    </div>
    """, unsafe_allow_html=True)

    STEPS = [
        ("Image Ingestion",
         "A karyotype image (JPG / PNG / BMP) is loaded and passed to the inference pipeline. "
         "No preprocessing beyond YOLO's built-in letterboxing is required."),
        ("YOLO Object Detection",
         "A fine-tuned YOLO26 model (best.pt, trained on 24 chromosome classes following "
         "the Denver naming scheme) runs inference at a user-specified confidence threshold. "
         "Each detection returns a bounding box, class ID, and confidence score."),
        ("Crop Extraction",
         "For every detected bounding box, a padded crop of the chromosome is extracted "
         "from the source image using extract_crop() (detection.py). These crops are "
         "stored alongside their class IDs in a grouped detections dictionary."),
        ("Numerical Rule Check (Autosomes)",
         "The ChromosomeClassifier (classifier.py) first checks the count for each "
         "autosome class: 0 detected = missing, 1 = monosomy flag, >2 = trisomy/polysomy flag. "
         "Any deviation immediately marks the chromosome as ambiguous."),
        ("DTW Structural Similarity (Autosomes with count == 2)",
         "For pairs with exactly two detected chromosomes, the ChromosomeDTW engine "
         "(dtw_similarity.py) extracts a 64-point medial-axis density profile from each crop "
         "via skeletonisation, then computes a normalised DTW similarity score. "
         "Pairs below the similarity threshold are flagged as structurally ambiguous."),
        ("Sex Chromosome Evaluation",
         "X and Y counts are evaluated jointly. Configurations 46,XY (1X + 1Y) and "
         "46,XX (2X + 0Y) are considered normal; all other combinations are flagged."),
        ("Result Aggregation & Report",
         "Classifications are aggregated into normal and ambiguous lists. "
         "The output includes counts, DTW scores, and human-readable descriptions "
         "for each ambiguous finding, ready for cytogeneticist review."),
    ]

    for i, (title, desc) in enumerate(STEPS, 1):
        st.markdown(f"""
        <div class='step-row'>
            <div class='step-num'>{i:02d}</div>
            <div class='step-body'>
                <div class='step-title'>{title}</div>
                <div class='step-desc'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # ── Section 3: Limitations ────────────────────────────────────────────────
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace;font-size:1rem;
                color:{CLR_PURPLE_LIGHT};margin:0.5rem 0 1.25rem 0;'>
        03 - Known Limitations
    </div>
    """, unsafe_allow_html=True)

    LIMITATIONS = [
        ("📷", "Image Quality Dependency",
         "Model accuracy is directly tied to image quality and resolution. "
         "Low-contrast, blurry, or poorly-stained karyograms will reduce detection reliability."),
        ("🔬", "G-Banding Assumption",
         "Results are optimal when the input image contains G-banded (Giemsa-stained) chromosomes. "
         "Other staining techniques may produce unreliable banding profiles and degrade similarity scoring."),
        ("🔗", "Overlapping Chromosome Sensitivity",
         "Normal/ambiguous classification success depends on the model's ability to isolate "
         "individual chromosomes. Overlapping or clustered chromosomes may be missed or "
         "merged into a single detection, invalidating the pair-count logic."),
        ("📉", "Unverifiable Classification Accuracy",
         "The accuracy of the normal/ambiguous classification step cannot be quantitatively "
         "evaluated due to the absence of a labelled ground-truth dataset containing verified "
         "normal/abnormal annotations at the individual chromosome level."),
    ]

    for icon, title, text in LIMITATIONS:
        st.markdown(f"""
        <div class='limit-item'>
            <div class='limit-icon'>{icon}</div>
            <div>
                <div style='font-size:0.88rem;font-weight:600;color:{CLR_TEXT};
                            margin-bottom:2px;'>{title}</div>
                <div class='limit-text'>{text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)