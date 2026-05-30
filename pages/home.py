import streamlit as st


def render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM):

    # Hero
    st.markdown(f"""
    <div style='padding:2.5rem 0 1.5rem 0;'>
        <div style='font-size:0.78rem;letter-spacing:0.18em;text-transform:uppercase;
                    color:{CLR_GREEN};font-family:Space Mono,monospace;margin-bottom:0.75rem;'>
            ● AI-Powered Karyotype Analysis
        </div>
        <div class='grad-title'>KaryoScan</div>
        <div style='font-family:Space Mono,monospace;font-size:1.35rem;
                    color:{CLR_TEXT_MUTED};margin-top:0.25rem;'>
            Chromosomal Abnormality Detection
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='max-width:700px;font-size:1.05rem;color:{CLR_TEXT_MUTED};
                line-height:1.75;margin-bottom:2rem;'>
        KaryoScan is a deep-learning system that automatically detects, classifies,
        and flags potential chromosomal abnormalities from karyotype images.
        It combines an object-detection backbone with a structural-similarity engine
        to produce clinician-ready reports, reducing manual review time and helping
        cytogeneticists focus their attention where it matters most.
    </div>
    """, unsafe_allow_html=True)

    # Stat row
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("24", "Chromosome Classes"),
        ("YOLO26", "Detection Model"),
        ("DTW", "Similarity Engine"),
        ("Denver", "Classification System"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-num'>{val}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # Two-column info cards
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(f"""
        <div class='kcard'>
            <div style='font-family:Space Mono,monospace;font-size:1rem;
                        color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
                🧬 What are Chromosomal Abnormalities?
            </div>
            <div style='color:{CLR_TEXT_MUTED};font-size:0.9rem;line-height:1.7;'>
                Chromosomal abnormalities are deviations from the normal human karyotype
                of 46 chromosomes arranged in 23 pairs. They are broadly divided into
                <b style='color:{CLR_TEXT};'>numerical abnormalities</b>
                (e.g., trisomies, monosomies) and
                <b style='color:{CLR_TEXT};'>structural abnormalities</b>
                (e.g., deletions, duplications, translocations, inversions).
                <br><br>
                These anomalies are associated with a wide range of genetic disorders
                including Down syndrome (trisomy 21), Turner syndrome (45,X), and
                various cancers detectable via cytogenetic analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='kcard'>
            <div style='font-family:Space Mono,monospace;font-size:1rem;
                        color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
                🔬 What is Karyotyping?
            </div>
            <div style='color:{CLR_TEXT_MUTED};font-size:0.9rem;line-height:1.7;'>
                Karyotyping is a cytogenetic technique that produces a standardised image
                of an individual's complete set of chromosomes, sorted by size and banding
                pattern. G-banding (Giemsa staining) is the most common method, revealing
                characteristic dark and light bands unique to each chromosome pair,
                making it possible to identify structural rearrangements with high specificity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class='kcard'>
            <div style='font-family:Space Mono,monospace;font-size:1rem;
                        color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
                ⚡ How KaryoScan Helps
            </div>
            <div style='color:{CLR_TEXT_MUTED};font-size:0.9rem;line-height:1.7;'>
                Traditional karyotype analysis is labour-intensive, requiring trained
                cytogeneticists to manually count and evaluate each chromosome pair.
                KaryoScan automates the initial screening step by:
            </div>
            <ul style='color:{CLR_TEXT_MUTED};font-size:0.9rem;line-height:2;
                        margin-top:0.75rem;padding-left:1.2rem;'>
                <li>Detecting all chromosomes in the karyogram using YOLO26</li>
                <li>Assigning each detection to one of 24 chromosome classes</li>
                <li>Verifying pair structural similarity via Dynamic Time Warping</li>
                <li>Flagging numerical and structural anomalies for expert review</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='kcard'>
            <div style='font-family:Space Mono,monospace;font-size:1rem;
                        color:{CLR_PURPLE_LIGHT};margin-bottom:0.75rem;'>
                ⚠️ Clinical Disclaimer
            </div>
            <div style='color:{CLR_TEXT_MUTED};font-size:0.88rem;line-height:1.7;'>
                KaryoScan is a <b style='color:{CLR_TEXT};'>research and screening tool</b>
                and is <b style='color:{CLR_TEXT};'>not a substitute</b> for professional
                cytogenetic analysis. All results flagged as ambiguous must be reviewed
                and confirmed by a qualified cytogeneticist before any clinical decision
                is made. The authors accept no liability for diagnostic outcomes derived
                solely from this tool.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='kdivider'/>", unsafe_allow_html=True)

    # Quick-start CTA
    st.markdown(f"""
    <div style='text-align:center;padding:1rem 0 0.5rem 0;'>
        <div style='font-family:Space Mono,monospace;font-size:1.1rem;
                    color:{CLR_TEXT};margin-bottom:0.5rem;'>
            Ready to analyse a karyotype?
        </div>
        <div style='color:{CLR_TEXT_MUTED};font-size:0.9rem;'>
            Navigate to <b style='color:{CLR_GREEN_LIGHT};'>🔬 Let's Detect</b>
            in the sidebar to upload an image and run the pipeline.
        </div>
    </div>
    """, unsafe_allow_html=True)
