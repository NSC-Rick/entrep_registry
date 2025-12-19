import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

st.title("NEK Entrepreneurial Initiative Registry")

DATA_PATH = Path("data/initiatives.csv")

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Convert date columns safely
    for col in ["Last Check-In", "Next Check-In"]:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    return df

df = load_data()

# Initialize session state
if "edited_df" not in st.session_state:
    st.session_state.edited_df = df.copy()

# --- Filter ---
status_filter = st.selectbox(
    "Filter by status",
    ["All", "Proposed", "Active", "Paused", "Completed"]
)

display_df = st.session_state.edited_df
if status_filter != "All":
    display_df = display_df[display_df["Status"] == status_filter]

# --- Editable table ---
edited = st.data_editor(
    display_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            options=["Proposed", "Active", "Paused", "Completed"]
        ),
        "Last Check-In": st.column_config.DateColumn(),
        "Next Check-In": st.column_config.DateColumn(),
        "Notes": st.column_config.TextColumn(),
    }
)

# --- Save button ---
if st.button("Save changes"):
    # Update session state
    st.session_state.edited_df.update(edited)

    # Write to CSV
    st.session_state.edited_df.to_csv(DATA_PATH, index=False)

    # Clear cache so reload picks up new data
    load_data.clear()

    st.success("Changes saved successfully.")
