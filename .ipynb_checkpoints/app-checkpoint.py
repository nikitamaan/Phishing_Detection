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
    st.error(f"Error loading model: {e}")

def extract_features(url):
    features = []
    
    features.append(len(url))
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(url.count('@'))
    features.append(url.count('//'))
    features.append(url.count('/'))
    features.append(1 if url.count('http') > 1 else -1)
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else -1)
    features.append(1 if "bit.ly" in url or "t.co" in url or "tinyurl" in url else -1)
    features.append(-1 if url.startswith('https') else 1)

    features.append(1 if len(url) > 75 else -1)
    features.append(1 if url.count('?') > 0 else -1)
    features.append(1 if url.count('=') > 0 else -1)
    features.append(1 if "login" in url.lower() or "verify" in url.lower() else -1)
    features.append(1 if "admin" in url.lower() or "bank" in url.lower() else -1)
    
    while len(features) < 30:
        features.append(-1) 
        
    return np.array(features).reshape(1, -1)

st.title("🛡️ AI-Driven Phishing Link Detection")
st.write("Enter a URL below to check if it is safe or a phishing attempt.")
st.markdown("---")

url_input = st.text_input("URL to Analyze:", placeholder="https://www.amazon.in")

if st.button("Analyze Now"):
    if url_input:
        with st.spinner('Analyzing...'):
            vector = extract_features(url_input)
            prediction = model.predict(vector)
            
            st.subheader("Verdict:")
            if prediction[0] == 1:
                st.error(f"❌ **PHISHING DETECTED!** The URL shows malicious patterns.")
            else:
                st.success(f"✔️ **SAFE URL.** This website appears legitimate.")
                
            with st.expander("Technical Details"):
                st.write(f"Processed URL: {url_input}")
                st.write("Model: XGBoost Classifier")
                st.write(f"Features used: {len(vector[0])}")
    else:
        st.warning("Please enter a URL first.")