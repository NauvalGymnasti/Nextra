import base64
import streamlit as st
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

def fetch_latest_emails(n=10):
    creds = st.session_state["gmail_creds"]
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me",
        maxResults=n,
        q="newer_than:7d"
    ).execute()

    msgs = results.get("messages", [])
    emails = []

    for m in msgs:
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="full"
        ).execute()

        headers = {h["name"].lower(): h["value"] for h in msg["payload"]["headers"]}
        subject = headers.get("subject", "(no subject)")
        sender = headers.get("from", "unknown")

        def extract_text(payload):
            if "parts" in payload:
                for p in payload["parts"]:
                    t = extract_text(p)
                    if t:
                        return t
            data = payload.get("body", {}).get("data")
            if data:
                raw = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                return BeautifulSoup(raw, "html.parser").get_text(" ", strip=True)
            return ""

        body = extract_text(msg["payload"])
        emails.append({
            "from_email": sender,
            "subject": subject,
            "body": body
        })

    return emails
