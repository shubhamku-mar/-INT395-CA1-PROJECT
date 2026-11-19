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
    page_title="News & Alerts - ShuttleLyze",
    page_icon="📢",
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
            <div style="color: #B3B3B3; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Real-Time Transit Broadcasts</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with header_nav:
    nav1, nav2, nav3, nav4, nav5 = st.columns([1.0, 1.3, 1.3, 0.9, 0.9], gap="small", vertical_alignment="center")
    with nav1:
        if st.button("Home", key="news_nav_home", use_container_width=True):
            st.switch_page("app.py")
    with nav2:
        if st.button("Services", key="news_nav_services", use_container_width=True):
            if os.path.exists("pages/Services.py"):
                st.switch_page("pages/Services.py")
    with nav3:
        if st.button("Safety Hub", key="news_nav_safety", use_container_width=True):
            if os.path.exists("pages/Safety.py"):
                st.switch_page("pages/Safety.py")
    with nav4:
        if st.button("About", key="news_nav_about", use_container_width=True):
            if os.path.exists("pages/About.py"):
                st.switch_page("pages/About.py")
    with nav5:
        if st.button("Contact", key="news_nav_contact", use_container_width=True):
            if os.path.exists("pages/Contact.py"):
                st.switch_page("pages/Contact.py")

# 4. Header Section
st.markdown(
    """
    <div style="margin: 15px 0 25px 0; border-bottom: 1px solid rgba(255, 106, 0, 0.25); padding-bottom: 20px;">
        <div class="lpu-pill-badge" style="margin-bottom: 8px;">Live Dispatch Alerts & Fleet Broadcasts</div>
        <h1 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
            News & Real-Time <span style="color: #FF6A00;">Campus Alerts</span>
        </h1>
        <p style="color: #B3B3B3; font-size: 14px; margin: 8px 0 0 0; max-width: 900px; line-height: 1.6;">
            Stay continuously synchronized with official transit operations, schedule revisions for examination periods, weather advisories, fleet modernization updates, and emergency corridor notifications across Lovely Professional University.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. Urgent Live Alert Banner
st.markdown(
    """
    <div class="lpu-card" style="border-left: 4px solid #FF6A00; background: linear-gradient(135deg, #18120e 0%, #121212 100%); margin-bottom: 25px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #FF6A00; box-shadow: 0 0 10px #FF6A00;"></span>
                <span style="color: #FF6A00; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">ACTIVE ADVISORY</span>
            </div>
            <span style="color: #B3B3B3; font-size: 12px;">Updated: Today • Campus Dispatch</span>
        </div>
        <div style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; margin-bottom: 6px;">
            Extended NightRide Operations for Midterm Exam Week
        </div>
        <p style="color: #B3B3B3; font-size: 13.5px; line-height: 1.6; margin: 0;">
            All NightRide shuttles connecting residential hostels (BH1–BH7, GH1–GH6) and central library facilities in Academic Block 34 will operate continuous loops until 11:30 PM throughout the examination window.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 6. Detailed Announcements List
st.markdown(
    """
    <div style="margin-bottom: 20px;">
        <h2 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; margin: 0 0 6px 0;">
            Operational Bulletins & Transit Updates
        </h2>
        <div style="width: 50px; height: 2px; background: #FF6A00; box-shadow: 0 0 8px #FF6A00; margin-bottom: 15px;"></div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("🚍 FLEET UPGRADE: 10 New Electric Shuttles Deployed on Campus Ring Road"):
    st.write("The LPU Transport Department has introduced 10 high-capacity electric golf carts and low-emission shuttles to reduce morning transit wait times between Block 1 and Block 57 to under 6 minutes.")

with st.expander("⚠️ WEATHER ADVISORY: Reduced Speed Limits During Morning Fog"):
    st.write("Seasonal winter fog advisories are active for early morning routes (7:30 AM – 9:00 AM). Vehicle speeds are electronically capped at 15 km/h for student safety. Please budget an additional 5 minutes for morning travel.")

with st.expander("📢 ROUTE NOTICE: Temporary Infrastructure Diversion Near Polytechnic (Block 57)"):
    st.write("Due to underground fiber-optic cabling and pedestrian promenade enhancement near Block 57, express shuttles are rerouted via Uni-Mall boulevard. Stop locations remain unaffected.")

with st.expander("📅 SPECIAL TIMETABLE: Festival & Cultural Event Schedules"):
    st.write("During university youth festivals and cultural celebrations, high-frequency express loops will connect Sh. Baldev Raj Mittal Auditorium, sports complexes, and Uni-Center every 8 minutes.")

with st.expander("💳 SMART MOBILITY: LPU ID Card Tap-to-Ride Integration"):
    st.write("Automated RFID boarding readers are now operational across all major terminals. Simply tap your registered Student or Faculty Smart Card for swift, ticketless transit.")

# 7. University Footer
render_cinematic_footer()
