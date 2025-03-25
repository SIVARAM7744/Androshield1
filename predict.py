import streamlit as st
from features import features  # List of permissions used in classification
import pandas as pd
from joblib import load
from androguard.misc import AnalyzeAPK
import os

# Load the trained model
model = load('ML_Model_Final/Random Forest.joblib')

# Define high-risk permissions (only relevant if APK is classified as Malware)
high_risk_permissions = {
    'android.permission.SEND_SMS': 'Send SMS (Potential for premium SMS fraud)',
    'android.permission.RECORD_AUDIO': 'Record Audio (Eavesdropping risk)',
    'android.permission.READ_SMS': 'Read SMS (Privacy risk)',
    'android.permission.CALL_PHONE': 'Call Phone (Unauthorized calls)',
    'android.permission.INTERNET': 'Internet Access (Data exfiltration)',
    'android.permission.READ_CONTACTS': 'Read Contacts (Stealing user data)',
    'android.permission.ACCESS_FINE_LOCATION': 'Precise Location (Tracking user movements)',
    'android.permission.WRITE_EXTERNAL_STORAGE': 'Write Storage (Can modify files)',
    'android.permission.READ_LOGS': 'Read System Logs (Access system info)',
    'android.permission.SYSTEM_ALERT_WINDOW': 'Overlay Windows (Phishing risk)',
}

# Function to extract features from APK
def extract_features_from_apk(apk_path):
    try:
        a, d, dx = AnalyzeAPK(apk_path)
        permissions = a.get_permissions()
    except Exception as e:
        st.error(f"Error analyzing {apk_path}: {e}")
        return None, None

    # Prepare feature vector based on permissions
    feature_vector = [1 if feature in permissions else 0 for feature in features]

    return feature_vector, permissions

# Streamlit App Interface
st.title("🔍 ANDROSHIELD: APK Malware Detector")

# Upload multiple APK files
apk_files = st.file_uploader("Upload APK files", type="apk", accept_multiple_files=True)

# Predict button
if st.button("Predict"):
    if not apk_files:
        st.warning("⚠ Please upload at least one APK file to proceed.")
    else:
        for apk_file in apk_files:
            # Save uploaded file temporarily
            temp_path = f"temp_{apk_file.name}"
            with open(temp_path, "wb") as f:
                f.write(apk_file.getbuffer())

            # Extract features & permissions
            feature_vector, detected_permissions = extract_features_from_apk(temp_path)

            if feature_vector is None:
                continue  # Skip if extraction failed

            # Convert feature vector to DataFrame
            input_data = pd.DataFrame([feature_vector], columns=features)

            # Make prediction
            prediction = model.predict(input_data)[0]
            is_malware = prediction == 1
            result_text = "🛑 Malware" if is_malware else "✅ Benign"
            result_color = "red" if is_malware else "green"

            # Display the result with color
            st.markdown(f"<h3 style='color: {result_color};'>{apk_file.name}: {result_text}</h3>", unsafe_allow_html=True)

            # **Show high-risk permissions ONLY IF Malware**
            if is_malware:
                risky_permissions = [perm for perm in detected_permissions if perm in high_risk_permissions]
                if risky_permissions:
                    st.write("🔴 **Permissions that contributed to malware classification:**")
                    for perm in risky_permissions:
                        st.markdown(f"🔴 **{perm}** - {high_risk_permissions[perm]}")

            # **Show all permissions (Neutral)**
            st.write("🔹 **All Permissions Used by APK:**")
            for perm in detected_permissions:
                if is_malware and perm in high_risk_permissions:
                    st.markdown(f"🔴 {perm} - {high_risk_permissions[perm]}")
                else:
                    st.markdown(f"⚪ {perm}")  # No red marks for Benign APKs

            st.markdown("---")  # Separator between APK results

            # Remove temp file after processing
            os.remove(temp_path)
