Got it 👍 You want a **cleaner README** without the long performance report.
Here’s the updated **README.md**:

---

# 🏦 Loan Eligibility Predictor

An AI-powered **Loan Eligibility Prediction Web App** built with **Streamlit** and **Random Forest Classifier**.
The app predicts whether a loan application will be **Approved (Y)** or **Rejected (N)** based on applicant details.

---

## 🔧 Model Used

* **Algorithm:** Random Forest Classifier
* **Features:** Gender, Married, Dependents, Education, Self\_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan\_Amount\_Term, Credit\_History, Property\_Area
* **Target:** Loan\_Status (Y/N)

### 📌 Notes

* **Credit Score** is mapped internally to `Credit_History` (`>=690 → Good history`).
* Data preprocessing:

  * Label Encoding for categorical features
  * Standard Scaling for numeric features

---

---

## ⚙️ Installation & Setup

### 1️⃣ Download the Project and unzip the file



Unzip the folder and navigate  to loan-eligibility-prediction

run the following cmd 
```bash
cd loan-eligibility-prediction
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

* Windows: `venv\Scripts\activate`
* Linux/Mac: `source venv/bin/activate`

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🚀 Usage

1. Go to **[http://localhost:8501/](http://localhost:8501/)** in your browser.
2. Enter applicant details (Income, Loan Amount, Property Area, etc.).
3. Click **Predict** to check eligibility.
4. Navigate to **About Project** for model details.

---
