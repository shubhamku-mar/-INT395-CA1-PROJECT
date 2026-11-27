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
            width: 100%;
            min-height: 100vh;
            padding: clamp(44px, 8vh, 86px) 1.15rem 2rem;
            background: linear-gradient(160deg, rgba(22, 39, 52, 0.78), rgba(8, 27, 36, 0.82));
            border-left: 1px solid rgba(255,255,255,0.28);
            border-right: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(9px);
            box-shadow: 0 0 55px rgba(0,0,0,0.28);
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stTextInput"] label {{
            color: #f5f5f5 !important;
            font-size: 0.82rem !important;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stTextInput"] input {{
            background: rgba(255,255,255,0.16) !important;
            border: 1px solid rgba(255,255,255,0.48) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            min-height: 42px;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stTextInput"] input::placeholder {{
            color: rgba(255,255,255,0.78) !important;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stButton"] button {{
            min-height: 42px;
            border: 1px solid rgba(255,255,255,0.52) !important;
            border-radius: 8px !important;
            background: rgba(24,25,28,0.66) !important;
            color: #ffffff !important;
        }}
        .st-key-shuttlelyze-login-panel [data-testid="stButton"] button:hover {{
            border-color: #ff914d !important;
            color: #ffb17c !important;
        }}
        @media (max-width: 850px) {{
            [data-testid="stHorizontalBlock"] {{
                min-height: auto;
            }}
            [data-testid="stColumn"]:first-child {{
                display: none !important;
            }}
            .st-key-shuttlelyze-login-panel {{
                width: min(100%, 560px);
                min-height: auto;
                margin: 20px auto !important;
                padding: 1.5rem 1.15rem 1.8rem;
                border: 1px solid rgba(255,255,255,0.25);
                border-radius: 16px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.0, 0.50], gap="small")
    with left_col:
        st.empty()

    with right_col:
        with st.container(key="shuttlelyze-login-panel"):
            st.markdown(
                """
                <div style="text-align:center; margin:0 0 34px;">
                    <div style="
                        border:1px solid rgba(255,255,255,.34);
                        border-radius:8px;
                        padding:14px 5px 24px;
                        box-shadow:0 0 18px rgba(0,0,0,.18);
                        position:relative;">
                        <div style="
                            font-size:clamp(32px,3.1vw,48px);
                            line-height:1.2;
                            font-weight:900;
                            letter-spacing:1px;
                            padding:10px 2px;
                            background:linear-gradient(90deg,#ff8738 0%,#fff1e5 72%);
                            -webkit-background-clip:text;
                            background-clip:text;
                            color:transparent;">
                            SHUTTLELYZE
                        </div>
                    </div>
                    <div style="
                        height:10px;
                        margin:-1px 18px 20px;
                        border-bottom:2px solid rgba(255,255,255,.42);
                        border-radius:0 0 8px 8px;">
                    </div>
                    <h2 style="color:white; margin:0 0 10px; font-size:21px;">
                        Email OTP Login
                    </h2>
                    <p style="color:#E0E4E8; margin:0; font-size:13px; line-height:1.5;">
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
