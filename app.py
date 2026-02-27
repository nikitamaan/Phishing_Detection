import streamlit as st
import pickle
import numpy as np
st.set_page_config(page_title="AI Phishing Detector")
st.title("🛡AI-Driven Phishing Link Detection")
st.write("Enter a URL below to check if it's safe or a scam.")
url_input = st.text_input("Paste the URL here:")
if st.button("Analyze URL"):
    if url_input:
        st.info(f"Analyzing: {url_input}...")
    else:
        st.warning("Please enter a URL first.")