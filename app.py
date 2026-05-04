"""
🌿 AI Leaf Disease Detector (Gemini)

A Streamlit application that uses Google Gemini Vision to detect
plant leaf diseases from uploaded photographs.

Run:
    streamlit run app.py
"""

import streamlit as st
from PIL import Image

from services.gemini_service import analyze_leaf, translate_json, ask_followup, GeminiServiceError
from utils.parser import parse_response
from utils import history_manager
from utils.config import check_api_configuration

# ──────────────────────────────────────────────
# API Configuration Check
# ──────────────────────────────────────────────
if not check_api_configuration():
    st.stop()
st.set_page_config(
    page_title="Leaf Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS – light clean theme
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* ── Global Text Enhancement ── */
    p, span, label, div { font-size: 1.05rem !important; letter-spacing: 0.3px; }
    h2, h3, h4, h5, h6 { margin-top: 1.2rem !important; margin-bottom: 0.6rem !important; }
    
    /* ── Sidebar Enhancement ── */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        font-size: 1.1rem !important; font-weight: 500;
    }

    /* ── Header ── */
    .app-header {
        text-align: center;
        padding: 1rem 0 0.5rem;
    }
    .app-header h1 {
        font-size: 2.5rem !important;
        font-weight: 800;
        color: #1B5E20;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
    }
    .app-header p {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0;
    }

    /* ── Result card ── */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .result-card h3 {
        margin: 0 0 0.4rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: #333;
    }
    .result-card ul {
        margin: 0;
        padding-left: 1.1rem;
    }
    .result-card li {
        margin-bottom: 0.15rem;
        color: #444;
        font-size: 0.85rem;
    }

    /* ── Small Cards for Details ── */
    .small-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 0.6rem;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .small-card h3 {
        margin: 0 0 0.4rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #333;
    }
    .small-card ul {
        margin: 0;
        padding-left: 1rem;
    }
    .small-card li {
        margin-bottom: 0.15rem;
        color: #444;
        font-size: 0.8rem;
    }
    .small-card p {
        font-size: 0.8rem;
        color: #666;
        margin: 0;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .badge-healthy {
        background: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #A5D6A7;
    }
    .badge-disease {
        background: #FFF3E0;
        color: #E65100;
        border: 1px solid #FFCC80;
    }

    /* ── Confidence bar label ── */
    .confidence-label {
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 0.2rem;
    }

    /* ── Divider ── */
    .section-divider {
        border: none;
        border-top: 1px solid #EEEEEE;
        margin: 0.8rem 0;
    }

    /* ── Upload area tweaks ── */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    /* ── Button styling ── */
    .stButton > button {
        background: #2E7D32;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: background 0.2s ease;
    }
    .stButton > button:hover {
        background: #1B5E20;
        color: white;
    }

    /* ── Limit Image Height ── */
    [data-testid="stImage"] img {
        max-height: 350px !important;
        object-fit: contain !important;
    }

    /* hide default Streamlit footer */
    footer {visibility: hidden;}

    /* reduce top padding */
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="app-header">
        <h1>🌿 Leaf Disease Detector</h1>
        <p>Upload a leaf photo to get instant diagnosis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Session State
# ──────────────────────────────────────────────
if "raw_response" not in st.session_state:
    st.session_state.raw_response = None
if "parsed_result" not in st.session_state:
    st.session_state.parsed_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_lang" not in st.session_state:
    st.session_state.current_lang = "English"

# ──────────────────────────────────────────────
# Two-column layout
# ──────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

# ==================== LEFT COLUMN ====================
with col_left:
    # ── Image input ──
    tab_upload, tab_camera = st.tabs(["📁 Upload", "📷 Camera"])

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Choose a leaf image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload a clear photo of a single plant leaf.",
        )

    with tab_camera:
        camera_image = st.camera_input("Take a photo of the leaf")

    # Resolve which image source to use
    image_source = uploaded_file or camera_image
    image: Image.Image | None = None

    if image_source is not None:
        try:
            image = Image.open(image_source)
        except Exception:
            st.error("⚠️ Could not open the image. Please upload a valid JPG or PNG file.")
            image = None

    # ── Preview ──
    if image is not None:
        st.image(image, caption="Uploaded Leaf", use_container_width=True)
        if st.button("🔬  Analyze Leaf", use_container_width=True):
            with st.spinner("🌿 Analyzing leaf…"):
                try:
                    raw = analyze_leaf(image)
                    st.session_state.raw_response = raw
                    parsed = parse_response(raw)
                    if parsed:
                        st.session_state.parsed_result = parsed
                        # Calculate severity score: high confidence + healthy = low severity, low confidence + diseased = high severity
                        conf_pct = parsed.get("confidence_pct", 50)
                        is_healthy = parsed.get("is_healthy", False)
                        severity = 0 if is_healthy else max(0, 100 - conf_pct)  # Inverted confidence for diseased plants
                        history_manager.save_record(parsed, severity_score=int(severity))
                    else:
                        st.warning("⚠️ Could not parse response as JSON.")
                        st.stop()
                    # Reset chat and language on new analysis
                    st.session_state.chat_history = []
                    st.session_state.current_lang = "English"
                except GeminiServiceError as err:
                    st.error(f"**API Error:** {err}")
                    st.info("💡 Please check your `GEMINI_API_KEY` and try again.")
                    st.stop()
    else:
        st.markdown(
            """
            <div style="text-align:center; padding:3rem 1rem; color:#999;
                        border:2px dashed #ddd; border-radius:12px; margin-top:0.5rem;">
                <p style="font-size:3rem; margin-bottom:0.5rem;">🍃</p>
                <p style="font-size:1rem;">Upload or capture a leaf image to get started</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==================== RIGHT COLUMN ====================
with col_right:
    if st.session_state.parsed_result is not None:
        result = st.session_state.parsed_result
        
        # ── Feature: Translate & Download ──
        col_act1, col_act2 = st.columns([1, 1])
        with col_act1:
            lang_options = ["English", "Hindi", "Marathi", "Spanish", "French"]
            idx = lang_options.index(st.session_state.current_lang) if st.session_state.current_lang in lang_options else 0
            new_lang = st.selectbox("🌐 Translate Results", lang_options, index=idx)
            
            if new_lang != st.session_state.current_lang:
                with st.spinner(f"Translating to {new_lang}..."):
                    if new_lang == "English":
                        st.session_state.parsed_result = parse_response(st.session_state.raw_response)
                    else:
                        trans_raw = translate_json(st.session_state.raw_response, new_lang)
                        parsed = parse_response(trans_raw)
                        if parsed:
                            st.session_state.parsed_result = parsed
                    st.session_state.current_lang = new_lang
                    st.rerun()

        with col_act2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            report_lines = [
                f"Disease: {result.get('disease_name', 'Unknown')}",
                f"Confidence: {result.get('confidence', 'N/A')}",
                "",
                "Symptoms:"
            ] + [f"- {s}" for s in result.get('symptoms', [])] + [
                "",
                "Treatment:"
            ] + [f"- {t}" for t in result.get('treatment', [])] + [
                "",
                "Prevention:"
            ] + [f"- {p}" for p in result.get('prevention', [])]
            
            st.download_button(
                "📥 Download Report",
                data="\n".join(report_lines),
                file_name="leaf_diagnosis.txt",
                mime="text/plain",
                use_container_width=True
            )

        # ──────────────────────────────────────
        # Display results
        # ──────────────────────────────────────
        st.markdown("### 📋 Analysis Results")

        # ── Disease name + badge ──
        is_healthy = result.get("is_healthy", False)
        disease_name = result.get("disease_name", "Unknown")

        if is_healthy:
            badge_html = f'<span class="badge badge-healthy">✅ {disease_name}</span>'
        else:
            badge_html = f'<span class="badge badge-disease">⚠️ {disease_name}</span>'

        st.markdown(
            f'<div class="result-card"><h3>Disease Detected</h3>{badge_html}</div>',
            unsafe_allow_html=True,
        )

        # ── Confidence ──
        conf_pct = result.get("confidence_pct", 0)
        conf_str = result.get("confidence", "N/A")

        st.progress(conf_pct / 100, text=f"Confidence: {conf_str}")

        # ── Details in Cards ──
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        col_sym, col_treat, col_prev = st.columns(3)

        with col_sym:
            symptoms = result.get("symptoms", [])
            if symptoms:
                items = "".join(f"<li>{s}</li>" for s in symptoms)
                st.markdown(f'<div class="small-card"><h3>🩺 Symptoms</h3><ul>{items}</ul></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="small-card"><h3>🩺 Symptoms</h3><p>None reported.</p></div>', unsafe_allow_html=True)

        with col_treat:
            treatment = result.get("treatment", [])
            if treatment:
                items = "".join(f"<li>{t}</li>" for t in treatment)
                st.markdown(f'<div class="small-card"><h3>💊 Treatment</h3><ul>{items}</ul></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="small-card"><h3>💊 Treatment</h3><p>None reported.</p></div>', unsafe_allow_html=True)

        with col_prev:
            prevention = result.get("prevention", [])
            if prevention:
                items = "".join(f"<li>{p}</li>" for p in prevention)
                st.markdown(f'<div class="small-card"><h3>🛡️ Prevention</h3><ul>{items}</ul></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="small-card"><h3>🛡️ Prevention</h3><p>None reported.</p></div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        st.caption("ℹ️ Does not replace professional agricultural advice.")
        
        # ── Feature: Follow-up Assistant ──
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("### 💬 Ask a Follow-up Question")
        
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])
            
        if prompt := st.chat_input("E.g., Can I use neem oil? Is this contagious?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_followup(disease_name, result, prompt)
                    st.write(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    elif image is not None:
        # Image uploaded but not yet analyzed
        st.markdown(
            """
            <div style="text-align:center; padding:3rem 1rem; color:#aaa;">
                <p style="font-size:2.5rem; margin-bottom:0.5rem;">🔬</p>
                <p style="font-size:1rem;">Click <strong>Analyze Leaf</strong> to get results</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # No image yet
        st.markdown(
            """
            <div style="text-align:center; padding:3rem 1rem; color:#bbb;">
                <p style="font-size:2.5rem; margin-bottom:0.5rem;">📋</p>
                <p style="font-size:1rem;">Results will appear here</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
