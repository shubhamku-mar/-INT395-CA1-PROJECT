import base64
import re
from pathlib import Path

import requests
import streamlit as st


OTP_API_BASE = "https://shuttlelyze-gps-cloud.onrender.com"


def require_app_login():
    """Require a separate email OTP before any SHUTTLELYZE app page loads."""
    if st.session_state.get("shuttlelyze_app_authenticated"):
        if st.sidebar.button("Log out", key="shuttlelyze_app_logout"):
            for key in (
                "shuttlelyze_app_authenticated",
                "shuttlelyze_app_verified_email",
                "shuttlelyze_app_otp_sent",
                "shuttlelyze_app_otp_email",
                "shuttlelyze_app_otp_code",
            ):
                st.session_state.pop(key, None)
            st.rerun()
        return

    background_path = Path(__file__).resolve().parent / "assets" / "lpu_login_background.png"
    background_css = ""
    if background_path.exists():
        background_b64 = base64.b64encode(background_path.read_bytes()).decode("ascii")
        background_css = (
            'url("data:image/png;base64,'
            + background_b64
            + '") center center / cover no-repeat fixed'
        )

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: {background_css if background_css else "linear-gradient(135deg, #27313a, #101820)"} !important;
        }}
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        [data-testid="stMain"] {{
            padding: 0 !important;
            background: transparent !important;
        }}
        [data-testid="stMainBlockContainer"] {{
            max-width: 100% !important;
            width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        [data-testid="stHorizontalBlock"] {{
            min-height: 100vh;
            align-items: stretch !important;
            gap: 0 !important;
        }}
        [data-testid="stColumn"] {{
            padding: 0 !important;
        }}
        .st-key-shuttlelyze-login-panel {{
            box-sizing: border-box;
            position: fixed;
            top: 0;
            right: 0;
            bottom: 0;
            z-index: 10;
            width: clamp(350px, 28.5vw, 455px);
            height: 100vh;
            min-height: 100vh;
            overflow-y: auto;
            padding: clamp(34px, 6vh, 64px) 1.05rem 1.5rem;
            margin: 0 !important;
            background: transparent !important;
            border-left: 1px solid rgba(255,255,255,0.28);
            border-right: 0;
            border-top: 0;
            border-bottom: 0;
            border-radius: 0;
            backdrop-filter: none !important;
            box-shadow: none !important;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stTextInput"] label {{
            color: #000000 !important;
            font-size: 0.86rem !important;
            font-weight: 800 !important;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stTextInput"] input {{
            background: rgba(255,255,255,0.045) !important;
            border: 1px solid rgba(255,145,64,0.58) !important;
            border-radius: 8px !important;
            color: #ff8a24 !important;
            font-weight: 750 !important;
            min-height: 38px;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stTextInput"] input::placeholder {{
            color: #ff9a3d !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stButton"] button {{
            min-height: 42px;
            border: 1px solid rgba(255,255,255,0.52) !important;
            border-radius: 8px !important;
            background: rgba(255,255,255,0.055) !important;
            color: #ff8a24 !important;
            font-weight: 850 !important;
            letter-spacing: .35px;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stButton"] button:hover {{
            border-color: #ff914d !important;
            color: #ffad62 !important;
            background: rgba(255,255,255,0.10) !important;
        }}
        @media (max-width: 850px) {{
            [data-testid="stHorizontalBlock"] {{ min-height: 100vh; }}
            [data-testid="stColumn"]:first-child {{ display: none !important; }}
            .st-key-shuttlelyze-login-panel {{
                position: relative; top: auto; right: auto; bottom: auto;
                width: min(100%, 560px); height: auto; min-height: 100vh;
                margin: 0 auto !important; padding: 2rem 1.15rem;
                border: 1px solid rgba(255,255,255,0.25); border-radius: 0;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.0, 0.42], gap=None)
    with left_col:
        st.empty()

    with right_col:
        with st.container(key="shuttlelyze-login-panel"):
            st.markdown(
                """
                <div style="text-align:center; margin:0 0 24px;">
                    <div style="
                        border:1px solid rgba(255,255,255,.34);
                        border-radius:8px;
                        padding:10px 5px 16px;
                        box-shadow:0 0 18px rgba(0,0,0,.18);
                        position:relative;">
                        <div style="
                            font-size:clamp(28px,2.6vw,40px);
                            line-height:1.2;
                            font-weight:950;
                            letter-spacing:1.6px;
                            text-shadow:0 2px 12px rgba(0,0,0,.28);
                            padding:8px 2px;
                            color:#ff7900;">
                            SHUTTLELYZE
                        </div>
                    </div>
                    <div style="
                        height:10px;
                        margin:-1px 18px 15px;
                        border-bottom:2px solid rgba(255,255,255,.42);
                        border-radius:0 0 8px 8px;">
                    </div>
                    <h2 style="color:#000000; margin:0 0 10px; font-size:22px; font-weight:950; letter-spacing:.2px; text-shadow:0 1px 5px rgba(255,255,255,.55);">
                        Email OTP Login
                    </h2>
                    <p style="color:#000000; margin:0; font-size:13px; line-height:1.5; font-weight:850; text-shadow:0 1px 5px rgba(255,255,255,.55);">
                        Verify your email to open the SHUTTLELYZE application.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            email = st.text_input(
                "Email address",
                key="shuttlelyze_app_login_email",
                placeholder="Enter your email address",
            ).strip().lower()

            if st.button("SEND APPLICATION OTP", use_container_width=True):
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    st.error("Enter a valid email address.")
                else:
                    try:
                        response = requests.post(
                            f"{OTP_API_BASE}/api/app/request-otp",
                            json={"email": email},
                            timeout=25,
                        )
                        result = response.json()
                        if response.ok and result.get("success"):
                            st.session_state["shuttlelyze_app_otp_sent"] = True
                            st.session_state["shuttlelyze_app_otp_email"] = email
                            st.session_state.pop("shuttlelyze_app_otp_code", None)
                            st.success("Application OTP sent. Check your inbox and spam folder.")
                        else:
                            st.error(result.get("error", "Could not send OTP. Please try again."))
                    except requests.RequestException:
                        st.error("Could not connect to the SHUTTLELYZE verification service.")
                    except ValueError:
                        st.error("The verification service returned an invalid response.")

            if st.session_state.get("shuttlelyze_app_otp_sent"):
                if st.session_state.get("shuttlelyze_app_otp_email") != email:
                    st.warning("The email address changed. Send a new OTP to this address.")
                else:
                    otp = st.text_input(
                        "Six-digit application OTP",
                        key="shuttlelyze_app_otp_code",
                        max_chars=6,
                        type="password",
                    ).strip()
                    if st.button("VERIFY & OPEN SHUTTLELYZE", use_container_width=True):
                        if not re.fullmatch(r"\d{6}", otp):
                            st.error("Enter the six-digit OTP.")
                        else:
                            try:
                                response = requests.post(
                                    f"{OTP_API_BASE}/api/app/verify-otp",
                                    json={"email": email, "otp": otp},
                                    timeout=25,
                                )
                                result = response.json()
                                if response.ok and result.get("success"):
                                    st.session_state["shuttlelyze_app_authenticated"] = True
                                    st.session_state["shuttlelyze_app_verified_email"] = email
                                    st.session_state.pop("shuttlelyze_app_otp_sent", None)
                                    st.session_state.pop("shuttlelyze_app_otp_code", None)
                                    st.rerun()
                                else:
                                    st.error(result.get("error", "OTP verification failed."))
                            except requests.RequestException:
                                st.error("Could not connect to the SHUTTLELYZE verification service.")
                            except ValueError:
                                st.error("The verification service returned an invalid response.")

    st.stop()
