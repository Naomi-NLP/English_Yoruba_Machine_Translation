import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📘 English–Yorùbá Glossary Validator")

# -----------------------------
# 1️⃣ Load CSV from GitHub
# -----------------------------
github_url = st.text_input(
    "Enter GitHub CSV Raw URL",
    "https://raw.githubusercontent.com/<username>/<repo>/main/your_glossary.csv"
)

df = None
if github_url:
    try:
        df = pd.read_csv(github_url)
        st.success("CSV loaded successfully from GitHub ✅")
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")

# -----------------------------
# 2️⃣ Main validator
# -----------------------------
if df is not None:

    if "df" not in st.session_state:
        st.session_state.df = df.copy()
    if "index" not in st.session_state:
        st.session_state.index = 0

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

    # Save changes
    if st.button("💾 Save Changes"):
        st.session_state.df.loc[i] = [sn, source, definition, yoruba, translation]
        st.success("Saved!")

    # Navigation
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅ Previous") and i > 0:
            st.session_state.index -= 1
    with col_next:
        if st.button("Next ➡") and i < len(df) - 1:
            st.session_state.index += 1

    st.markdown("---")
    # Download cleaned CSV
    csv = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Cleaned CSV",
        csv,
        "validated_glossary.csv",
        "text/csv"
    )
