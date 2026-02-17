

import streamlit as st

# Sample streamlit code

st.set_page_config(layout = 'wide')

st.title('Project Tile Here')

with st.sidebar:


    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
