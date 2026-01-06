import streamlit as st
import pandas as pd

from src.gmail_oauth import gmail_login, is_logged_in
from src.gmail_fetcher import fetch_latest_emails
from src.predict import EmailPriorityModel
from src.action_extractor import extract_actions
from src.utils import clean_text_basic

st.set_page_config(page_title="Smart Email Priority Sorter", layout="wide")
st.title("📧 Nextra")

# ===============================
# LOGIN SECTION
# ===============================
if not is_logged_in():
    st.warning("🔐 Please login with Google to access Gmail")
    gmail_login()
    st.stop()

# ===============================
# LOAD MODEL
# ===============================
model = EmailPriorityModel()

# ===============================
# FETCH EMAILS
# ===============================
st.sidebar.header("Gmail Settings")
n_email = st.sidebar.slider("Number of emails", 5, 50, 10)

if st.sidebar.button("📥 Fetch Gmail"):
    emails = fetch_latest_emails(n=n_email)
    st.session_state["emails"] = emails

if "emails" not in st.session_state:
    st.info("Click **Fetch Gmail** to load emails")
    st.stop()

df = pd.DataFrame(st.session_state["emails"])

# ===============================
# PREDICTION
# ===============================
preds, probs = model.predict_batch(df)
df["pred_priority"] = preds
df["pred_confidence"] = probs
df["action"] = ""
df["deadline"] = ""

for i, r in df.iterrows():
    acts = extract_actions(clean_text_basic(r["subject"] + " " + r["body"]))
    df.at[i, "action"] = acts["action"]
    df.at[i, "deadline"] = acts["deadline"]

# ===============================
# DISPLAY
# ===============================
cols = st.columns(3)
prio_map = {
    "high": "🔴 Urgent",
    "medium": "🟡 Important",
    "low": "🟢 Normal"
}

for idx, prio in enumerate(["high", "medium", "low"]):
    with cols[idx]:
        st.subheader(prio_map[prio])
        sub = df[df["pred_priority"] == prio]
        for _, r in sub.iterrows():
            st.markdown(f"**{r.subject}**")
            st.caption(r.from_email)
            if r.action or r.deadline:
                st.write(f"- Action: `{r.action or '-'}` | Deadline: `{r.deadline or '-'}`")
            st.progress(min(max(r.pred_confidence, 0.0), 1.0))
            st.divider()

st.download_button(
    "⬇️ Export CSV",
    df.to_csv(index=False),
    "email_priorities.csv",
    "text/csv"
)
