import os
import re

import streamlit as st

from lib import ROOT, picture
from style import page_title

page_title("Paper and Log", "The full text, as it stands in the repository")
DOCS = {"Executive summary": "SS_Executive_Summary.md", "Research paper": "SS_Research_Paper.md", "Development log": "SS_Development_Log.md"}
choice = st.radio("Document", list(DOCS), horizontal=True, label_visibility="collapsed")
path = os.path.join(ROOT, DOCS[choice])
if choice == "Development log":
    st.info("The log is a day-by-day record written while the work was being done. Shown here from Entry 16, where the rebuild and the correction begin.")
if not os.path.exists(path):
    st.warning("This document is not available in this deployment.")
    st.stop()
text = open(path, encoding="utf-8").read()
if choice == "Development log" and "## Entry 16" in text:
    # show the rebuild only; the first-version entries (1-15) stay in the repository file
    text = "\n".join(l for l in text.split("## Index", 1)[0].splitlines() if l.startswith(("#", ">")) or not l.strip()) + "\n\n" + "*Entries 1–15, which describe the withdrawn first version, are in `SS_Development_Log.md` in the repository.*\n\n" + "## Entry 16" + text.split("## Entry 16", 1)[1]
IMG = re.compile(r"!\[(.*?)\]\((.*?)\)")
pos = 0
for m in IMG.finditer(text):
    if text[pos:m.start()].strip():
        st.markdown(text[pos:m.start()])
    src = os.path.join(ROOT, m.group(2))
    if os.path.exists(src):
        picture(src, caption=m.group(1))
    else:
        st.caption(m.group(1))
    pos = m.end()
if text[pos:].strip():
    st.markdown(text[pos:])
