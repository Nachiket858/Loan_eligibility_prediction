import streamlit as st
import pandas as pd
import joblib
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Loan Eligibility Predictor",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main header */
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
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

    /* Buttons */
    .stButton>button {
        background-color: #1E88E5 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #1565C0 !important;
    }

    /* Success box */
    .success-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        color: #2E7D32;
    }

    /* Reject box */
    .reject-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
        color: #B71C1C;
    }

    /* Info box */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #E3F2FD;
        margin: 1rem 0;
        color: #0D47A1;
    }

    /* List items inside info boxes */
    .info-box ul {
        margin-left: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Function to load model and preprocessors
@st.cache_resource
def load_model_and_preprocessors(model_path, encoders_path, scaler_path, status_encoder_path):
    model = joblib.load(model_path)
    label_encoders = joblib.load(encoders_path)
    scaler = joblib.load(scaler_path)
    status_encoder = joblib.load(status_encoder_path)
    return model, label_encoders, scaler, status_encoder

# Function to preprocess user input data
def preprocess_user_input(user_input, label_encoders, scaler):
    user_data = pd.DataFrame(user_input, index=[0])
    categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    for col in categorical_columns:
        if col in label_encoders:
            user_data[col] = label_encoders[col].transform(user_data[col])
    numeric_columns = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
    user_data[numeric_columns] = scaler.transform(user_data[numeric_columns])
    return user_data

# Function to predict using the model
def predict(model, user_data):
    predictions = model.predict(user_data)
    return predictions[0]

# Load model and preprocessors
model_path = './model/random_forest_model.pkl'
encoders_path = './model/label_encoders.pkl'
scaler_path = './model/scaler.pkl'
status_encoder_path = './model/status_encoder.pkl'

model, label_encoders, scaler, status_encoder = load_model_and_preprocessors(
    model_path, encoders_path, scaler_path, status_encoder_path
)

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1005/1005141.png", width=100)
    selected = option_menu(
        menu_title="Main Menu",
        options=["Loan Predictor", "Information", "About"],
        icons=["house", "info-circle", "person"],
        default_index=0,
    )

# Main content
if selected == "Loan Predictor":
    st.markdown('<h1 class="main-header">🏦 Loan Eligibility Predictor</h1>', unsafe_allow_html=True)

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 class="section-header">Personal Information</h3>', unsafe_allow_html=True)
        gender = st.selectbox('Gender', ['Male', 'Female'])
        married = st.selectbox('Marital Status', ['Yes', 'No'])
        dependents = st.selectbox('Number of Dependents', ['0', '1', '2', '3+'])
        education = st.selectbox('Education', ['Graduate', 'Not Graduate'])
        self_employed = st.selectbox('Self Employed', ['Yes', 'No'])
        property_area = st.selectbox('Property Area', ['Urban', 'Semiurban', 'Rural'])

    with col2:
        st.markdown('<h3 class="section-header">Financial Information</h3>', unsafe_allow_html=True)
        applicant_income = st.number_input('Applicant Income (₹)', min_value=0, value=5000, step=1000)
        coapplicant_income = st.number_input('Coapplicant Income (₹)', min_value=0, value=0, step=1000)
        loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=100000, step=10000)
        loan_amount_term = st.slider('Loan Term (months)', 12, 480, 360)

        # Credit score input (converted internally to Credit_History for model)
        credit_score = st.slider('Credit Score', 300, 900, 700)
        credit_history = 1 if credit_score >= 600 else 0

        # Credit score indicator
        if credit_score >= 750:
            st.success("Excellent Credit Score")
        elif credit_score >= 690:
            st.info("Good Credit Score")
        elif credit_score >= 600:
            st.warning("Fair Credit Score")
        else:
            st.error("Poor Credit Score")

    user_input = {
        'Gender': gender,
        'Married': married,
        'Dependents': dependents,
        'Education': education,
        'Self_Employed': self_employed,
        'ApplicantIncome': applicant_income,
        'CoapplicantIncome': coapplicant_income,
        'LoanAmount': loan_amount,
        'Loan_Amount_Term': loan_amount_term,
        'Credit_History': credit_history,
        'Property_Area': property_area
    }

    if st.button('Check Eligibility'):
        with st.spinner('Analyzing your information...'):
            user_data_processed = preprocess_user_input(user_input, label_encoders, scaler)
            prediction = predict(model, user_data_processed)
            prediction_label = status_encoder.inverse_transform([prediction])[0]

            if prediction_label == 'Y':
                st.markdown(f"""
                <div class="success-box">
                    <h2>✅ Congratulations! Loan Likely Approved</h2>
                    <p>Your loan application is likely to be approved.</p>
                    <p><strong>Credit Score:</strong> {credit_score}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="reject-box">
                    <h2>❌ Loan Application Likely Rejected</h2>
                    <p>Your loan application may not be approved at this time.</p>
                    <p><strong>Credit Score:</strong> {credit_score}</p>
                </div>
                """, unsafe_allow_html=True)

elif selected == "Information":
    st.markdown('<h1 class="main-header">📋 Loan Information</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h3>Understanding Loan Eligibility</h3>
        <p>Our AI-powered predictor analyzes multiple factors to estimate your approval chance:</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Factors Considered"):
        st.markdown("""
        - **Credit Score** (300-900)  
        - **Income & Coapplicant Income**  
        - **Loan Amount & Term**  
        - **Employment Type**  
        - **Property Area**  
        - **Dependents**  
        """)

elif selected == "About":
    st.markdown('<h1 class="main-header">ℹ️ About</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h3>Loan Eligibility Predictor</h3>
        <p>This tool predicts loan eligibility using a trained Random Forest model.</p>
    </div>
                
            
    """, unsafe_allow_html=True)

    st.info("""
    **Disclaimer**: This is only a prediction.  
    Final decisions are made by banks based on additional checks.
    """)
