import streamlit as st
import pickle
import numpy as np
import re
@st.cache_resource
def load_model():
    return pickle.load(open('phishing_model.pkl', 'rb'))

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")

def extract_features(url):
    features = []
    features.append(len(url))             
    features.append(url.count('.'))      
    features.append(url.count('-'))      
    features.append(1 if '@' in url else 0) 
    features.append(url.count('//'))     
    while len(features) < 30:
        features.append(0)
    
    return np.array(features).reshape(1, -1)
st.set_page_config(page_title="AI Phishing Detector", page_icon="🛡️")
st.title("🛡️ AI-Driven Phishing Link Detection")
st.write("A machine learning portal to verify URL safety")

url_input = st.text_input("Enter the URL to be analyzed:", placeholder="https://example.com")

if st.button("Analyze Now"):
    if url_input:
        with st.spinner('Scanning URL patterns'):
            vector = extract_features(url_input)
            prediction = model.predict(vector)
            st.subheader("Verdict:")
            if prediction[0] == 1:
                st.error(f" **PHISHING DETECTED!** '{url_input}' is high-risk.")
            else:
                st.success(f"**SAFE URL.** No malicious patterns found for '{url_input}'.")
    else:
        st.warning("Please enter a URL first")