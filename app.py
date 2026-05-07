import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np

import sys
sys.path.append("src")

from constants import (
    CLASS_NAMES,
    ADVISORY,
    SIGN_CATEGORIES,
    get_category,
    STYLES
)

from src.model_utils import load_model

from src.image_utils import (
    load_class_images,
    to_b64
)

from src.gradcam import make_gradcam

# ── Page Configuration ────────────────────────────────────
st.set_page_config(
    page_title="Traffic Sign Recognition",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject Styles & Initialize ────────────────────────────
st.markdown(STYLES, unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Google Sans', sans-serif !important; }
h1,h2,h3 { color:#ffffff !important; }

/* ===== CLICKABLE IMAGE OVERLAY ===== */

.sign-wrapper {
    position: relative;
    width: 100%;
    height: 190px;
    margin-bottom: 10px;
}

.sign-icon {
    position: relative;
    height: 190px;
    border-radius: 14px;
    overflow: hidden;
    background: #1e1e2e;
    cursor: pointer;
    border: 2px solid transparent;
    transition: transform 0.12s ease, box-shadow 0.12s ease, border 0.12s ease;
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
}

.sign-icon:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(26,115,232,0.28);
}

.sign-icon.active {
    border: 2px solid #1a73e8;
    box-shadow: 0 0 18px rgba(26,115,232,0.55), 0 0 30px rgba(26,115,232,0.20);
}

.sign-icon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    border-radius: 12px;
}

/* invisible clickable overlay */
div[data-testid="stButton"]:has(button[kind="secondary"]) {
    position: relative !important;
    margin-top: -190px !important;
    height: 190px !important;
    z-index: 999 !important;
}

div[data-testid="stButton"]:has(button[kind="secondary"]) button {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 190px !important;
    opacity: 0 !important;
    border: none !important;
    background: transparent !important;
    cursor: pointer !important;
    z-index: 999 !important;
}

.card-dark {
    background: #1e1e2e;
    border: 1px solid #2d2d3f;
    border-radius: 12px;
    padding: 1rem 1.2rem;
}

.feedback-form input,
.feedback-form textarea {
    width:100%; background:#1e1e2e; border:1px solid #2d2d3f;
    border-radius:8px; color:#e8eaed; padding:0.5rem 0.7rem;
    font-size:0.82rem; margin-bottom:0.5rem; outline:none;
    box-sizing:border-box; font-family:'Google Sans',sans-serif;
}
.feedback-form input:focus,
.feedback-form textarea:focus { border-color:#1a73e8; }
.feedback-form button {
    background:#1a73e8; color:white; border:none;
    border-radius:8px; padding:0.45rem 1.2rem;
    font-size:0.82rem; font-weight:600; cursor:pointer;
}
.feedback-form button:hover { background:#1557b0; }
</style>
""", unsafe_allow_html=True)

# Load modularized components
model = load_model()
class_images = load_class_images()


# ── Session state ─────────────────────────────────────────
if "home_selected" not in st.session_state:
    st.session_state.home_selected = None

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0;'>
        <span style='font-size:1.4rem;'>🚦</span>
        <span style='font-size:1rem; font-weight:700; color:#1a73e8; margin-left:8px;'>TSR System</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Traffic Sign Recognition · CNN · 99.87%")
    st.markdown("---")
    st.metric("Accuracy", "99.87%")
    st.metric("Classes",  "43")
    st.metric("Images",   "39,209")
    st.markdown("---")
    st.markdown("""
    <div style='font-weight:600; font-size:0.82rem; color:#e8eaed; margin-bottom:0.5rem;'>💬 Feedback</div>
    <div class='feedback-form'>
        <form action="https://formspree.io/f/xkoyzybw" method="POST">
            <input type="email" name="email" placeholder="Your email" required/>
            <textarea name="message" rows="3" placeholder="Your message..." required></textarea>
            <button type="submit">Send →</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div style='padding:1.5rem 0 0.5rem;'>
    <div style='font-size:2rem; font-weight:700; color:#ffffff;'>
        🚦 Traffic Sign Recognition
    </div>
    <div style='color:#9aa0a6; font-size:0.88rem; margin-top:0.3rem;'>
        CNN · 43 classes · 99.87% accuracy · GTSRB dataset
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# AUTO-SLIDESHOW (Bulletproof Iframe Implementation)
# ──────────────────────────────────────────────────────────

slideshow_html = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap');
body {
    margin: 0;
    padding: 0;
    font-family: 'Google Sans', sans-serif;
    background-color: transparent; /* Seamlessly blends with Streamlit */
}
.card-dark {
    background: #1e1e2e;
    border: 1px solid #2d2d3f;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #ffffff;
    box-sizing: border-box;
}
.slide-num {
    display: inline-flex; justify-content: center; align-items: center;
    width: 26px; height: 26px; border-radius: 6px;
    background: #2d2d3f; color: #9aa0a6; font-size: 0.8rem; font-weight: 500;
    cursor: pointer; transition: all 0.2s ease; margin-right: 8px;
    border: 1px solid transparent; user-select: none;
}
.slide-num:hover {
    background: #3c3c50; color: #ffffff;
}
.slide-num.active {
    background: #1a73e8; color: #ffffff; font-weight: 700;
    box-shadow: 0 0 10px rgba(26,115,232,0.4);
}
.slide-text-container {
    min-height: 65px;
}
</style>
</head>
<body>

<div class="card-dark" style="min-height:110px; position:relative;">
    <div class="slide-text-container">
        <div style="display:flex; align-items:center; margin-bottom:0.6rem;">
            <span id="tsr-slide-icon" style="font-size:1.1rem;">🧠</span>
            <span id="tsr-slide-title" style="font-weight:600; margin-left:8px;">Convolutional Neural Network</span>
        </div>
        <div id="tsr-slide-desc" style="color:#9aa0a6; font-size:0.82rem; line-height: 1.4;">
            3 conv blocks with BatchNorm and Dropout. Trained end-to-end on 39,209 real-world images at 32×32 resolution.
        </div>
    </div>

    <div style="margin-top:0.8rem; display:flex; align-items:center;">
        <div class="slide-num active" onclick="setSlide(0)">1</div>
        <div class="slide-num" onclick="setSlide(1)">2</div>
        <div class="slide-num" onclick="setSlide(2)">3</div>
        <div class="slide-num" onclick="setSlide(3)">4</div>
        <div class="slide-num" onclick="setSlide(4)">5</div>
    </div>
</div>

<script>
    const slides = [
        {icon: '🧠', title: 'Convolutional Neural Network', desc: '3 conv blocks with BatchNorm and Dropout. Trained end-to-end on 39,209 real-world images at 32×32 resolution.'},
        {icon: '📊', title: 'Real-World Dataset', desc: 'German traffic sign photos across 43 classes. Natural class imbalance from 210 to 2,250 images — handled with stratified splits.'},
        {icon: '✅', title: '99.87% Validation Accuracy', desc: 'Achieved in 20 epochs with Adam optimizer. Per-class F1-score is 1.00 for 40 out of 43 classes.'},
        {icon: '🔥', title: 'Grad-CAM Explainability', desc: 'Visual heatmaps show exactly which pixels the model focused on — making predictions interpretable, not just accurate.'},
        {icon: '🚗', title: 'Real-World ADAS Application', desc: 'Core technology behind autonomous vehicles. Reads signs in milliseconds and advises the driver instantly.'}
    ];

    let currentSlide = 0;
    let slideInterval;

    function renderSlide(index) {
        document.getElementById('tsr-slide-icon').innerText = slides[index].icon;
        document.getElementById('tsr-slide-title').innerText = slides[index].title;
        document.getElementById('tsr-slide-desc').innerText = slides[index].desc;

        const nums = document.querySelectorAll('.slide-num');
        nums.forEach((el, i) => {
            if (i === index) el.classList.add('active');
            else el.classList.remove('active');
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        renderSlide(currentSlide);
    }

    function setSlide(index) {
        currentSlide = index;
        renderSlide(index);
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, 2000);
    }

    // Start auto loop
    slideInterval = setInterval(nextSlide, 2000);
</script>

</body>
</html>
"""

# Render the isolated iframe inside Streamlit
components.html(slideshow_html, height=170)


# ── Main layout ───────────────────────────────────────────
grid_col, pred_col = st.columns([2.4, 1], gap="large")

with grid_col:
    st.markdown("""
    <div style='font-weight:600; font-size:0.85rem; color:#ffffff; margin-bottom:0.5rem;'>
        All 43 Classes — click any sign
    </div>
    """, unsafe_allow_html=True)

    cat_filter = st.selectbox(
        "Filter", ["All"] + list(SIGN_CATEGORIES.keys()),
        label_visibility="collapsed"
    )

    show_ids     = list(range(43)) if cat_filter == "All" else SIGN_CATEGORIES[cat_filter]
    cols_per_row = 6
    rows         = [show_ids[i:i+cols_per_row]
                    for i in range(0, len(show_ids), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for col, cid in zip(cols, row):
            with col:
                if cid in class_images:
                    try:
                        pil      = Image.open(class_images[cid]).convert("RGB")
                        selected = st.session_state.home_selected == cid
                        b64      = to_b64(pil)
                        css      = "sign-icon active" if selected else "sign-icon"

                        st.markdown(f"""
<div class='sign-wrapper'>
    <div class='{css}'>
        <img src='data:image/png;base64,{b64}'/>
    </div>
</div>
""", unsafe_allow_html=True)
                        if st.button("", key=f"g_{cid}", use_container_width=True, type="secondary"):
                            st.session_state.home_selected = cid
                            st.rerun()
                    except Exception:
                        continue

# ── Prediction Panel ──────────────────────────────────────
with pred_col:
    st.markdown("""
    <div style='font-weight:600; font-size:0.85rem; color:#ffffff; margin-bottom:0.5rem;'>
        Prediction
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.home_selected is not None:
        cid    = st.session_state.home_selected
        pil    = Image.open(class_images[cid]).convert("RGB")
        b64_lg = to_b64(pil, size=(300, 300))

        st.markdown(f"""
        <div style='border-radius:16px; overflow:hidden; box-shadow:0 8px 28px rgba(0,0,0,0.5); margin-bottom:1rem;'>
            <img src='data:image/png;base64,{b64_lg}' style='width:100%; display:block;'/>
        </div>
        """, unsafe_allow_html=True)

        img_arr   = np.array(pil.resize((32, 32))) / 255.0
        img_input = np.expand_dims(img_arr, axis=0)
        preds     = model.predict(img_input, verbose=0)[0]

        top_idx    = np.argmax(preds)
        confidence = preds[top_idx] * 100
        sign_name  = CLASS_NAMES[top_idx]
        cat        = get_category(top_idx)
        advisory   = ADVISORY.get(sign_name, "Stay alert.")
        top5       = np.argsort(preds)[-5:][::-1]

        st.markdown(f"""
        <div style='margin-bottom:0.8rem;'>
            <div style='font-size:1.05rem; font-weight:700; color:#ffffff;'>{sign_name}</div>
            <div style='font-size:0.75rem; color:#9aa0a6; margin-top:2px;'>{cat}</div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(confidence), text=f"{confidence:.1f}% confidence")

        st.markdown(f"""
        <div class='card-dark' style='margin-top:0.8rem; font-size:0.82rem;'>
            <div style='font-weight:600; color:#ffffff; margin-bottom:0.3rem;'>Driver Advisory</div>
            <div style='color:#9aa0a6;'>{advisory}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='font-weight:600; font-size:0.82rem; color:#ffffff; margin:0.9rem 0 0.4rem;'>
            Top 5 Predictions
        </div>
        """, unsafe_allow_html=True)

        for i, idx in enumerate(top5):
            pct   = preds[idx] * 100
            name  = CLASS_NAMES[idx]
            color = "#1a73e8" if i == 0 else "#3c3c50"
            st.markdown(f"""
            <div style='margin:5px 0;'>
                <div style='display:flex; justify-content:space-between; font-size:0.73rem; margin-bottom:2px;'>
                    <span style='color:{"#ffffff" if i==0 else "#9aa0a6"};
                                 font-weight:{"600" if i==0 else "400"};
                                 white-space:nowrap; overflow:hidden;
                                 text-overflow:ellipsis; max-width:140px;'>
                        {name}
                    </span>
                    <span style='color:#9aa0a6;'>{pct:.1f}%</span>
                </div>
                <div style='background:#2d2d3f; border-radius:4px; height:5px; overflow:hidden;'>
                    <div style='width:{pct}%; height:100%; background:{color}; border-radius:4px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Grad-CAM
        st.markdown("""
        <div style='font-weight:600; font-size:0.82rem; color:#ffffff; margin:1rem 0 0.3rem;'>
            🔥 How the AI sees this sign
        </div>
        <div style='font-size:0.73rem; color:#9aa0a6; margin-bottom:0.6rem;'>
            Red = focused · Blue = ignored
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Generating heatmap..."):
            heatmap, blended = make_gradcam(model, pil)

        if heatmap is not None and blended is not None:
            h1, h2 = st.columns(2)
            with h1:
                st.image(heatmap, caption="Heatmap", use_container_width=True)
            with h2:
                st.image(blended, caption="Overlay", use_container_width=True)
        else:
            st.caption("Heatmap unavailable for this image.")

    else:
        st.markdown("""
        <div class='card-dark' style='text-align:center; padding:3rem 1rem;'>
            <div style='font-size:2rem; margin-bottom:0.5rem;'>👆</div>
            <div style='color:#9aa0a6; font-size:0.85rem;'>
                Click any sign on the left<br>to see the AI prediction
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='color:#5f6368; font-size:0.75rem; text-align:center;'>
    Built by <b style='color:#9aa0a6;'>Agasthyan</b> ·
    TensorFlow · Streamlit · GTSRB · 2026
</div>
""", unsafe_allow_html=True)