import streamlit as st
import pickle
import numpy as np
import re
st.set_page_config(page_title="AI Phishing Detector", page_icon="🛡️")
@st.cache_resource
def load_model():
    return pickle.load(open('phishing_model.pkl', 'rb'))

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model file: {e}")

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(url.count('@'))
    features.append(url.count('//'))
    features.append(url.count('/'))
    features.append(1 if url.count('http') > 1 else 0)
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)
    features.append(1 if "bit.ly" in url or "t.co" in url else 0)
    features.append(1 if url.startswith('https') else 0)
    while len(features) < 30:
        features.append(0)
        
    return np.array(features).reshape(1, -1)
st.title("🛡️ AI-Driven Phishing Link Detection")

st.markdown("---")

url_input = st.text_input("Enter the URL to be scanned:", placeholder="e.g., https://google.com")

if st.button("Analyze Now"):
    if url_input:
        with st.spinner('Scrutinizing URL features...'):
            vector = extract_features(url_input)
            prediction = model.predict(vector)
            st.subheader("Results:")
            if prediction[0] == 1:
                st.error(f"❌ **PHISHING DETECTED!**")
                st.write(f"The URL '{url_input}' shows high-risk characteristics.")
            else:
                st.success(f"✔️ **SAFE URL.**")
                st.write(f"No malicious patterns found for '{url_input}'.")
                
            with st.expander("See technical details"):
                st.write(f"Features extracted: {len(vector[0])}")
                st.write(f"Model used: XGBoost Classifier")
    else:
        st.warning("Please enter a URL first.")

st.markdown("---")
st.caption("Disclaimer: This tool is based on heuristic analysis and machine learning for educational purposes.")