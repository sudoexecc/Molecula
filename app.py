import streamlit as st
from PIL import Image
import io
from simulated_detector import SimulatedDetector
from utils import draw_detections, crop_wbcs

# Page Configuration
st.set_page_config(
    page_title="Molecula - Blood Smear Analysis",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Mode & Neon Accents
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #fafafa !important;
    }
    
    /* Neon Accents */
    .highlight-blue {
        color: #00f3ff;
        font-weight: bold;
    }
    .highlight-purple {
        color: #bc13fe;
        font-weight: bold;
    }
    
    /* Cards/Metrics */
    div[data-testid="stMetric"] {
        background-color: #1a1c24;
        border: 1px solid #2d303e;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Warning Box */
    .warning-box {
        background-color: rgba(255, 75, 75, 0.1);
        border: 1px solid rgba(255, 75, 75, 0.5);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🩸 Molecula")
    st.caption("Automated Hematology Prototype")
    
    st.divider()
    
    st.header("Settings")
    confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    
    st.divider()
    
    st.info(
        """
        **Disclaimer**: This is a **DEMO** application using simulated data. 
        It is NOT a medical device and should not be used for diagnosis.
        """
    )
    
    st.markdown("---")
    st.markdown("Built with Python & YOLOv7 (Simulated)")

# Main Content
st.title("Peripheral Blood Smear Analysis")
st.markdown("Upload a microscopic image of a blood smear to detect **RBCs**, **WBCs**, and **Platelets**.")

# File Uploader
uploaded_file = st.file_uploader("Choose a blood smear image...", type=["jpg", "png", "jpeg", "tiff"])

if uploaded_file is not None:
    # Load Image
    image = Image.open(uploaded_file).convert("RGB")
    
    # Run Simulation
    with st.spinner("Analyzing cell morphology..."):
        detector = SimulatedDetector()
        detections = detector.detect(image)
        
        # Filter by confidence
        detections = [d for d in detections if d['confidence'] >= confidence]
        
        # Get Flags & Counts
        flags, counts, wbc_subtypes = detector.get_disease_flags(detections)
        
        # Draw Detections
        annotated_image = image.copy()
        annotated_image = draw_detections(annotated_image, detections)
        
        # Crop WBCs
        wbc_crops = crop_wbcs(image, detections)

    # --- Layout ---
    
    # 1. Top Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("RBC Count", counts['RBC'], delta_color="off")
    col2.metric("WBC Count", counts['WBC'], delta_color="off")
    col3.metric("Platelet Count", counts['Platelets'], delta_color="off")
    
    st.divider()

    # 2. Main Analysis Area (Image + Flags)
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.subheader("Annotated Slide")
        st.image(annotated_image, use_container_width=True)
        
        # Export Button
        buf = io.BytesIO()
        annotated_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Annotated Image",
            data=byte_im,
            file_name="molecula_analysis.png",
            mime="image/png"
        )

    with row1_col2:
        st.subheader("Clinical Flags (PROTOTYPE)")
        
        if flags:
            for flag in flags:
                severity_color = "red" if flag['severity'] == 'danger' else "orange"
                st.markdown(
                    f"""
                    <div class="warning-box" style="border-color: {severity_color};">
                        <h4 style="color: {severity_color}; margin: 0;">⚠️ {flag['title']}</h4>
                        <p style="margin-top: 5px; font-size: 0.9em;">{flag['description']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.success("No significant morphological anomalies detected in this field of view.")
            
        st.subheader("WBC Differential")
        if wbc_subtypes:
            for subtype, count in wbc_subtypes.items():
                st.write(f"**{subtype}**: {count}")
        else:
            st.write("No WBCs detected.")

    st.divider()

    # 3. WBC Gallery
    st.subheader("WBC Morphology Gallery")
    if wbc_crops:
        # Display crops in a grid
        cols = st.columns(6)
        for idx, crop_data in enumerate(wbc_crops):
            col = cols[idx % 6]
            with col:
                st.image(crop_data['image'], caption=crop_data['subtype'], use_container_width=True)
    else:
        st.info("No WBCs found to crop.")

else:
    # Empty State
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; border: 2px dashed #333; border-radius: 10px;">
            <h3 style="color: #666;">Waiting for image upload...</h3>
            <p style="color: #444;">Drag and drop a file above to begin analysis.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
