import pandas as pd
import streamlit as st


st.title("NEK Initiative Registry")

st.markdown(
    """
The NEK Initiative Registry is a simple, shared list of initiatives happening across the region.
It is meant to help residents, partners, and stewards understand what work is underway, who is leading it,
and when it was last checked in.

This page uses sample, in-memory data only.
"""
)

records = [
    {
        "Initiative Name": "Main Street Winter Walkability",
        "Description": "Improve winter sidewalk access and maintenance guidance for downtown routes.",
        "Region": "St. Johnsbury",
        "Status": "Active",
        "Lead Steward": "Town Public Works",
        "Last Check-in": "2025-12-05",
    },
    {
        "Initiative Name": "NEK Local Food Mapping",
        "Description": "Create a shared map of producers, markets, and aggregation points.",
        "Region": "Northeast Kingdom",
        "Status": "Proposed",
        "Lead Steward": "Regional Food Coalition",
        "Last Check-in": "2025-11-18",
    },
    {
        "Initiative Name": "Downtown Vacancy Snapshot",
        "Description": "Track storefront vacancies monthly to support targeted revitalization efforts.",
        "Region": "Newport",
        "Status": "Paused",
        "Lead Steward": "City Planning",
        "Last Check-in": "2025-10-22",
    },
    {
        "Initiative Name": "Community Solar Outreach",
        "Description": "Coordinate outreach sessions for enrollment in community solar programs.",
        "Region": "Hardwick",
        "Status": "Completed",
        "Lead Steward": "Energy Committee",
        "Last Check-in": "2025-09-30",
    },
]

df = pd.DataFrame.from_records(records)

status_options = ["All", "Proposed", "Active", "Paused", "Completed"]
selected_status = st.selectbox("Filter by Status", options=status_options, index=0)

filtered_df = df if selected_status == "All" else df[df["Status"] == selected_status]

st.dataframe(filtered_df, use_container_width=True, hide_index=True)
