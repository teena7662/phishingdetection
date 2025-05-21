
import streamlit as st
import pickle
from feature_extractor import extract_features

st.title("🔒 Phishing Website Detector")

url = st.text_input("Enter a URL")

if url:
    try:
        with open('phishing_model.pkl', 'rb') as file:
            model = pickle.load(file)
        features = extract_features(url)
        prediction = model.predict([features])[0]
        if prediction == 1:
            st.error("Warning: This is a Phishing URL!")
        else:
            st.success("This URL is Safe.")
    except Exception as e:
        st.error(f"Model loading or prediction failed: {e}")
