import streamlit as st
import pandas as pd
import pickle

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="centered"
)

# ==============================
# LOAD MODEL & COLUMNS
# ==============================
model = pickle.load(open("diabetes_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>

.main {
    background-color: #f4f6f9;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #2563eb;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.stButton>button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    font-size: 20px;
    border-radius: 10px;
    height: 3em;
    border: none;
}

.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}

.result-box {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# TITLE
# ==============================
st.markdown("<div class='title'>🩺 Diabetes Prediction App</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>Predict diabetes risk using Machine Learning</div>",
    unsafe_allow_html=True
)

# ==============================
# INPUT SECTION
# ==============================
st.subheader("📋 Patient Details")

col1, col2 = st.columns(2)

with col1:
    preg = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose", 50, 200, 120)
    bp = st.number_input("Blood Pressure", 30, 120, 70)
    skin = st.number_input("Skin Thickness", 0, 100, 20)

with col2:
    insulin = st.number_input("Insulin", 0, 300, 100)
    bmi = st.number_input("BMI", 10.0, 60.0, 25.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
    age = st.number_input("Age", 1, 100, 30)

# ==============================
# BMI STATUS
# ==============================
if bmi < 18.5:
    st.info("BMI Status: Underweight")
elif bmi < 25:
    st.success("BMI Status: Normal")
elif bmi < 30:
    st.warning("BMI Status: Overweight")
else:
    st.error("BMI Status: Obese")

# ==============================
# PREDICTION
# ==============================
if st.button("🔍 Predict"):

    # Create input dataframe
    input_raw = pd.DataFrame({
        'Pregnancies': [preg],
        'Glucose': [glucose],
        'BloodPressure': [bp],
        'SkinThickness': [skin],
        'Insulin': [insulin],
        'BMI': [bmi],
        'DiabetesPedigreeFunction': [dpf],
        'Age': [age]
    })

    # ==========================
    # Feature Engineering
    # ==========================
    input_raw['Glucose_BMI'] = input_raw['Glucose'] * input_raw['BMI']
    input_raw['Insulin_Glucose'] = input_raw['Insulin'] * input_raw['Glucose']
    input_raw['Age_BMI'] = input_raw['Age'] * input_raw['BMI']
    input_raw['BMI_Squared'] = input_raw['BMI'] ** 2

    # ==========================
    # Encoding
    # ==========================
    input_encoded = pd.get_dummies(input_raw)

    # ==========================
    # Match columns
    # ==========================
    input_df = input_encoded.reindex(columns=columns, fill_value=0)

    # ==========================
    # Prediction
    # ==========================
    prediction = model.predict(input_df)

    # ==========================
    # Output
    # ==========================
    st.subheader("📊 Prediction Result")

    if prediction[0] == 1:

        st.markdown(
            """
            <div class='result-box'
            style='background-color:#fee2e2;color:#b91c1c;'>
            ⚠️ High Risk of Diabetes
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class='result-box'
            style='background-color:#dcfce7;color:#166534;'>
            ✅ Low Risk of Diabetes
            </div>
            """,
            unsafe_allow_html=True
        )

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Developed using Streamlit & Machine Learning")
