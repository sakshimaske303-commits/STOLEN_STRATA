"""Stolen Strata dashboard (revised analysis, October 2026).  Run:  streamlit run dashboard/app.py"""
import streamlit as st

from style import inject_css

st.set_page_config(page_title="Stolen Strata | Karewa tableland and brick kilns", page_icon="🏔️", layout="wide", initial_sidebar_state="expanded")
inject_css()

PAGES = [
    st.Page("views/home.py", title="Overview", default=True),
    st.Page("views/correction.py", title="The Correction", url_path="correction"),
    st.Page("views/terrace_map.py", title="Terrace Map", url_path="terrace-map"),
    st.Page("views/conversion.py", title="Conversion 2013–2025", url_path="conversion"),
    st.Page("views/accuracy.py", title="Accuracy Sample", url_path="accuracy"),
    st.Page("views/where_when.py", title="Where and When", url_path="where-and-when"),
    st.Page("views/explore_map.py", title="Interactive Map", url_path="map"),
    st.Page("views/limits.py", title="What It Cannot Show", url_path="limits"),
    st.Page("views/methods.py", title="Methods and Data", url_path="methods"),
    st.Page("views/documents.py", title="Paper and Log", url_path="documents"),
]
st.navigation(PAGES).run()
