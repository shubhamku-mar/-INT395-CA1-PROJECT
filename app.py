import base64
import os
import streamlit as st
import streamlit.components.v1 as components

# Import shared LPU Black & Dark Orange Theme
from assets.frontend_theme import (
    inject_lpu_theme,
    render_centered_loading_screen,
    render_top_banner,
    render_cinematic_footer,
    get_lpu_logo_url,
    get_lpu_campus_url,
)

# 1. Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="ShuttleLyze - LPU Campus Transit AI",
    page_icon="🚌",
    layout="wide"
)

# 2. Inject Black & Dark Orange Theme Styles
inject_lpu_theme()

# 3. Centered LPU Logo Loading Screen (Smooth opening animation)
render_centered_loading_screen()

# 4. Top University Status Bar
render_top_banner()

# 5. Secondary Floating Header Navigation
logo_url = get_lpu_logo_url()
campus_bg_url = get_lpu_campus_url()

header_brand, header_spacer, header_nav = st.columns(
    [3.2, 0.6, 6.2],
    gap="small",
    vertical_alignment="center"
)

with header_brand:
    logo_html = f'<img src="{logo_url}" style="height: 44px; width: 44px; margin-right: 14px; object-fit: contain; filter: drop-shadow(0 0 10px rgba(255,106,0,0.5));" alt="LPU Logo">' if logo_url else ''
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; height: 65px; box-sizing: border-box; padding-left: 10px;">
            {logo_html}
            <div>
                <span style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; letter-spacing: 1.5px; line-height: 1;">
                    SHUTTLE<span style="color: #FF6A00;">LYZE</span>
                </span>
                <div style="color: #B3B3B3; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">LPU Transit Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_nav:
    nav1, nav2, nav3, nav4, nav5 = st.columns(
        [1.3, 1.0, 1.3, 0.9, 0.9],
        gap="small",
        vertical_alignment="center"
    )

    with nav1:
        if st.button("Safety Hub", key="nav_safety", use_container_width=True):
            if os.path.exists("pages/Safety.py"):
                st.switch_page("pages/Safety.py")
            else:
                st.warning("Safety page not found.")

    with nav2:
        if st.button("Services", key="nav_services", use_container_width=True):
            if os.path.exists("pages/Services.py"):
                st.switch_page("pages/Services.py")
            else:
                st.warning("Services page not found.")

    with nav3:
        if st.button("News & Alerts", key="nav_news", use_container_width=True):
            if os.path.exists("pages/News.py"):
                st.switch_page("pages/News.py")
            else:
                st.warning("News page not found.")

    with nav4:
        if st.button("About", key="nav_about", use_container_width=True):
            if os.path.exists("pages/About.py"):
                st.switch_page("pages/About.py")
            else:
                st.warning("About page not found.")

    with nav5:
        if st.button("Contact", key="nav_contact", use_container_width=True):
            if os.path.exists("pages/Contact.py"):
                st.switch_page("pages/Contact.py")
            else:
                st.warning("Contact page not found.")

st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

# 6. Hero Section Showcasing LPU Campus Building
bg_style = f"background-image: url('{campus_bg_url}');" if campus_bg_url else "background-color: #121212;"
st.markdown(
    f"""
    <div class="lpu-hero-wrap">
        <div class="lpu-hero-bg" style="{bg_style}"></div>
        <div class="lpu-hero-overlay">
            <div class="lpu-pill-badge">
                <span style="font-size: 14px;">✦</span> Next-Gen Campus Transit • Lovely Professional University
            </div>
            <h1 class="lpu-hero-title">
                Smart Autonomous Transit &<br>
                <span>Predictive Fleet Intelligence</span>
            </h1>
            <p class="lpu-hero-desc">
                The ShuttleLyze system orchestrates campus transportation at Lovely Professional University using real-time machine learning passenger demand forecasting, dynamic vehicle scheduling, and intelligent road routing across all 47 campus stations.
            </p>
            <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 106, 0, 0.15); border: 1px solid rgba(255, 106, 0, 0.4); padding: 8px 16px; border-radius: 8px; font-size: 13px; color: #FFFFFF; font-weight: 500;">
                    <span style="color: #FF6A00; font-size: 16px;">⚡</span> Real-time AI Demand Prediction
                </div>
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12); padding: 8px 16px; border-radius: 8px; font-size: 13px; color: #B3B3B3;">
                    <span style="color: #FF6A00; font-size: 16px;">📍</span> 47 Campus Blocks Connected
                </div>
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12); padding: 8px 16px; border-radius: 8px; font-size: 13px; color: #B3B3B3;">
                    <span style="color: #FF6A00; font-size: 16px;">🛡️</span> 24/7 NightRide Security
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Quick Action Banner
cta_col1, cta_col2 = st.columns(2, gap="medium")
with cta_col1:
    st.markdown(
        """
        <div class="lpu-card" style="margin-bottom: 0px; border-left: 3px solid #FF6A00;">
            <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Interactive AI Dashboard</div>
            <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">Run Route & Demand Prediction</div>
            <p style="color: #B3B3B3; font-size: 13px; line-height: 1.6; margin-bottom: 15px;">
                Calculate passenger loads, recommended shuttle frequencies, and road routing across any pair of campus blocks in real time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🚀 Open Services & Analytics", key="btn_hero_services", use_container_width=True):
        st.switch_page("pages/Services.py")

with cta_col2:
    st.markdown(
        """
        <div class="lpu-card" style="margin-bottom: 0px; border-left: 3px solid #CC4B00;">
            <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">Campus Safety & Security</div>
            <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">NightRide & Escort Protocol</div>
            <p style="color: #B3B3B3; font-size: 13px; line-height: 1.6; margin-bottom: 15px;">
                Review vehicle CCTV monitoring, emergency alarm triggers, campus escort response desks, and 24/7 hotline resources.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🛡️ View Safety Protocols", key="btn_hero_safety", use_container_width=True):
        st.switch_page("pages/Safety.py")

st.markdown('<div style="height: 35px;"></div>', unsafe_allow_html=True)

# 7. University Route Map Section
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <div class="lpu-pill-badge" style="margin-bottom: 10px;">LPU Campus Transit Map</div>
        <h2 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; margin: 0 0 10px 0;">
            Intra-Campus Shuttle Corridors & Stations
        </h2>
        <div style="width: 60px; height: 2px; background: #FF6A00; margin: 0 auto 12px auto; box-shadow: 0 0 10px #FF6A00;"></div>
        <p style="color: #B3B3B3; font-size: 14px; max-width: 750px; margin: 0 auto; line-height: 1.6;">
            Navigate high-frequency shuttle corridors connecting academic complexes, residential student hostels, dining hubs, and administrative zones.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col_routes, col_map = st.columns([1, 1.25], gap="large")

with col_routes:
    st.markdown(
        """
        <div class="lpu-card" style="height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
                <span style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px;">Core Transit Corridors</span>
                <span style="color: #FF6A00; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">Active Routes</span>
            </div>
            <div style="font-size: 13px; line-height: 2.1;">
                <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 8px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="color: #FFFFFF;">Block 1 ➔ Block 57 Corridor</b>
                        <span style="color: #FF6A00; font-size: 12px; font-weight: 600;">~12 min</span>
                    </div>
                    <span style="color: #B3B3B3; font-size: 12px;">Distance: 1,451.1 m • High Demand</span>
                </div>
                <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 8px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="color: #FFFFFF;">Block 1 ➔ Block 73 Corridor</b>
                        <span style="color: #FF6A00; font-size: 12px; font-weight: 600;">~14 min</span>
                    </div>
                    <span style="color: #B3B3B3; font-size: 12px;">Distance: 1,620.0 m • Peripheral Transit</span>
                </div>
                <div style="border-bottom: 1px solid rgba(255,255,255,0.06); padding: 8px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="color: #FFFFFF;">Block 1 ➔ Block 48 Corridor</b>
                        <span style="color: #FF6A00; font-size: 12px; font-weight: 600;">~9 min</span>
                    </div>
                    <span style="color: #B3B3B3; font-size: 12px;">Distance: 1,180.5 m • Moderate Load</span>
                </div>
                <div style="padding: 8px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="color: #FFFFFF;">Block 1 ➔ Block 25 (CSE Dept)</b>
                        <span style="color: #FF6A00; font-size: 12px; font-weight: 600;">~7 min</span>
                    </div>
                    <span style="color: #B3B3B3; font-size: 12px;">Distance: 885.2 m • Core Campus Hub</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_map:
    st.iframe(
        "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d13715.1798369524!2d75.7001!3d31.2530!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x391a5f5e9c0c0c0d%3A0x7c7c7c7c7c7c7c7c!2sLovely%20Professional%20University!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin",
        height=350,
    )

st.markdown('<div style="height: 35px;"></div>', unsafe_allow_html=True)

# 8. LPU Shuttle FAQ & Transit Schedules
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 25px;">
        <div class="lpu-pill-badge" style="margin-bottom: 10px;">Information & Guidelines</div>
        <h2 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 700; margin: 0 0 10px 0;">
            Frequently Asked Questions & Transit Operations
        </h2>
        <div style="width: 50px; height: 2px; background: #FF6A00; margin: 0 auto; box-shadow: 0 0 8px #FF6A00;"></div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("🕒 Daytime Shuttle Schedule & Frequencies"):
    st.write("Daytime shuttles operate from 8:00 AM to 10:00 PM, Monday through Sunday, with peak dispatch intervals of every 5-10 minutes during morning and evening rush hours.")

with st.expander("🌙 NightRide Shuttle Security Operations"):
    st.write("NightRide shuttles operate after 10:00 PM across all residential hostels and library complexes. Each vehicle is staffed with security-verified operators and real-time GPS tracking.")

with st.expander("📍 Real-time Tracking via LPU Golf Kart App"):
    st.write("Live vehicle GPS locations, estimated arrival times (ETAs), and passenger load indicators can be tracked in real-time through the official LPU Golf Kart Application.")

with st.expander("💬 Passenger Feedback & Route Suggestions"):
    st.write("Feedback can be submitted directly on the ShuttleLyze portal via the Contact page or within the mobile application to help improve route allocation.")

with st.expander("🔍 Lost & Found Protocol"):
    st.write("Items left on campus shuttles are delivered directly to the University Division of Student Affairs (DSA) and can be reported online at ums.lpu.in.")

with st.expander("💳 Identification & Boarding Guidelines"):
    st.write("Passengers must display their valid University Student/Staff ID when boarding university shuttles. Digital verification is integrated at terminal points.")

with st.expander("🚨 Emergency Escort & Alarm Assistance"):
    st.write("Each shuttle is fitted with an emergency panic alarm and continuous CCTV monitoring. For immediate security accompaniment across campus, contact Security Ext. 123.")

# 9. University Footer
render_cinematic_footer()
