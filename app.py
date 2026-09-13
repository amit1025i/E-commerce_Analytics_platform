import streamlit as st
import pandas as pd
import plotly.express as px
import base64


# Page Configuration

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load Background Image

def get_image_base64(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


image_base64 = get_image_base64(
    "assets/ecommerce_home.jpg"
)


# Custom CSS

st.markdown(
    """
<style>

/* Main App */

.stApp {
    background: #f7f8fa;
}


/* Remove Default Streamlit Sidebar Navigation  */

div[data-testid="stSidebarNav"] {
    display: none;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(0, 0, 0, 0.08);
}


/* Sidebar text */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1f2937 !important;
}


/* Sidebar buttons */

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(255, 255, 255, 0.55);
    color: #1f2937 !important;
    border: 1px solid rgba(0, 0, 0, 0.10);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
    font-size: 14px;
    font-weight: 500;
    text-align: left;
    transition: 0.2s ease;
}


/* Sidebar button hover */

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0, 0, 0, 0.06);
    border-color: rgba(0, 0, 0, 0.18);
}


/* Sidebar button text */

section[data-testid="stSidebar"] .stButton > button p {
    color: #1f2937 !important;
}


/* Hero Section */

.hero {
    position: relative;
    width: 100%;
    height: 470px;

    background-image:
        linear-gradient(
            90deg,
            rgba(255,255,255,0.94) 0%,
            rgba(255,255,255,0.78) 38%,
            rgba(255,255,255,0.10) 72%
        ),
        url("data:image/jpeg;base64,IMAGE_DATA");

    background-size: cover;
    background-position: center;

    border-radius: 20px;
    overflow: hidden;

    display: flex;
    align-items: center;

    margin-bottom: 30px;
}


/* Hero content */

.hero-content {
    width: 46%;
    margin-left: 55px;
}


/* Small label */

.hero-label {
    font-size: 13px;
    font-weight: 600;
    color: #6b7280;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}


/* Hero title */

.hero-title {
    font-size: 48px;
    line-height: 1.08;
    font-weight: 750;
    color: #111827;
    margin-bottom: 18px;
}


/* Hero description */

.hero-description {
    font-size: 17px;
    line-height: 1.65;
    color: #374151;
    max-width: 520px;
    margin-bottom: 25px;
}


/* Upload Area */

.upload-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 30px;
}


/* Module Cards */

.module-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 22px;
    height: 150px;
    transition: 0.2s ease;
}


.module-card:hover {
    border-color: #cbd5e1;
    box-shadow: 0 5px 18px rgba(0,0,0,0.05);
}


.module-title {
    font-size: 17px;
    font-weight: 650;
    color: #111827;
    margin-bottom: 9px;
}


.module-text {
    font-size: 14px;
    line-height: 1.55;
    color: #6b7280;
}


/* Section Title */

.section-heading {
    font-size: 22px;
    font-weight: 650;
    color: #111827;
    margin: 28px 0 14px 0;
}


/*  Upload Button */

.upload-button-container {
    margin-top: 8px;
}


/* Hide Streamlit Main Menu / Footer */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""".replace(
        "IMAGE_DATA",
        image_base64
    ),
    unsafe_allow_html=True
)



# Sidebar

with st.sidebar:

    st.markdown(
        """
<div style="
    font-size:23px;
    font-weight:700;
    color:#111827;
    margin-bottom:3px;
">
    🛒 E-Commerce
</div>

<div style="
    font-size:13px;
    color:#6b7280;
    margin-bottom:22px;
">
    Analytics Platform
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
<div style="
    font-size:14px;
    font-weight:650;
    color:#374151;
    margin-bottom:10px;
">
    Navigation
</div>
""",
        unsafe_allow_html=True
    )


    # Dashboard

    st.markdown(
        """
<div style="
    background:rgba(0,0,0,0.06);
    color:#111827;
    padding:10px 12px;
    border-radius:8px;
    margin-bottom:7px;
    font-size:14px;
    font-weight:600;
">
     Dashboard
</div>
""",
        unsafe_allow_html=True
    )


    # Data Upload

    if st.button(
        "  Data Upload & Processing",
        use_container_width=True
    ):
        st.switch_page("pages/data_upload.py")


    # Sales

    if st.button(
        "  Sales Analysis",
        use_container_width=True
    ):
        st.switch_page("pages/sales_analysis.py")


    # Profit

    if st.button(
        "  Profit Analysis",
        use_container_width=True
    ):
        st.switch_page("pages/profit_analysis.py")


    # Customer

    if st.button(
        "  Customer Analysis",
        use_container_width=True
    ):
        st.switch_page("pages/customer_analysis.py")


    # Sales vs Profit

    if st.button(
        "  Sales vs Profit",
        use_container_width=True
    ):
        st.switch_page("pages/sales_vs_profit.py")


    # Data Explorer

    if st.button(
        "  Data Explorer",
        use_container_width=True
    ):
        st.switch_page("pages/data_explorer.py")


    st.markdown("---")

    st.markdown(
        """
<div style="
    font-size:14px;
    font-weight:650;
    color:#374151;
    margin-bottom:8px;
">
    Settings
</div>
""",
        unsafe_allow_html=True
    )


    show_advanced = st.checkbox(
        "Show advanced metrics"
    )


    st.markdown("---")

    st.caption(
        "E-Commerce Analytics v1.0"
    )



# HOMEPAGE

if "data" not in st.session_state:



    # HERO

    st.markdown(
        """
<div class="hero">

<div class="hero-content">

<div class="hero-label">
BUSINESS INTELLIGENCE
</div>

<div class="hero-title">
E-Commerce<br>
Analytics
</div>

<div class="hero-description">
Turn your e-commerce data into clear business insights.
Explore sales, profit, customers, products and regional
performance from one place.
</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )


    
    # DATA UPLOAD

    st.markdown(
        """
<div class="section-heading">
Get started
</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        """
<div class="upload-section">

<div style="
    font-size:19px;
    font-weight:650;
    color:#111827;
    margin-bottom:8px;
">
     Upload your dataset
</div>

<div style="
    color:#6b7280;
    font-size:14px;
    line-height:1.6;
    margin-bottom:16px;
">
    Start by uploading your CSV or Excel dataset.
    Once the data is processed, you can explore
    sales, profit, customer and product insights.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    # Actual working Streamlit button

    if st.button(
        "Upload Dataset",
        type="primary",
        use_container_width=False
    ):
        st.switch_page(
            "pages/data_upload.py"
        )


    
    # MODULES

    st.markdown(
        """
<div class="section-heading">
Explore the platform
</div>
""",
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
<div class="module-card">

<div class="module-title">
 Sales Analysis
</div>

<div class="module-text">
Track sales trends, categories,
regions and product performance.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="module-card">

<div class="module-title">
 Profit Analysis
</div>

<div class="module-text">
Understand profitability and identify
products and segments driving results.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
<div class="module-card">

<div class="module-title">
 Customer Analysis
</div>

<div class="module-text">
Explore customer behaviour, segments
and contribution to overall sales.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    st.stop()


# Existing Dashboard

data = st.session_state["data"].copy()

st.markdown(
    '<div class="section-heading">Dashboard</div>',
    unsafe_allow_html=True
)

