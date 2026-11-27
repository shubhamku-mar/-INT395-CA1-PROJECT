import os
import streamlit as st
from app_auth import require_app_login
import streamlit.components.v1 as components

from assets.frontend_theme import (
    inject_lpu_theme,
    render_top_banner,
    render_cinematic_footer,
    get_lpu_logo_url,
)

# 1. Page Configuration
st.set_page_config(
    page_title="Contact Support - ShuttleLyze",
    page_icon="✉️",
    layout="wide"
)

# Require separate email OTP before opening this application page.
require_app_login()

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
            <div style="color: #B3B3B3; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Helpdesk & Passenger Inquiries</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with header_nav:
    nav1, nav2, nav3, nav4, nav5 = st.columns([1.0, 1.3, 1.3, 0.9, 0.9], gap="small", vertical_alignment="center")
    with nav1:
        if st.button("Home", key="cnt_nav_home", use_container_width=True):
            st.switch_page("app.py")
    with nav2:
        if st.button("Services", key="cnt_nav_services", use_container_width=True):
            if os.path.exists("pages/Services.py"):
                st.switch_page("pages/Services.py")
    with nav3:
        if st.button("Safety Hub", key="cnt_nav_safety", use_container_width=True):
            if os.path.exists("pages/Safety.py"):
                st.switch_page("pages/Safety.py")
    with nav4:
        if st.button("News & Alerts", key="cnt_nav_news", use_container_width=True):
            if os.path.exists("pages/News.py"):
                st.switch_page("pages/News.py")
    with nav5:
        if st.button("About", key="cnt_nav_about", use_container_width=True):
            if os.path.exists("pages/About.py"):
                st.switch_page("pages/About.py")

# 4. Header Section
st.markdown(
    """
    <div style="margin: 15px 0 25px 0; border-bottom: 1px solid rgba(255, 106, 0, 0.25); padding-bottom: 20px;">
        <div class="lpu-pill-badge" style="margin-bottom: 8px;">24/7 University Mobility Assistance</div>
        <h1 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
            Support Desk & <span style="color: #FF6A00;">Inquiry Terminal</span>
        </h1>
        <p style="color: #B3B3B3; font-size: 14px; margin: 8px 0 0 0; max-width: 900px; line-height: 1.6;">
            Have questions regarding campus shuttle schedules, lost and found belongings, accessibility requests, or transport route feedback? Submit an official ticket directly to the LPU ShuttleLyze Support Desk or reach out through our dedicated hotline channels.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Fast Contact Channels
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(
        """
        <div class="lpu-card" style="border-left: 3px solid #FF6A00; min-height: 130px;">
            <div style="color: #FF6A00; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Phone Helpline</div>
            <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; margin-bottom: 4px;">+91 1824-444433</div>
            <span style="color: #B3B3B3; font-size: 12px;">Ext: 123 (Campus Intercom)</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        """
        <div class="lpu-card" style="border-left: 3px solid #CC4B00; min-height: 130px;">
            <div style="color: #FF6A00; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Official Email</div>
            <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; margin-bottom: 4px;">support@lpu.co.in</div>
            <span style="color: #B3B3B3; font-size: 12px;">Responses within 24 operational hours</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        """
        <div class="lpu-card" style="border-left: 3px solid #FF6A00; min-height: 130px;">
            <div style="color: #FF6A00; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Campus Helpdesk</div>
            <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; margin-bottom: 4px;">Division of Student Affairs</div>
            <span style="color: #B3B3B3; font-size: 12px;">Block 13, Ground Floor</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

# 6. Contact Form
_, form_col, _ = st.columns([0.1, 1.8, 0.1])

with form_col:
    with st.form("contact_form"):
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 20px;">
                <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 19px; font-weight: 700;">
                    Dispatch Support Ticket
                </div>
                <span class="lpu-pill-badge">Official Portal</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            user_name = st.text_input("Your Full Name", placeholder="e.g. Student Name")
            student_id = st.text_input("Registration / Student ID", placeholder="e.g. 12215000")
        with col2:
            user_email = st.text_input("University Email Address", placeholder="e.g. name@lpu.in")
            support_category = st.selectbox("Inquiry Category", ["Shuttle Schedule & Timing", "Lost & Found Item", "Route Optimization Feedback", "Safety & Security Concern", "General Support"])

        subject_line = st.text_input("Subject", placeholder="Brief summary of your inquiry...")
        message_body = st.text_area("Message / Details", placeholder="Type your message, query, or feedback here...", height=140)

        submitted = st.form_submit_button("🚀 Submit Support Ticket", use_container_width=True)

        if submitted:
            if user_name and user_email and message_body:
                st.success(f"✓ Thank you, {user_name}! Your support ticket has been received and logged under Ticket #{abs(hash(user_email)) % 100000:05d}. Our transit dispatch team will follow up at {user_email}.")
            else:
                st.warning("Please fill in all required fields (Name, Email, and Message) before submitting.")

# 7. University Footer
render_cinematic_footer()
