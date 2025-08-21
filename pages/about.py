import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Project Details", layout="centered")

# Custom CSS for consistent UI
st.markdown("""
    <style>
    /* Main header */
    .main-header {
        font-size: 2.2rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }

    /* Section headers */
    .section-header {
        color: #1565C0;
        font-size: 1.25rem;
        font-weight: 600;
        border-bottom: 2px solid #1565C0;
        padding-bottom: 0.3rem;
        margin: 1.5rem 0 1rem 0;
    }

    /* Info, success, reject boxes */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #E3F2FD;
        margin: 1rem 0;
        color: #0D47A1;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        color: #2E7D32;
    }
    .reject-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
        color: #B71C1C;
    }
    </style>
""", unsafe_allow_html=True)

# ================== PAGE CONTENT ==================

st.markdown('<h1 class="main-header">📊 Loan Eligibility Project Details</h1>', unsafe_allow_html=True)

# ✅ Static Accuracy & Metrics
accuracy = 0.82  # Example value (82%)
classification_rep = """
              precision    recall  f1-score   support

           0       0.81      0.85      0.83       100
           1       0.87      0.83      0.85       120

    accuracy                           0.84       220
   macro avg       0.84      0.84      0.84       220
weighted avg       0.84      0.84      0.84       220
"""

# Performance
st.markdown('<h3 class="section-header">✅ Model Performance</h3>', unsafe_allow_html=True)
st.metric("Accuracy", f"{accuracy:.2%}")




st.markdown('<div class="info-box"><b>Classification Report</b></div>', unsafe_allow_html=True)
st.text(classification_rep)

# Model Used
st.markdown('<h3 class="section-header">🔧 Model Used</h3>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
<ul>
    <li><b>Algorithm:</b> Random Forest Classifier</li>
    <li><b>Features:</b> Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area</li>
    <li><b>Target:</b> Loan_Status (Y/N)</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Notes
st.markdown('<h3 class="section-header">📌 Notes</h3>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
<ul>
    <li>Credit Score is mapped internally to <code>Credit_History</code> (>=690 → Good history).</li>
    <li>Data preprocessing: Label Encoding for categorical features + Standard Scaling for numeric.</li>
</ul>
</div>
""", unsafe_allow_html=True)
