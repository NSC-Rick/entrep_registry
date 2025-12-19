import streamlit as st


st.set_page_config(
    page_title="NEK Entrepreneurial Registry Portal",
    layout="wide",
)

st.title("NEK Registry")

st.markdown(
    """
This is a working prototype of a regional registry portal built with Streamlit.

What this prototype includes:
- Simple, readable pages
- In-memory sample data (where applicable)

What this prototype intentionally excludes:
- Authentication
- Database or persistent storage
- External APIs or integrations
"""
)
