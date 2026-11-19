import os
import streamlit as st
from assets.frontend_theme import (
    inject_lpu_theme,
    render_top_banner,
    render_cinematic_footer,
    get_lpu_logo_url,
)

# 1. Page Configuration
st.set_page_config(
    page_title="About - LPU ShuttleLyze",
    page_icon="🚌",
    layout="wide",
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLUSTER_IMAGE = os.path.join(PROJECT_ROOT, "lpu_location_clusters_plot.png")
HEATMAP_IMAGE = os.path.join(PROJECT_ROOT, "lpu_demand_heatmap.png")

# 2. Inject Black & Dark Orange Theme
inject_lpu_theme()
render_top_banner()

# Custom page styles
st.markdown("""
<style>
.section-heading {
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    border-bottom: 1px solid rgba(255, 106, 0, 0.3);
    padding-bottom: 8px;
    margin: 35px 0 16px 0;
    letter-spacing: -0.3px;
}
.section-heading::before {
    content: '✦ ';
    color: #FF6A00;
}
.info-card {
    background: #121212;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 3px solid #CC4B00;
    border-radius: 12px;
    padding: 18px 20px;
    min-height: 180px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: all 0.25s ease;
    margin-bottom: 14px;
}
.info-card:hover {
    border-color: rgba(255, 106, 0, 0.5);
    border-left-color: #FF6A00;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 106, 0, 0.15);
}
.info-card h3 {
    color: #FFFFFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    margin-top: 0 !important;
    margin-bottom: 8px !important;
}
.info-card p {
    color: #B3B3B3 !important;
    font-size: 13.5px !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}
.tech-tag {
    display: inline-block;
    background: rgba(255, 106, 0, 0.12);
    border: 1px solid rgba(255, 106, 0, 0.35);
    color: #FF6A00;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    margin: 0 6px 8px 0;
}
.note-box {
    background: #141414;
    border: 1px solid rgba(255, 106, 0, 0.3);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 13px;
    color: #B3B3B3;
    line-height: 1.6;
    margin: 15px 0 25px 0;
}
.note-box b {
    color: #FF6A00;
}
.workflow-card {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    background: #121212;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.25s ease;
}
.workflow-card:hover {
    border-color: rgba(255, 106, 0, 0.4);
    box-shadow: 0 6px 20px rgba(255, 106, 0, 0.1);
}
.workflow-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #FF6A00;
    line-height: 1;
    min-width: 32px;
}
.workflow-title {
    color: #FFFFFF;
    font-weight: 700;
    font-size: 15px;
    margin-bottom: 4px;
}
.workflow-description {
    color: #B3B3B3;
    font-size: 13.5px;
    line-height: 1.55;
}
</style>
""", unsafe_allow_html=True)

# 3. Floating Header Navigation Bar
abt_logo_url = get_lpu_logo_url()
header_brand, header_spacer, header_nav = st.columns([3.2, 0.6, 6.2], gap="small", vertical_alignment="center")

with header_brand:
    abt_logo_html = f'<img src="{abt_logo_url}" style="height: 44px; width: 44px; margin-right: 14px; object-fit: contain; filter: drop-shadow(0 0 10px rgba(255,106,0,0.5));" alt="LPU Logo">' if abt_logo_url else ''
    st.markdown(f'''
    <div style="display: flex; align-items: center; height: 65px; box-sizing: border-box; padding-left: 10px;">
        {abt_logo_html}
        <div>
            <span style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; letter-spacing: 1.5px; line-height: 1;">
                SHUTTLE<span style="color: #FF6A00;">LYZE</span>
            </span>
            <div style="color: #B3B3B3; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">System Architecture & ML Specs</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with header_nav:
    nav1, nav2, nav3, nav4, nav5 = st.columns([1.0, 1.3, 1.3, 0.9, 0.9], gap="small", vertical_alignment="center")
    with nav1:
        if st.button("Home", key="abt_nav_home", use_container_width=True):
            st.switch_page("app.py")
    with nav2:
        if st.button("Services", key="abt_nav_services", use_container_width=True):
            if os.path.exists("pages/Services.py"):
                st.switch_page("pages/Services.py")
    with nav3:
        if st.button("Safety Hub", key="abt_nav_safety", use_container_width=True):
            if os.path.exists("pages/Safety.py"):
                st.switch_page("pages/Safety.py")
    with nav4:
        if st.button("News & Alerts", key="abt_nav_news", use_container_width=True):
            if os.path.exists("pages/News.py"):
                st.switch_page("pages/News.py")
    with nav5:
        if st.button("Contact", key="abt_nav_contact", use_container_width=True):
            if os.path.exists("pages/Contact.py"):
                st.switch_page("pages/Contact.py")

# 4. Helper Functions
def section(title):
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)

def info_card(title, body):
    st.markdown(f'<div class="info-card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

# 5. Project Hero Container
st.markdown('''
<div style="background: linear-gradient(135deg, #181818 0%, #101010 100%); border: 1px solid rgba(255, 106, 0, 0.35); border-left: 4px solid #FF6A00; border-radius: 14px; padding: 28px 32px; margin: 15px 0 25px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <div class="lpu-pill-badge" style="margin-bottom: 8px;">INT395 • CA1 RESEARCH PROJECT</div>
    <h1 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 800; margin: 0 0 10px 0;">
        Intelligent Campus Transit <span style="color: #FF6A00;">Demand Prediction & Spatial Analytics</span>
    </h1>
    <p style="color: #B3B3B3; font-size: 14px; line-height: 1.7; margin: 0; max-width: 900px;">
        ShuttleLyze applies ensemble supervised learning, transportation demand forecasting, and geospatial routing to optimize student and faculty mobility across all 47 campus zones at Lovely Professional University.
    </p>
</div>
''', unsafe_allow_html=True)

# # 7. PROJECT OVERVIEW
# ============================================================
section("Project Overview")

overview = [
    (
        "🎯 Project Objective",
        "Predict passenger demand, analyze travel patterns, compare campus "
        "locations, and support transportation resource planning."
    ),
    (
        "📊 Dataset & Location Mapping",
        "The transportation dataset was sourced from the University of Chicago "
        "shuttle service. Pickup and drop-off locations were mapped to "
        "corresponding LPU campus blocks, with location names and distances "
        "aligned for campus route analysis."
    ),
    (
        "🚌 Application",
        "The application combines demand prediction, historical route analytics, "
        "saved distance and travel-time matrices, geospatial route visualization, "
        "and operational insights."
    ),
]

cols = st.columns(3, gap="medium")

for col, (title, body) in zip(cols, overview):
    with col:
        info_card(title, body)

# ============================================================
# 8. TECHNOLOGIES USED
# ============================================================
section("Technologies & Tools")

st.markdown(
    """
    <span class="tech-tag">Python</span>
    <span class="tech-tag">Streamlit</span>
    <span class="tech-tag">Pandas</span>
    <span class="tech-tag">NumPy</span>
    <span class="tech-tag">Scikit-learn</span>
    <span class="tech-tag">LightGBM</span>
    <span class="tech-tag">XGBoost</span>
    <span class="tech-tag">Random Forest</span>
    <span class="tech-tag">Joblib</span>
    <span class="tech-tag">Matplotlib</span>
    <span class="tech-tag">Seaborn</span>
    <span class="tech-tag">Geospatial Mapping</span>
    <span class="tech-tag">OSRM</span>
    <span class="tech-tag">Excel</span>
    """,
    unsafe_allow_html=True,
)

tech_info = [
    (
        "Data Processing & Preprocessing",
        "Pandas and NumPy support data loading, cleaning, feature preparation, "
        "aggregation, and numerical calculations. Scikit-learn provides "
        "imputation, encoding, preprocessing pipelines, and model evaluation."
    ),
    (
        "Interactive Application",
        "Streamlit provides the interface for selecting campus locations and "
        "viewing demand, route, travel-time, and transportation analytics."
    ),
    (
        "Machine Learning",
        "LightGBM and XGBoost are gradient-boosting algorithms for structured-data "
        "prediction. Random Forest is another ensemble approach. The model used "
        "for each output should match the model actually loaded by the app."
    ),
    (
        "Geospatial Mapping & Visualization",
        "Mapped campus coordinates, block names, route distance, and travel-time "
        "information support spatial analysis. OSRM can provide road-route "
        "alternatives where configured. Matplotlib and Seaborn support heatmaps "
        "and location-clustering visualizations."
    ),
]

for start in range(0, len(tech_info), 2):
    cols = st.columns(2, gap="medium")

    for col, (title, body) in zip(cols, tech_info[start:start + 2]):
        with col:
            info_card(title, body)

# ============================================================
# 9. MODELS & ANALYTICAL COMPONENTS
# ============================================================
section("Models & Analytical Components")

model_info = [
    (
        "1. LightGBM",
        "A gradient-boosting framework based on decision trees. It can learn "
        "patterns in structured transportation data and support passenger-demand "
        "prediction when trained for that target."
    ),
    (
        "2. XGBoost",
        "An optimized gradient-boosting algorithm that builds trees sequentially "
        "to improve predictions. Its role depends on the target and training setup."
    ),
    (
        "3. Geospatial Route Analysis",
        "Uses mapped campus locations and route information to analyze "
        "pickup-to-drop paths, route distance, and estimated travel time. "
        "Road routing is separate from a supervised-learning model."
    ),
    (
        "4. Demand Heatmap & Location Clustering",
        "Compares locations using trip counts, passenger volume, average "
        "passengers per trip, and average travel time. The clustering algorithm "
        "description should match the implementation used to generate the plot."
    ),
]

for start in range(0, len(model_info), 2):
    cols = st.columns(2, gap="medium")

    for col, (title, body) in zip(cols, model_info[start:start + 2]):
        with col:
            info_card(title, body)

st.markdown(
    """
    <div class="note-box">
        <b>Model transparency:</b> LightGBM, XGBoost, and Random Forest are
        listed as project technologies. Identify which trained model actually
        generates each prediction. Do not attribute the saved validation scores
        to LightGBM or XGBoost unless those exact models produced them.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 10. DEMAND MODEL VALIDATION
# ============================================================
section("Demand Prediction Model Validation")

st.write(
    "These are the previously recorded evaluation results. Lower MAE, MSE, "
    "and RMSE indicate smaller prediction errors; R² and explained variance "
    "closer to 1 generally indicate a stronger fit."
)

metrics = [
    ("R² Score", "0.998451"),
    ("MAE", "0.100500"),
    ("MSE", "0.112171"),
    ("RMSE", "0.334919"),
    ("Explained Variance", "0.998454"),
    ("Maximum Absolute Error", "3.233333"),
    ("Within ±1 Passenger", "97.40%"),
    ("Within ±2 Passengers", "99.45%"),
]

for start in range(0, len(metrics), 3):
    cols = st.columns(3, gap="medium")

    for col, (label, value) in zip(cols, metrics[start:start + 3]):
        with col:
            st.metric(label=label, value=value)

st.markdown(
    """
    <div class="note-box">
        <b>Validation limitation:</b> These are the saved evaluation results
        previously reported for the demand prediction pipeline. Since the model
        was trained before the later validation split was created, some evaluated
        records may overlap with its original training data. Independent testing
        and target-leakage checks are needed before treating these metrics as
        performance on genuinely unseen trips.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 11. CAMPUS LOCATION CLUSTERING
# ============================================================
section("Campus Location Clustering")

st.write(
    "This plot compares campus locations by total trips generated and total "
    "passengers carried. Displayed cluster categories and marker shapes help "
    "distinguish transportation patterns across campus zones."
)

if os.path.exists(CLUSTER_IMAGE):
    st.image(
        CLUSTER_IMAGE,
        caption="LPU Campus Location Clustering — Trips vs Passenger Volume",
        use_container_width=True,
    )
else:
    st.warning(
        "Clustering image not found. Place "
        "'lpu_location_clusters_plot.png' in the project root."
    )

# ============================================================
# 12. CAMPUS DEMAND HEATMAP
# ============================================================
section("Campus Demand Heatmap")

st.write(
    "This heatmap compares campus locations using total trips, total passengers, "
    "average passengers per trip, and average travel time to identify locations "
    "with comparatively high transportation activity."
)

if os.path.exists(HEATMAP_IMAGE):
    st.image(
        HEATMAP_IMAGE,
        caption="LPU Campus Locations — Demand Heatmap & Operational Metrics",
        use_container_width=True,
    )
else:
    st.warning(
        "Heatmap image not found. Place 'lpu_demand_heatmap.png' "
        "in the project root."
    )

# ============================================================
# 13. PROJECT WORKFLOW
# ============================================================
section("Project Workflow")

workflow = [
    (
        "01",
        "Data Collection & Location Mapping",
        "Source transportation records and map pickup/drop locations to LPU "
        "campus blocks and distances."
    ),
    (
        "02",
        "Data Preprocessing",
        "Prepare numerical and categorical features and handle missing values."
    ),
    (
        "03",
        "Demand Prediction",
        "Use the trained model configured in the application to estimate "
        "passenger demand."
    ),
    (
        "04",
        "Geospatial Route Analysis",
        "Analyze mapped locations, distances, road routes, and estimated "
        "travel times."
    ),
    (
        "05",
        "Visualization & Analytics",
        "Present demand heatmaps, location clusters, historical metrics, "
        "and route comparisons."
    ),
    (
        "06",
        "Resource Planning",
        "Use demand estimates and route context to support shuttle scheduling "
        "and allocation decisions."
    ),
]

for number, title, description in workflow:
    st.markdown(
        f"""
        <div class="workflow-card">
            <div class="workflow-number">{number}</div>
            <div style="flex:1;">
                <div class="workflow-title">{title}</div>
                <div class="workflow-description">{description}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# 14. END OF ABOUT PAGE — NO FOOTER
# ============================================================
st.write("")


render_cinematic_footer()
