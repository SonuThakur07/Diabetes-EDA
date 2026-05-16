import streamlit as st
import pandas as pd
import pickle

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide"
)

# =====================================
# LOAD MODEL
# =====================================
model = pickle.load(open("diabetes_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #dbeafe, #f0f9ff);
}

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #1e3a8a;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #475569;
    margin-bottom: 30px;
}

.glass {
    background: rgba(255,255,255,0.55);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(31,38,135,0.15);
    margin-bottom: 25px;
}

.stButton>button {
    width: 100%;
    height: 3.5em;
    border-radius: 15px;
    border: none;
    background: linear-gradient(to right, #2563eb, #1d4ed8);
    color: white;
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #1d4ed8, #1e40af);
    color: white;
}

.result-high {
    background: #fee2e2;
    color: #b91c1c;
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    font-size: 34px;
    font-weight: bold;
}

.result-low {
    background: #dcfce7;
    color: #166534;
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    font-size: 34px;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================
st.markdown(
    "<div class='main-title'>🩺 Diabetes Prediction App</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>AI Powered Health Risk Prediction System</div>",
    unsafe_allow_html=True
)

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("ℹ️ About")

st.sidebar.info(
    """
This application predicts diabetes risk using
Machine Learning algorithms based on patient health data.
"""
)

st.sidebar.success("Model Used: Random Forest")

st.sidebar.markdown("### 🩺 Health Tips")
st.sidebar.write("✅ Drink more water")
st.sidebar.write("✅ Exercise daily")
st.sidebar.write("✅ Maintain healthy BMI")
st.sidebar.write("✅ Avoid excess sugar")

# =====================================
# INPUT SECTION
# =====================================
st.markdown("<div class='glass'>", unsafe_allow_html=True)

st.subheader("📋 Enter Patient Details")

col1, col2 = st.columns(2)

with col1:
    preg = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.slider("Glucose", 50, 250, 120)
    bp = st.slider("Blood Pressure", 30, 150, 70)
    skin = st.slider("Skin Thickness", 0, 100, 20)

with col2:
    insulin = st.slider("Insulin", 0, 900, 100)
    bmi = st.slider("BMI", 10.0, 60.0, 25.0)
    dpf = st.slider("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
    age = st.slider("Age", 1, 100, 30)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================
# BMI STATUS
# =====================================
st.markdown("<div class='glass'>", unsafe_allow_html=True)

st.subheader("📊 BMI Analysis")

if bmi < 18.5:
    st.info("Underweight")
elif bmi < 25:
    st.success("Normal BMI")
elif bmi < 30:
    st.warning("Overweight")
else:
    st.error("Obese")

st.markdown("</div>", unsafe_allow_html=True)

# =====================================
# PREDICTION
# =====================================
if st.button("🔍 Predict Diabetes Risk"):

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

    # Feature Engineering
    input_raw['Glucose_BMI'] = input_raw['Glucose'] * input_raw['BMI']
    input_raw['Insulin_Glucose'] = input_raw['Insulin'] * input_raw['Glucose']
    input_raw['Age_BMI'] = input_raw['Age'] * input_raw['BMI']
    input_raw['BMI_Squared'] = input_raw['BMI'] ** 2

    # Encoding
    input_encoded = pd.get_dummies(input_raw)

    # Match Columns
    input_df = input_encoded.reindex(columns=columns, fill_value=0)

    # Prediction
    prediction = model.predict(input_df)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    st.subheader("📈 Prediction Result")

    if prediction[0] == 1:

        st.markdown(
            """
            <div class='result-high'>
            ⚠️ High Risk of Diabetes
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Please consult a healthcare professional."
        )

    else:

        st.markdown(
            """
            <div class='result-low'>
            ✅ Low Risk of Diabetes
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("Healthy indicators detected.")

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================
# FOOTER
# =====================================
st.markdown("---")

st.markdown(
    """
    <div class='footer'>
        Developed using ❤️ Streamlit & Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
