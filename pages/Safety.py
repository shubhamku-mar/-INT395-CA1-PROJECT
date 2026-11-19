import os
import streamlit as st
import streamlit.components.v1 as components

from assets.frontend_theme import (
    inject_lpu_theme,
    render_top_banner,
    render_cinematic_footer,
    get_lpu_logo_url,
)

# 1. Page Configuration
st.set_page_config(
    page_title="Campus Safety & Security - ShuttleLyze",
    page_icon="🛡️",
    layout="wide"
)

# 2. Inject Black & Dark Orange Theme
inject_lpu_theme()
render_top_banner()

# 3. Floating Header Navigation Bar
logo_url = get_lpu_logo_url()
header_brand, header_spacer, header_nav = st.columns([3.2, 0.6, 6.2], gap="small", vertical_alignment="center")

with header_brand:
    logo_html = f'<img src="{logo_url}" style="height: 44px; width: 44px; margin-right: 14px; object-fit: contain; filter: drop-shadow(0 0 10px rgba(255,106,0,0.5));" alt="LPU Logo">' if logo_url else ''
    st.markdown(f'''
    <div style="display: flex; align-items: center; height: 65px; box-sizing: border-box; padding-left: 10px;">
        {logo_html}
        <div>
            <span style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; letter-spacing: 1.5px; line-height: 1;">
                SHUTTLE<span style="color: #FF6A00;">LYZE</span>
            </span>
            <div style="color: #B3B3B3; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Campus Safety & Security</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with header_nav:
    nav1, nav2, nav3, nav4, nav5 = st.columns([1.0, 1.3, 1.3, 0.9, 0.9], gap="small", vertical_alignment="center")
    with nav1:
        if st.button("Home", key="safe_nav_home", use_container_width=True):
            st.switch_page("app.py")
    with nav2:
        if st.button("Services", key="safe_nav_services", use_container_width=True):
            if os.path.exists("pages/Services.py"):
                st.switch_page("pages/Services.py")
    with nav3:
        if st.button("News & Alerts", key="safe_nav_news", use_container_width=True):
            if os.path.exists("pages/News.py"):
                st.switch_page("pages/News.py")
    with nav4:
        if st.button("About", key="safe_nav_about", use_container_width=True):
            if os.path.exists("pages/About.py"):
                st.switch_page("pages/About.py")
    with nav5:
        if st.button("Contact", key="safe_nav_contact", use_container_width=True):
            if os.path.exists("pages/Contact.py"):
                st.switch_page("pages/Contact.py")

# 4. Hero Section Header
st.markdown(
    """
    <div style="margin: 15px 0 25px 0; border-bottom: 1px solid rgba(255, 106, 0, 0.25); padding-bottom: 20px;">
        <div class="lpu-pill-badge" style="margin-bottom: 8px;">24/7 Security Operations & Vigilance</div>
        <h1 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
            Campus Safety & <span style="color: #FF6A00;">Security Protocols</span>
        </h1>
        <p style="color: #B3B3B3; font-size: 14px; margin: 8px 0 0 0; max-width: 900px; line-height: 1.6;">
            The safety and well-being of all students, faculty, and campus visitors is the paramount mission of Lovely Professional University. The Department of Campus Safety & Security deploys comprehensive multi-tier protocols ensuring safe transit across every corner of the campus day and night.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Emergency SOS Fast Cards
sos1, sos2, sos3 = st.columns(3, gap="medium")
with sos1:
    st.markdown(
        """
        <div class="lpu-card" style="border-left: 3px solid #FF6A00; min-height: 140px;">
            <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Immediate Helpline</div>
            <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; margin-bottom: 6px;">+91 1824-444433</div>
            <p style="color: #B3B3B3; font-size: 12.5px; line-height: 1.5; margin: 0;">24/7 Control Room hotline for immediate medical, security, and transit emergencies.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with sos2:
    st.markdown(
        """
        <div class="lpu-card" style="border-left: 3px solid #CC4B00; min-height: 140px;">
            <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Internal Campus Phone</div>
            <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; margin-bottom: 6px;">Extension 123</div>
            <p style="color: #B3B3B3; font-size: 12.5px; line-height: 1.5; margin: 0;">Direct speed-dial from any intercom station across academic blocks and residential hostels.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with sos3:
    st.markdown(
        """
        <div class="lpu-card" style="border-left: 3px solid #FF6A00; min-height: 140px;">
            <div style="color: #FF6A00; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">NightRide Security Escorts</div>
            <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; margin-bottom: 6px;">10:00 PM – 5:00 AM</div>
            <p style="color: #B3B3B3; font-size: 12.5px; line-height: 1.5; margin: 0;">Dedicated security accompanied transit between central library, hostels, and medical centers.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# 6. Key Strategies Section
st.markdown(
    """
    <div style="margin-bottom: 20px;">
        <h2 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; margin: 0 0 6px 0;">
            Key Security Strategies & Protocols
        </h2>
        <div style="width: 50px; height: 2px; background: #FF6A00; box-shadow: 0 0 8px #FF6A00; margin-bottom: 15px;"></div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("🛡️ LPU Campus Security Department Operations"):
    st.write("LPU Campus Security operates 24/7 with motorized patrol units securing academic blocks, hostel corridors, open plazas, and perimeters. Response teams maintain a sub-3 minute response time to all logged distress signals.")

with st.expander("🌐 Campus and Neighborhood Perimeter Surveillance"):
    st.write("Comprehensive round-the-clock monitoring includes 100% automated number-plate recognition (ANPR) at entry gates, fixed CCTV surveillance across 47 campus blocks, and active coordination with Phagwara Police.")

with st.expander("🚌 Safe Shuttle Transit & CCTV In-Cabin Verification"):
    st.write("All ShuttleLyze Daytime and NightRide vehicles are equipped with emergency alarm switches, high-definition GPS telemetry, verified driver IDs, and constant radio communication with the central dispatch hub.")

with st.expander("📡 Blue-Light Emergency Towers & Campus Technology"):
    st.write("Emergency blue-light telephone towers positioned at 100-meter intervals along major campus walkways provide one-touch instant voice connection and automatic video tracking to the security control desk.")

with st.expander("🚨 Transparent Incident Reporting & SMS Alerts"):
    st.write("Students receive instant emergency broadcast SMS notifications for severe weather or traffic diversions, and can file anonymous safety or lost item reports directly through the University UMS portal.")

with st.expander("🤝 Community Safety Collaboration & Student Escorts"):
    st.write("Active joint student-faculty safety councils regularly inspect street lighting, review shuttle timing, and provide self-defense workshops and late-night escort groups.")

with st.expander("📞 Emergency Support Resources Directory"):
    st.write("Direct 24/7 access to campus ambulances (+91 1824-444433), Uni-Hospital medical triage, women's safety helplines, and psychological counseling services at the Division of Student Affairs.")

# 7. University Footer
render_cinematic_footer()
