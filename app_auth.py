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
            [data-testid="stMainBlockContainer"] {{
                width: min(560px, 43vw);
                max-width: 560px;
                margin-left: auto;
                margin-right: clamp(24px, 5vw, 90px);
                margin-top: clamp(24px, 12vh, 110px);
                padding: 1.15rem 1.5rem 1.35rem;
                background: rgba(12, 15, 22, 0.76);
                border: 1px solid rgba(255,255,255,0.18);
                border-radius: 18px;
                backdrop-filter: blur(9px);
                box-shadow: 0 18px 55px rgba(0,0,0,0.35);
            }}
            [data-testid="stMainBlockContainer"] h1 {{
                font-size: clamp(1.65rem, 2.2vw, 2.1rem);
            }}
            @media (max-width: 900px) {{
                [data-testid="stMainBlockContainer"] {{
                    width: min(620px, calc(100vw - 32px));
                    margin: 24px auto;
                    padding: 1.1rem 1.2rem 1.3rem;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="text-align:center; padding:8px 6px 8px;">
            <div style="color:#FF6A00; font-size:13px; font-weight:700;
                        letter-spacing:2px;">SHUTTLELYZE SECURITY</div>
            <h1 style="color:white; margin:6px 0; font-size:30px;">Email OTP Login</h1>
            <p style="color:#D0D0D0; margin:4px 0 8px;">Verify your email to open the SHUTTLELYZE application.</p>
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
