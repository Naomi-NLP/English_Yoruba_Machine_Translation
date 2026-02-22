import streamlit as st
import pandas as pd
import os

# -----------------------------
# CONFIG
# -----------------------------
USERNAME = "admin"
PASSWORD = "143admin78"
GITHUB_URL = "https://raw.githubusercontent.com/Naomi-NLP/Validator/refs/heads/main/hiv_aids_glossary.csv"
VALIDATED_FILE = "validated_container.csv"

st.set_page_config(layout="wide")
st.title("📘 English–Yorùbá Glossary Validator")

# -----------------------------
# 1️⃣ LOGIN
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()  # ✅ Force clean rerun after login
        else:
            st.error("❌ Wrong username or password")

else:
    st.success("✅ Logged in as admin")

    # -----------------------------
    # 2️⃣ Load datasets
    # -----------------------------
    if "original_df" not in st.session_state:
        st.session_state.original_df = pd.read_csv(GITHUB_URL)
    original_df = st.session_state.original_df

    if os.path.exists(VALIDATED_FILE):
        validated_df = pd.read_csv(VALIDATED_FILE)
    else:
        validated_df = pd.DataFrame(columns=original_df.columns)
    st.session_state.validated_df = validated_df

    # -----------------------------
    # 3️⃣ Track current row index
    # -----------------------------
    if "current_index" not in st.session_state:
        validated_indices = validated_df['S/N'].astype(str).tolist()
        unvalidated_df = original_df[~original_df['S/N'].astype(str).isin(validated_indices)]
        st.session_state.current_index = unvalidated_df.index[0] if len(unvalidated_df) > 0 else None

    # -----------------------------
    # 4️⃣ Helper: load row into session state form fields
    # -----------------------------
    def load_row_into_state(index):
        sn_current = str(original_df.loc[index, "S/N"])
        existing_row = st.session_state.validated_df[
            st.session_state.validated_df['S/N'].astype(str) == sn_current
        ]
        row = existing_row.iloc[0] if not existing_row.empty else original_df.loc[index]
        st.session_state.form_sn = str(row.get("S/N", ""))
        st.session_state.form_source = str(row.get("SOURCE", ""))
        st.session_state.form_definition = str(row.get("DEFINITION", ""))
        st.session_state.form_yoruba = str(row.get("YORÙBÁ", ""))
        st.session_state.form_translation = str(row.get("TRANSLATION", ""))

    # Load form fields if not already loaded for current index
    if "form_sn" not in st.session_state and st.session_state.current_index is not None:
        load_row_into_state(st.session_state.current_index)

    # -----------------------------
    # 5️⃣ Show current row
    # -----------------------------
    if st.session_state.current_index is None:
        st.success("🎉 All rows validated!")
    else:
        # Progress indicator
        total = len(original_df)
        done = len(st.session_state.validated_df)
        st.progress(done / total, text=f"Validated: {done} / {total}")

        col1, col2 = st.columns(2)
        with col1:
            sn = st.text_input("S/N", value=st.session_state.get("form_sn", ""), key="field_sn")
            source = st.text_input("SOURCE", value=st.session_state.get("form_source", ""), key="field_source")
            definition = st.text_area("DEFINITION", value=st.session_state.get("form_definition", ""), height=150, key="field_definition")
        with col2:
            yoruba = st.text_input("YORÙBÁ", value=st.session_state.get("form_yoruba", ""), key="field_yoruba")
            translation = st.text_area("TRANSLATION", value=st.session_state.get("form_translation", ""), height=150, key="field_translation")

        # -----------------------------
        # 6️⃣ Save validated row
        # -----------------------------
        if st.button("💾 Save this row"):
            new_row = pd.DataFrame([{
                "S/N": st.session_state.field_sn,
                "SOURCE": st.session_state.field_source,
                "DEFINITION": st.session_state.field_definition,
                "YORÙBÁ": st.session_state.field_yoruba,
                "TRANSLATION": st.session_state.field_translation
            }])

            sn_val = str(st.session_state.field_sn)
            existing_index = st.session_state.validated_df.index[
                st.session_state.validated_df['S/N'].astype(str) == sn_val
            ].tolist()

            if existing_index:
                st.session_state.validated_df.loc[existing_index[0]] = new_row.iloc[0]
            else:
                st.session_state.validated_df = pd.concat(
                    [st.session_state.validated_df, new_row], ignore_index=True
                )

            st.session_state.validated_df.to_csv(VALIDATED_FILE, index=False)
            st.success(f"✅ Row {sn_val} saved!")

            # Move to next unvalidated row
            validated_indices = st.session_state.validated_df['S/N'].astype(str).tolist()
            unvalidated_df = original_df[~original_df['S/N'].astype(str).isin(validated_indices)]
            if len(unvalidated_df) > 0:
                st.session_state.current_index = unvalidated_df.index[0]
                load_row_into_state(st.session_state.current_index)  # ✅ Load next row immediately
            else:
                st.session_state.current_index = None

            st.rerun()  # ✅ Force clean rerun

        # -----------------------------
        # 7️⃣ Navigation buttons
        # -----------------------------
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅ Previous"):
                prev_indices = original_df.index[original_df.index < st.session_state.current_index].tolist()
                if prev_indices:
                    st.session_state.current_index = prev_indices[-1]
                    load_row_into_state(st.session_state.current_index)  # ✅ Load row into state
                    st.rerun()  # ✅ Force clean rerun
        with col_next:
            if st.button("Next ➡"):
                next_indices = original_df.index[original_df.index > st.session_state.current_index].tolist()
                if next_indices:
                    st.session_state.current_index = next_indices[0]
                    load_row_into_state(st.session_state.current_index)  # ✅ Load row into state
                    st.rerun()  # ✅ Force clean rerun

    # -----------------------------
    # 8️⃣ Admin-only download
    # -----------------------------
    st.divider()
    st.subheader("🔒 Admin Download")
    password = st.text_input("Enter admin password for download", type="password", key="dl_password")
    if password == PASSWORD:
        if os.path.exists(VALIDATED_FILE):
            csv_bytes = open(VALIDATED_FILE, "rb").read()
            st.download_button("📥 Download Validated Container", csv_bytes, VALIDATED_FILE, "text/csv")
            st.success("✅ You are authenticated as admin")
        else:
            st.warning("No validated CSV exists yet.")
    elif password:
        st.error("❌ Wrong password")
