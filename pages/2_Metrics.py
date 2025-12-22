# pages/2_Metrics.py

import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import timedelta

st.set_page_config(page_title="Metrics", layout="wide")

st.title("Initiative Metrics")
st.markdown("Read-only health and attention signals across NEK initiatives.")

# -------------------------
# Supabase connection
# -------------------------
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

@st.cache_data(ttl=60)
def load_initiatives():
    resp = supabase.table("initiatives").select("*").execute()
    df = pd.DataFrame(resp.data or [])

    for col in ["last_check_in", "next_check_in"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df

df_all = load_initiatives()

today = pd.Timestamp.today().normalize()
due_window_days = 14
activeish_statuses = ["Active", "Proposed"]

activeish_df = df_all[df_all["status"].isin(activeish_statuses)]

overdue_df = df_all[
    (df_all["status"].isin(activeish_statuses))
    & (df_all["next_check_in"].notna())
    & (df_all["next_check_in"] < today)
]

due_soon_df = df_all[
    (df_all["status"].isin(activeish_statuses))
    & (df_all["next_check_in"].notna())
    & (df_all["next_check_in"] >= today)
    & (df_all["next_check_in"] <= (today + timedelta(days=due_window_days)))
]

recent_df = df_all[
    (df_all["last_check_in"].notna())
    & (df_all["last_check_in"] >= (today - timedelta(days=30)))
]

# -------------------------
# Metrics Row
# -------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Active / Proposed", len(activeish_df))
c2.metric("Overdue", len(overdue_df))
c3.metric(f"Due Soon ({due_window_days}d)", len(due_soon_df))
c4.metric("Updated (30d)", len(recent_df))

st.divider()

# -------------------------
# Needs Attention
# -------------------------
st.subheader("Needs Attention")

show_due_soon = st.checkbox(
    "Show due-soon items (in addition to overdue)",
    value=True
)

cols_focus = [
    "initiative_name",
    "region",
    "lead_steward",
    "status",
    "next_check_in",
    "last_check_in",
]

if overdue_df.empty and (not show_due_soon or due_soon_df.empty):
    st.info("Nothing urgent right now — no overdue items (and none due soon, if enabled).")
else:
    if not overdue_df.empty:
        st.markdown("**Overdue**")
        st.dataframe(
            overdue_df[cols_focus].sort_values("next_check_in"),
            use_container_width=True,
            hide_index=True,
        )

    if show_due_soon and not due_soon_df.empty:
        st.markdown("**Due Soon**")
        st.dataframe(
            due_soon_df[cols_focus].sort_values("next_check_in"),
            use_container_width=True,
            hide_index=True,
        )
