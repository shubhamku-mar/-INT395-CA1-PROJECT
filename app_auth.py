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


    # Full-screen LPU campus background for the application OTP screen.
    background_path = Path(__file__).resolve().parent / "assets" / "lpu_login_background.png"
    if background_path.exists():
        background_b64 = base64.b64encode(background_path.read_bytes()).decode("ascii")
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background:
                    linear-gradient(rgba(10, 12, 18, 0.48), rgba(10, 12, 18, 0.62)),
                    url("data:image/png;base64,{background_b64}") center center / cover fixed;
            }}
            [data-testid="stHeader"] {{ background: transparent; }}
            [data-testid="stMain"] {{ background: transparent; }}
            [data-testid="stMain"] {{
                padding-top: 0 !important;
            }}
            [data-testid="stMainBlockContainer"] {{
                box-sizing: border-box;
                width: min(32.5vw, 480px) !important;
                min-width: 390px;
                max-width: 480px !important;
                min-height: 100vh;
                margin: 0 clamp(18px, 2.5vw, 38px) 0 auto !important;
                padding: 8vh 1.15rem 2rem;
                background: linear-gradient(160deg, rgba(13, 27, 39, 0.88), rgba(8, 21, 29, 0.76));
                border-left: 1px solid rgba(255,255,255,0.22);
                border-right: 1px solid rgba(255,255,255,0.16);
                border-radius: 0;
                backdrop-filter: blur(12px);
                box-shadow: 0 0 55px rgba(0,0,0,0.30);
            }}
            [data-testid="stMainBlockContainer"] h1 {{
                font-size: clamp(1.55rem, 2vw, 1.9rem);
            }}
            [data-testid="stMainBlockContainer"] [data-testid="stTextInput"] input {{
                background: rgba(255,255,255,0.13);
                border: 1px solid rgba(255,255,255,0.42);
                border-radius: 8px;
                color: #fff;
            }}
            [data-testid="stMainBlockContainer"] [data-testid="stButton"] button {{
                border: 1px solid rgba(255,255,255,0.5);
                border-radius: 8px;
                background: rgba(24, 25, 28, 0.62);
                color: #fff;
                min-height: 40px;
            }}
            [data-testid="stMainBlockContainer"] [data-testid="stButton"] button:hover {{
                border-color: #ff8a3d;
                color: #ffb17c;
            }}
            @media (max-width: 900px) {{
                [data-testid="stMainBlockContainer"] {{
                    width: min(620px, calc(100vw - 28px)) !important;
                    min-width: 0;
                    min-height: auto;
                    margin: 18px auto !important;
                    padding: 1.5rem 1.2rem 1.8rem;
                    border: 1px solid rgba(255,255,255,0.2);
                    border-radius: 18px;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="text-align:center; margin:0 0 34px; padding:4px 0 24px; border:1px solid rgba(255,255,255,.30); border-radius:8px; box-shadow:0 0 18px rgba(0,0,0,.18);">
            <div style="font-size:clamp(34px,3.3vw,48px); line-height:1.2; font-weight:900; letter-spacing:1px; padding:18px 4px; background:linear-gradient(90deg,#ff8738 0%,#fff1e5 72%); -webkit-background-clip:text; background-clip:text; color:transparent;">SHUTTLELYZE</div>
        </div>
        <div style="height:8px; margin:-35px 16px 22px; border-bottom:2px solid rgba(255,255,255,.38); border-radius:0 0 8px 8px;"></div>
        <div style="text-align:center; padding:0 4px 12px;">
            <h2 style="color:white; margin:0 0 10px; font-size:21px;">Email OTP Login</h2>
            <p style="color:#E0E4E8; margin:0; font-size:13px;">Verify your email to open the SHUTTLELYZE application.</p>
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
