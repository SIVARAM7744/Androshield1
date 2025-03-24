# Android Malware Detection using Machine Learning

This section presents a detailed overview of our proposed classification system. This study introduces an Android malware detection system that uses updated data sources and aims for high performance. The system is divided into two main phases: the first is data collection and model training, and the second is testing the trained model using Streamlit.

Figure shows the diagram of the data collection system and model training used in this study. The architecture is divided into four main parts: (1) Dataset – consisting of both benign and malicious APKs collected for analysis, and (2) Feature Extraction – where static features, such as permissions, are extracted from the APKs using Androguard. These features are formatted and stored in a Comma-Separated Values (CSV) file for use in training. Finally, (3) the data is fed into different machine learning classifiers to obtain evaluation results.
![img_4.png](img_4.png)
    
After the training phase, the model is deployed using Streamlit to execute the steps shown in Figure First, (A) an APK file is uploaded as input data through the Streamlit interface. (B) The system extracts relevant information using the Androguard tool and returns a feature vector. Next, (C) the vector is passed to the trained model for prediction. Finally, (D) the prediction result is displayed. In my implementation, rather than deploying the model to a mobile device, I use Streamlit for testing and evaluation after the training phase.
![img_3.png](img_3.png)

---

## Project Structure

The project directory is organized as follows:

```
Android-malware-detection/
│
├── File apk test/                      # Folder containing APK files for testing
│   ├── Benign/                         # APK files classified as benign
│   └── Malware/                        # APK files classified as malware
│
├── ML_Model_Final/                     # Trained machine learning models
│   ├── Random Forest.joblib            # Saved Random Forest model
│
├── apk_permissions_analysis.csv        # CSV file containing extracted permissions
├── data.csv                            # Processed dataset for training/testing
│
├── extracted_features_permission.py    # Extracts permissions from APK files using Androguard
├── features.py                         # Defines a list of permissions to extract as features
├── malware-detection-android.ipynb     # Model training
├── predict.py                          # Predicts whether an APK file is malicious or benign
│
├── venv/                               # Virtual environment for Python dependencies
└── External Libraries                  # Python libraries required for the project
```

---

## Dataset Information

This project uses an enhanced version of the **NATICUSdroid (2022)** dataset combined with additional app samples:

- **NATICUSdroid Dataset**:
  - Contains **29,333 app samples**:
    - **15,169** malicious apps
    - **14,175** benign apps
    - **85 permissions** extracted
  - Data is encoded in binary format: **1** (permission present), **0** (permission absent).

- **Additional Apps**:
  - Added **2,500 unextracted apps**:
    - **1,000 benign apps**:
      - 300 apps from ApkPure (August 2024)
      - 700 apps from CICMalDroid (2020) dataset
    - **1,500 malicious apps**:
      - Obtained from the **Maloid-DS (2024)** dataset.

### Final Dataset Statistics:
- **15,175 benign apps**
- **16,669 malicious apps**
- **85 permissions** extracted.

---

## Key Components

### 1. Extracted Features Permission (`extracted_features_permission.py`)
This script extracts permissions from APK files using the **Androguard** library. It processes the APK files stored in the `File apk test/` folder.

### 2. Features Definition (`features.py`)
This file contains a list of permissions (features) used for malware classification. Example permissions include:

```python
features = [
    'android.permission.GET_ACCOUNTS',
    'com.sonyericsson.home.permission.BROADCAST_BADGE',
    'android.permission.READ_PROFILE',
    'android.permission.MANAGE_ACCOUNTS',
    ...
]
```

### 3. Malware Prediction (`predict.py`)
This script takes an APK file as input and predicts whether it is **malicious** or **benign** using trained models (Random Forest and SVC).

### 4. Trained Models (`ML_Model_Final/`)
- **Random Forest.joblib**: Trained Random Forest model for malware detection.
- **SVC.joblib**: Trained Support Vector Classifier model.

### 5. Test APK Files (`File apk test/`)
Contains APK files used for testing the model:
- `Benign/`: APKs labeled as benign.
- `Malware/`: APKs labeled as malware.

---

## Dependencies

The project uses Python 3 and the following libraries:

- **Androguard**: To extract permissions from APK files.
- **scikit-learn**: For machine learning model training and prediction.
- **joblib**: To save and load trained models.
- **pandas**: For data manipulation and analysis.

### Install Dependencies

Set up a virtual environment and install required libraries:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows

# Install required libraries
pip install androguard scikit-learn pandas joblib
```

---

## How to Run the Project

Before starting, install all necessary dependencies by running the following command:

```bash
pip install -r requirements.txt
```

1. **Extract Permissions**:
   - Run `extracted_features_permission.py` to extract permissions from APK files located in `File apk test/`.

   ```bash
   python extracted_features_permission.py
   ```

2. **Define Features**:
   - Modify or update the list of permissions in `features.py` if necessary.

3. **Predict Malware**:
   - The prediction system is implemented using Streamlit. Run the following command to start the Streamlit app:

   ```bash
   streamlit run predict.py
   ```

4. **Model Training** (Optional):
   - Use the file `malware-detection-android.ipynb` for training machine learning models. Open this file on Google Colab or Jupyter Notebook to:
     - Preprocess the data from `data.csv`.
     - Train models such as Random Forest and SVC.
     - Save the trained models in the `ML_Model_Final/` directory using **joblib**.

---

## Result

The results table shows that machine learning algorithms all achieve high effectiveness in detecting malware on Android, with accuracy and F-measure ranging from 96.7% to 97.3%. These are impressive figures, demonstrating that the algorithms have good classification capabilities in this task. Among them, CatBoost achieves the best performance with the highest accuracy and F-measure of 97.3%. Random Forest also performs very well, coming in second with 97.2%. Other algorithms such as SVM, Decision Tree, and XGBoost show fairly consistent performance, with accuracy and F-measure at levels between 96.7% and 96.8%.

When considering execution time, the differences between the algorithms become more apparent. Decision Tree is the fastest algorithm, taking only 0.28 seconds. Random Forest and XGBoost have execution times of 4.30 seconds and 1.02 seconds, respectively, significantly faster than CatBoost (16.95 seconds) and SVM (17.64 seconds). Overall, while CatBoost and Random Forest excel in accuracy, CatBoost is the best choice if accuracy is prioritized, whereas Decision Tree is suitable when quick processing speed is needed.

| Metrics       | CatBoost | Random Forest | XGBoost | Decision Tree | SVM   |
|---------------|----------|---------------|---------|---------------|-------|
| Accuracy      | 97.3%    | 97.2%         | 96.8%   | 96.7%         | 96.7% |
| F-measure     | 97.3%    | 97.2%         | 96.8%   | 96.7%         | 96.7% |
| Time (second) | 16.95s   | 4.30s         | 1.02s   | 0.28s         | 17.64s|



---

## Conclusion

Malware applications pose a serious risk to smartphones as they can steal personal data and lead to financial losses. This method uses permissions from Android applications as features to identify malware and distinguish them from safe applications. Permissions are extracted using Androguard to generate feature vectors. Different machine learning models, such as Support Vector Machine, Decision tree algorithm, CatBoost, XGBoost, and Random forest, were tested. The results show that the Random Forest algorithm is the most balanced model, achieving an accuracy and F1 of 97.2% and time of 4.30.

---

## References

1. **NATICUSdroid Dataset (2022)**
2. **CICMalDroid Dataset (2020)**
3. **Maloid-DS Dataset (2024)**
4. APK samples sourced from ApkPure.


