import re

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

    st.markdown(
        """
        <div style="text-align:center; padding:55px 10px 15px;">
            <div style="color:#FF6A00; font-size:13px; font-weight:700;
                        letter-spacing:2px;">SHUTTLELYZE SECURITY</div>
            <h1 style="color:white; margin:8px 0;">Email OTP Login</h1>
            <p style="color:#B3B3B3;">Verify your email to open the SHUTTLELYZE application.</p>
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
