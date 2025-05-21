import streamlit as st
import pickle
import socket
from urllib.parse import urlparse
from datetime import datetime
import whois
from feature_extractor import extract_features

# Load model
with open('phishing_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Page config
st.set_page_config(page_title="Phishing Link Detection System", page_icon="🔐")
st.title("🔐 Advanced Phishing Link Detection System")
st.markdown("This system analyzes a URL using machine learning and domain intelligence to detect phishing threats.")

# User input
url = st.text_input("Enter the URL to check:", placeholder="e.g. http://secure-paypal.com.login.verify-account.io")

if url:
    st.markdown("---")
    st.subheader("🔍 Step 1: Basic URL Structure Info")

    parsed = urlparse(url)
    st.write(f"**Full URL:** {url}")
    st.write(f"**Domain:** {parsed.netloc}")
    st.write(f"**Scheme:** {parsed.scheme}")
    st.write(f"**Path:** {parsed.path or '/'}")

    st.markdown("---")
    st.subheader("⚙️ Step 2: Extracted Features")
    features = extract_features(url)
    st.json({
        "URL Length": len(url),
        "Uses HTTPS": "Yes" if "https" in url else "No",
        "Dot Count": url.count('.'),
    })

    st.markdown("---")
    st.subheader("🌐 Step 3: Domain Intelligence")

    try:
        domain_info = whois.whois(parsed.netloc)
        st.write(f"**Registrar:** {domain_info.registrar}")
        st.write(f"**Creation Date:** {domain_info.creation_date}")
        st.write(f"**Expiration Date:** {domain_info.expiration_date}")
        st.write(f"**Country:** {domain_info.country}")
        domain_age = (datetime.now() - domain_info.creation_date[0]).days if isinstance(domain_info.creation_date, list) else (datetime.now() - domain_info.creation_date).days
        st.write(f"**Domain Age:** {domain_age} days")
    except:
        st.warning("Unable to fetch WHOIS data. Domain may be private or malformed.")

    try:
        ip = socket.gethostbyname(parsed.netloc)
        st.write(f"**Resolved IP Address:** {ip}")
    except:
        st.warning("Could not resolve IP address.")

    st.markdown("---")
    st.subheader("📊 Step 4: ML-Based Prediction")

    try:
        prediction = model.predict([features])[0]
        if prediction == 1:
            st.markdown("<div style='background-color:#ffcccc;padding:12px;border-radius:10px;'>"
                        "<h4 style='color:red;'>⚠️ Result: Phishing Website Detected!</h4></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color:#ccffcc;padding:12px;border-radius:10px;'>"
                        "<h4 style='color:green;'>✅ Result: This Website Appears Safe.</h4></div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Prediction failed: {e}")

