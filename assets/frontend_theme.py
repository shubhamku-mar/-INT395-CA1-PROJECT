import os
import base64
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@st.cache_data
def get_asset_b64(filename, mime_type=None):
    """Encodes an asset file into a base64 data URL."""
    if mime_type is None:
        if filename.endswith(".png"):
            mime_type = "image/png"
        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            mime_type = "image/jpeg"
        elif filename.endswith(".svg"):
            mime_type = "image/svg+xml"
        else:
            mime_type = "application/octet-stream"

    candidates = [
        os.path.join(PROJECT_ROOT, "assets", filename),
        os.path.join(PROJECT_ROOT, filename),
        os.path.join(os.path.dirname(__file__), filename),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:{mime_type};base64,{b64}"
    return None

def get_lpu_logo_url():
    return get_asset_b64("lpu_logo.png", "image/png")

def get_lpu_campus_url():
    return get_asset_b64("lpu_campus.jpg", "image/jpeg")

def inject_lpu_theme():
    """Injects the cinematic Black and Dark Orange theme stylesheet."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

        /* -------------------------------------------------------------
           1. ROOT & CORE BACKGROUND PALETTE
           ------------------------------------------------------------- */
        :root {
            --bg-black: #080808;
            --surface-charcoal: #121212;
            --surface-card: #161616;
            --surface-card-hover: #1c1c1c;
            --orange-primary: #FF6A00;
            --orange-burnt: #CC4B00;
            --orange-glow: rgba(255, 106, 0, 0.45);
            --orange-border: rgba(255, 106, 0, 0.28);
            --orange-border-subtle: rgba(255, 106, 0, 0.15);
            --text-white: #FFFFFF;
            --text-muted: #B3B3B3;
            --text-dim: #777777;
            --border-dark: rgba(255, 255, 255, 0.08);
        }

        html, body, .stApp {
            background-color: #080808 !important;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
        }

        /* Hide default Streamlit header bar, footer, and sidebar */
        .stApp header {
            visibility: hidden !important;
            height: 0px !important;
        }
        [data-testid="stSidebar"] {
            display: none !important;
        }
        footer {
            visibility: hidden !important;
        }

        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 3rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 1440px !important;
            margin: 0 auto !important;
            background-color: transparent !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #080808;
        }
        ::-webkit-scrollbar-thumb {
            background: #2a2a2a;
            border-radius: 4px;
            border: 1px solid rgba(255, 106, 0, 0.2);
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #CC4B00;
        }

        /* -------------------------------------------------------------
           2. STREAMLIT WIDGETS OVERRIDES (INPUTS, BUTTONS, CARDS)
           ------------------------------------------------------------- */

        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, #FF6A00 0%, #CC4B00 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 106, 0, 0.6) !important;
            border-radius: 10px !important;
            font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            padding: 10px 22px !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 4px 18px rgba(255, 106, 0, 0.25) !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.4);
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(255, 106, 0, 0.5) !important;
            border-color: #FF6A00 !important;
            color: #FFFFFF !important;
        }
        .stButton button:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 10px rgba(255, 106, 0, 0.3) !important;
        }

        /* Selectboxes & Dropdowns */
        [data-testid="stSelectbox"] label,
        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stNumberInput"] label {
            color: #B3B3B3 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            letter-spacing: 0.4px !important;
            text-transform: uppercase !important;
            margin-bottom: 6px !important;
        }

        [data-baseweb="select"] > div,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input {
            background-color: #121212 !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
            font-size: 14px !important;
            transition: all 0.25s ease !important;
        }

        [data-baseweb="select"] > div:hover,
        [data-testid="stTextInput"] input:hover,
        [data-testid="stTextArea"] textarea:hover,
        [data-testid="stNumberInput"] input:hover {
            border-color: rgba(255, 106, 0, 0.5) !important;
            box-shadow: 0 0 12px rgba(255, 106, 0, 0.15) !important;
        }

        [data-baseweb="select"] > div:focus-within,
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: #FF6A00 !important;
            box-shadow: 0 0 16px rgba(255, 106, 0, 0.35) !important;
        }

        /* Dropdown popover options menu */
        [data-baseweb="popover"], [data-baseweb="menu"] {
            background-color: #121212 !important;
            border: 1px solid rgba(255, 106, 0, 0.3) !important;
            border-radius: 8px !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7) !important;
        }
        [data-baseweb="menu"] li {
            color: #FFFFFF !important;
            background-color: #121212 !important;
            font-size: 13px !important;
            padding: 8px 14px !important;
            transition: background 0.15s ease !important;
        }
        [data-baseweb="menu"] li:hover,
        [aria-selected="true"] {
            background-color: rgba(255, 106, 0, 0.18) !important;
            color: #FF6A00 !important;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background: #121212 !important;
            border: 1px solid rgba(255, 106, 0, 0.22) !important;
            border-radius: 12px !important;
            padding: 16px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }
        [data-testid="stMetricLabel"] {
            color: #B3B3B3 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.6px !important;
        }
        [data-testid="stMetricValue"] {
            color: #FF6A00 !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            font-size: 26px !important;
            text-shadow: 0 0 16px rgba(255, 106, 0, 0.4) !important;
        }
        [data-testid="stMetricDelta"] {
            color: #FFFFFF !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background-color: #121212 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 3px solid #CC4B00 !important;
            border-radius: 10px !important;
            margin-bottom: 12px !important;
            transition: all 0.25s ease !important;
        }
        [data-testid="stExpander"]:hover {
            border-color: rgba(255, 106, 0, 0.4) !important;
            border-left-color: #FF6A00 !important;
            box-shadow: 0 6px 20px rgba(255, 106, 0, 0.1) !important;
        }
        [data-testid="stExpander"] summary {
            background-color: transparent !important;
            padding: 14px 18px !important;
        }
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            letter-spacing: 0.2px !important;
        }
        [data-testid="stExpanderDetails"] {
            padding: 0 18px 16px 18px !important;
            color: #B3B3B3 !important;
            font-size: 14px !important;
            line-height: 1.7 !important;
        }

        /* -------------------------------------------------------------
           3. CINEMATIC GLASSMORPHIC & BENTO CARD CONTAINERS
           ------------------------------------------------------------- */
        .lpu-card {
            background: #121212;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }
        .lpu-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 106, 0, 0.4), transparent);
        }
        .lpu-card:hover {
            border-color: rgba(255, 106, 0, 0.4);
            transform: translateY(-3px);
            box-shadow: 0 14px 35px rgba(255, 106, 0, 0.12);
        }

        .lpu-pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            background: rgba(255, 106, 0, 0.12);
            border: 1px solid rgba(255, 106, 0, 0.35);
            color: #FF6A00;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* -------------------------------------------------------------
           4. FLOATING CINEMATIC NAVIGATION PILL
           ------------------------------------------------------------- */
        .nav-pill-wrapper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(18, 18, 18, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 12px 24px;
            margin: 15px 0 25px 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        }

        .nav-brand-title {
            color: #FFFFFF;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1.5px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .nav-brand-highlight {
            color: #FF6A00;
            text-shadow: 0 0 12px rgba(255, 106, 0, 0.6);
        }

        /* Style navigation buttons to look like clean dark-orange pills */
        [data-testid="stHorizontalBlock"] button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: #B3B3B3 !important;
            border-radius: 8px !important;
            padding: 8px 14px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px !important;
            box-shadow: none !important;
            transition: all 0.25s ease !important;
        }
        [data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
            background: rgba(255, 106, 0, 0.15) !important;
            border-color: rgba(255, 106, 0, 0.5) !important;
            color: #FF6A00 !important;
            box-shadow: 0 0 15px rgba(255, 106, 0, 0.25) !important;
        }

        /* -------------------------------------------------------------
           5. LOADING OVERLAY ANIMATION
           ------------------------------------------------------------- */
        @keyframes lpuRingRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes lpuLogoPulse {
            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 15px rgba(255, 106, 0, 0.4)); }
            50% { transform: scale(1.04); filter: drop-shadow(0 0 30px rgba(255, 106, 0, 0.8)); }
        }
        @keyframes lpuBarFill {
            0% { width: 0%; }
            45% { width: 65%; }
            100% { width: 100%; }
        }
        @keyframes lpuOverlayFade {
            0% { opacity: 1; visibility: visible; }
            75% { opacity: 1; }
            100% { opacity: 0; visibility: hidden; pointer-events: none; }
        }

        .lpu-loader-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #080808;
            z-index: 9999999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: lpuOverlayFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) 1.5s forwards;
            pointer-events: none;
        }

        .lpu-loader-container {
            position: relative;
            width: 140px;
            height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
        }

        .lpu-loader-ring {
            position: absolute;
            inset: -8px;
            border-radius: 50%;
            border: 2px solid transparent;
            border-top: 2px solid #FF6A00;
            border-right: 2px solid #CC4B00;
            animation: lpuRingRotate 1.2s linear infinite;
            filter: drop-shadow(0 0 10px rgba(255, 106, 0, 0.7));
        }

        .lpu-loader-logo {
            width: 110px;
            height: 110px;
            object-fit: contain;
            animation: lpuLogoPulse 2s ease-in-out infinite;
        }

        .lpu-loader-text {
            color: #FFFFFF;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            margin-bottom: 12px;
            text-shadow: 0 0 10px rgba(255, 106, 0, 0.5);
        }

        .lpu-loader-bar-bg {
            width: 220px;
            height: 3px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }

        .lpu-loader-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #CC4B00, #FF6A00);
            box-shadow: 0 0 10px #FF6A00;
            border-radius: 4px;
            animation: lpuBarFill 1.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* -------------------------------------------------------------
           6. RESPONSIVE BUILDING HERO BACKGROUND
           ------------------------------------------------------------- */
        .lpu-hero-wrap {
            position: relative;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255, 106, 0, 0.25);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
            margin-bottom: 35px;
        }

        .lpu-hero-bg {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center 30%;
            filter: brightness(0.48) contrast(1.15);
            transform: scale(1.02);
            transition: transform 10s ease;
        }
        .lpu-hero-wrap:hover .lpu-hero-bg {
            transform: scale(1.05);
        }

        .lpu-hero-overlay {
            position: relative;
            z-index: 2;
            padding: 60px 45px;
            background: linear-gradient(
                180deg,
                rgba(8, 8, 8, 0.65) 0%,
                rgba(18, 18, 18, 0.88) 70%,
                #080808 100%
            );
        }

        .lpu-hero-title {
            color: #FFFFFF;
            font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif;
            font-size: 38px;
            font-weight: 800;
            line-height: 1.15;
            margin: 14px 0 16px 0;
            letter-spacing: -0.5px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        }
        .lpu-hero-title span {
            background: linear-gradient(135deg, #FF6A00 0%, #FFA86B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: none;
        }

        .lpu-hero-desc {
            color: #B3B3B3;
            font-size: 15px;
            line-height: 1.7;
            max-width: 820px;
            margin-bottom: 24px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
        }

        @media (max-width: 768px) {
            .lpu-hero-overlay {
                padding: 35px 20px;
            }
            .lpu-hero-title {
                font-size: 26px;
            }
            .lpu-card {
                padding: 16px;
            }
            .nav-pill-wrapper {
                flex-direction: column;
                gap: 12px;
            }
        }

        /* Reduced motion compliance */
        @media (prefers-reduced-motion: reduce) {
            .lpu-loader-overlay, .lpu-loader-ring, .lpu-loader-logo, .lpu-hero-bg {
                animation: none !important;
                transition: none !important;
            }
            .lpu-loader-overlay {
                display: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_centered_loading_screen():
    """Renders the centered LPU Logo opening animation."""
    logo_url = get_lpu_logo_url()
    if not logo_url:
        return

    st.markdown(
        f"""
        <div class="lpu-loader-overlay" id="lpu-loading-screen">
            <div class="lpu-loader-container">
                <div class="lpu-loader-ring"></div>
                <img src="{logo_url}" class="lpu-loader-logo" alt="LPU Logo">
            </div>
            <div class="lpu-loader-text">INITIALIZING SHUTTLELYZE AI</div>
            <div class="lpu-loader-bar-bg">
                <div class="lpu-loader-bar-fill"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_top_banner():
    """Renders the sleek top university status bar."""
    st.markdown(
        """
        <div style="background-color: #080808; border-bottom: 1px solid rgba(255, 106, 0, 0.2); padding: 7px 25px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #B3B3B3; font-family: 'Space Grotesk', sans-serif; letter-spacing: 0.5px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #FF6A00; box-shadow: 0 0 8px #FF6A00;"></span>
                <span style="color: #FFFFFF; font-weight: 600;">LOVELY PROFESSIONAL UNIVERSITY</span>
                <span style="color: #666;">•</span>
                <span>CAMPUS MOBILITY NETWORK</span>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="border: 1px solid rgba(255, 106, 0, 0.3); border-radius: 4px; padding: 2px 8px; color: #FF6A00; font-size: 11px; font-weight: 600;">24/7 SUPPORT: +91 1824-444433</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_cinematic_footer():
    """Renders the sleek dark orange & black university footer."""
    st.markdown(
        """
        <div style="background: #080808; border-top: 1px solid rgba(255, 106, 0, 0.25); margin-top: 50px; padding: 40px 30px 25px 30px; font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px; max-width: 1400px; margin: 0 auto; padding-bottom: 25px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                <div style="flex: 1.5; min-width: 260px;">
                    <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; letter-spacing: 1px; margin-bottom: 10px;">
                        LPU <span style="color: #FF6A00;">SHUTTLELYZE</span>
                    </div>
                    <p style="color: #B3B3B3; font-size: 13px; line-height: 1.7; max-width: 380px;">
                        Next-generation campus transit analytics, AI passenger demand forecasting, and dynamic shuttle routing system for Lovely Professional University.
                    </p>
                </div>
                <div style="flex: 1; min-width: 180px;">
                    <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Transit System</div>
                    <div style="color: #B3B3B3; font-size: 13px; line-height: 2.2;">
                        <div>• Real-time Route Recommendations</div>
                        <div>• Passenger Demand Forecasting</div>
                        <div>• Fleet Resource Allocation</div>
                        <div>• Campus K-Means Clustering</div>
                    </div>
                </div>
                <div style="flex: 1.2; min-width: 220px;">
                    <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Contact Helpline</div>
                    <p style="color: #B3B3B3; font-size: 13px; line-height: 1.7; margin: 0;">
                        <b style="color: #FFFFFF;">Lovely Professional University</b><br>
                        Jalandhar - Delhi, G.T. Road, Phagwara, Punjab 144411<br>
                        Emergency: Ext. 123 (Internal)<br>
                        Email: support@lpu.co.in
                    </p>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; max-width: 1400px; margin: 20px auto 0 auto; font-size: 12px; color: #777777;">
                <div>&copy; 2026 Lovely Professional University. All rights reserved. INT395-CA1-PROJECT.</div>
                <div style="display: flex; gap: 20px;">
                    <span style="color: #B3B3B3;">Privacy Policy</span>
                    <span style="color: #B3B3B3;">Terms of Service</span>
                    <span style="color: #B3B3B3;">Campus Security Protocol</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
