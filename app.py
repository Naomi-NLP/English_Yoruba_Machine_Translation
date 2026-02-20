import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("📘 English–Yorùbá Glossary Validator")

# -----------------------------
# Config
# -----------------------------
ADMIN_PASSWORD = "143admin78"
GITHUB_URL = "https://raw.githubusercontent.com/<username>/<repo>/main/your_glossary.csv"
WORKING_FILE = "validated_glossary.csv"  # This is your "new CSV container"

# -----------------------------
# 1️⃣ Load CSV (from working copy if exists)
# -----------------------------
if "df" not in st.session_state:
    if os.path.exists(WORKING_FILE):
        st.session_state.df = pd.read_csv(WORKING_FILE)
        st.success(f"✅ Loaded working copy: {WORKING_FILE}")
    else:
        try:
            st.session_state.df = pd.read_csv(GITHUB_URL)
            st.success("✅ Loaded CSV from GitHub")
        except Exception as e:
            st.error(f"Failed to load CSV from GitHub: {e}")
    st.session_state.index = 0

df = st.session_state.df
i = st.session_state.index

# -----------------------------
# 2️⃣ Row-by-row validator
# -----------------------------
st.write(f"### Reviewing entry {i+1} of {len(df)}")
row = df.iloc[i]

col1, col2 = st.columns(2)

with col1:
    sn = st.text_input("S/N", row.get("S/N", ""))
    source = st.text_input("SOURCE", row.get("SOURCE", ""))
    definition = st.text_area("DEFINITION", row.get("DEFINITION", ""), height=150)

with col2:
    yoruba = st.text_input("YORÙBÁ", row.get("YORÙBÁ", ""))
    translation = st.text_area("TRANSLATION", row.get("TRANSLATION", ""), height=150)

# -----------------------------
# 3️⃣ Save changes instantly
# -----------------------------
if st.button("💾 Save Changes"):
    st.session_state.df.loc[i] = [sn, source, definition, yoruba, translation]
    # Save immediately to the new CSV container
    st.session_state.df.to_csv(WORKING_FILE, index=False)
    st.success(f"Saved ✅ — updated CSV stored in {WORKING_FILE}")

# -----------------------------
# 4️⃣ Navigation
# -----------------------------
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("⬅ Previous") and i > 0:
        st.session_state.index -= 1
with col_next:
    if st.button("Next ➡") and i < len(df) - 1:
        st.session_state.index += 1

st.markdown("---")

# -----------------------------
# 5️⃣ Admin-only download
# -----------------------------
st.subheader("🔒 Admin Download")
password = st.text_input("Enter admin password", type="password")

if password == ADMIN_PASSWORD:
    if os.path.exists(WORKING_FILE):
        csv_bytes = open(WORKING_FILE, "rb").read()
        st.download_button(
            "📥 Download Validated CSV",
            csv_bytes,
            WORKING_FILE,
            "text/csv"
        )
        st.success("✅ You are authenticated as admin")
    else:
        st.warning("No validated CSV exists yet.")
elif password:
    st.error("❌ Wrong password")
