import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📘 English–Yorùbá Glossary Validator")

# -----------------------------
# 1️⃣ Admin password (for download)
# -----------------------------
ADMIN_PASSWORD = "143admin78"

# -----------------------------
# 2️⃣ Load CSV from GitHub once
# -----------------------------
GITHUB_URL = "https://raw.githubusercontent.com/Naomi-NLP/Validator/refs/heads/main/hiv_aids_glossary.csv"  # replace with your raw CSV URL

if "df" not in st.session_state:
    try:
        df = pd.read_csv(GITHUB_URL)
        st.session_state.df = df.copy()
        st.session_state.index = 0
        st.success("✅ CSV loaded successfully from GitHub")
    except Exception as e:
        st.error(f"Failed to load CSV from GitHub: {e}")

# -----------------------------
# 3️⃣ Row-by-row validator
# -----------------------------
if "df" in st.session_state:
    df = st.session_state.df
    i = st.session_state.index

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
    # Save changes with form
    # -----------------------------
    with st.form(key="edit_form"):
        submitted = st.form_submit_button("💾 Save Changes")
        if submitted:
            st.session_state.df.loc[i] = [sn, source, definition, yoruba, translation]
            st.success("Saved!")

    # -----------------------------
    # Navigation
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
    # Admin-only download
    # -----------------------------
    st.subheader("🔒 Admin Download")
    password = st.text_input("Enter admin password", type="password")

    if password == ADMIN_PASSWORD:
        csv_bytes = st.session_state.df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Cleaned CSV",
            csv_bytes,
            "validated_glossary.csv",
            "text/csv"
        )
        st.success("✅ You are authenticated as admin")
    elif password:
        st.error("❌ Wrong password")
