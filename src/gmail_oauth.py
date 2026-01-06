import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT_URI = "http://localhost:8501"

def is_logged_in():
    return "gmail_creds" in st.session_state

def gmail_login():
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    st.markdown(f"[🔐 Login with Google]({auth_url})")

    params = st.query_params
    if "code" in params:
        flow.fetch_token(code=params["code"][0])
        st.session_state["gmail_creds"] = flow.credentials
        st.rerun()
