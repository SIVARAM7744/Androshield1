import streamlit as st
from features import features
import pandas as pd
from joblib import load
from androguard.misc import AnalyzeAPK

# Load the pre-trained model
model = load('ML_Model_Final/Random Forest.joblib')


# Function to extract features from the APK file for prediction
def extract_features_from_apk(apk_path):
    a, d, dx = AnalyzeAPK(apk_path)
    permissions = a.get_permissions()
    # Prepare feature vector based on permissions
    vector = [1 if feature in permissions else 0 for feature in features]
    return vector

# App interface
st.title("ANDROSHIELD")

# Custom CSS for buttons
st.markdown(
    """
    <style>
        /* Style for the file uploader button */
        .stFileUploader > label { 
            color: white; 
            background-color: #28a745; 
            padding: 10px 15px; 
            border-radius: 5px; 
            cursor: pointer;
        }
        .stFileUploader > label:hover {
            background-color: #218838; /* Slightly darker green on hover */
        }

        /* Style for the predict button */
        .stButton button { 
            color: white; 
            background-color: #28a745; 
            padding: 10px 15px; 
            border: none; 
            border-radius: 5px; 
            transition: background-color 0.3s ease; /* Smooth transition */
        }
        .stButton button:hover { 
            background-color: #85e085; /* Light green background on hover */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Upload multiple APK files
apk_files = st.file_uploader("Upload APK files", type="apk", accept_multiple_files=True)

# Button always displayed
predict_button = st.button("Predict")

if predict_button:
    if not apk_files:
        # Display a dialog if no files are uploaded
        st.markdown(
            """
            <div id="dialog-message" style="border: 2px solid #dc3545; padding: 20px; border-radius: 5px; background-color: #f8d7da;">
                <p style="color: #721c24;">You have not uploaded any APK files. Please upload files to proceed!</p>
            </div>
            <script>
                // Set a timeout to hide the message after 5 seconds (5000ms)
                setTimeout(function() {
                    document.getElementById("dialog-message").style.display = "none";
                }, 5000);
            </script>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Process files if uploaded
        results = []
        for apk_file in apk_files:
            # Save the file temporarily for analysis
            temp_path = f"temp_{apk_file.name}"
            with open(temp_path, "wb") as f:
                f.write(apk_file.getbuffer())

            # Extract features from the APK file
            feature_vector = extract_features_from_apk(temp_path)
            input_data = pd.DataFrame([feature_vector], columns=features)

            # Make prediction
            prediction = model.predict(input_data)
            result = "Malware" if prediction[0] == 1 else "Benign"
            results.append(f"{apk_file.name}: {result}")

        # Display the results in the requested format
        st.subheader("Prediction Results:")
        for result in results:
            st.write(result)
