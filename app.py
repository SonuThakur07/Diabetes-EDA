import streamlit as st
import pandas as pd
import pickle

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Diabetes Predictor",
    page_icon="🩺",
    layout="centered"
)

# ==========================================
# LOAD MODEL
# ==========================================
model = pickle.load(open("diabetes_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ==========================================
# SESSION STATE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>

/* BACKGROUND */
.stApp{
    background:#eef3f7;
}

/* HIDE STREAMLIT */
#MainMenu, footer, header{
    visibility:hidden;
}

/* REMOVE TOP SPACE */
.block-container{
    padding-top:2rem;
}

/* CARD */
.auth-box{
    background:white;
    width:520px;
    padding:45px;
    border-radius:24px;
    margin:auto;
    margin-top:50px;
    box-shadow:0 10px 35px rgba(0,0,0,0.08);
}

/* TITLE */
.auth-title{
    text-align:center;
    font-size:54px;
    font-weight:800;
    background:linear-gradient(to right,#2563eb,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:10px;
}

/* SUBTITLE */
.auth-subtitle{
    text-align:center;
    color:#6b7280;
    font-size:20px;
    margin-bottom:35px;
}

/* LABEL */
label{
    font-size:17px !important;
    font-weight:700 !important;
    color:#111827 !important;
}

/* INPUT */
.stTextInput input{
    height:55px !important;
    border-radius:12px !important;
    border:1px solid #d1d5db !important;
    padding-left:15px !important;
    font-size:17px !important;
}

/* MAIN BUTTON */
.main-btn button{
    width:100%;
    height:55px;
    border:none;
    border-radius:12px;
    background:linear-gradient(to right,#2563eb,#06b6d4);
    color:white;
    font-size:20px;
    font-weight:700;
}

.main-btn button:hover{
    color:white;
}

/* SMALL TEXT */
.bottom-text{
    text-align:center;
    margin-top:22px;
    color:#6b7280;
    font-size:17px;
}

.blue{
    color:#2563eb;
    font-weight:700;
}

/* DASHBOARD TITLE */
.dashboard-title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    background:linear-gradient(to right,#2563eb,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:10px;
}

.dashboard-subtitle{
    text-align:center;
    color:#6b7280;
    font-size:20px;
    margin-bottom:35px;
}

/* RESULT */
.result-high{
    background:#fee2e2;
    color:#b91c1c;
    padding:25px;
    border-radius:16px;
    text-align:center;
    font-size:28px;
    font-weight:700;
    margin-top:20px;
}

.result-low{
    background:#dcfce7;
    color:#166534;
    padding:25px;
    border-radius:16px;
    text-align:center;
    font-size:28px;
    font-weight:700;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOGIN / SIGNUP
# ==========================================
if not st.session_state.logged_in:

    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)

    # LOGIN PAGE
    if not st.session_state.show_signup:

        st.markdown(
            "<div class='auth-title'>Welcome Back</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='auth-subtitle'>Please sign in to access your health dashboard</div>",
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Email Address",
            placeholder="name@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="••••••••"
        )

        st.markdown("<div class='main-btn'>", unsafe_allow_html=True)

        if st.button("Sign In"):
            st.session_state.logged_in = True
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class='bottom-text'>
            Don't have an account?
            <span class='blue'> Sign Up</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Create New Account"):
            st.session_state.show_signup = True
            st.rerun()

    # SIGNUP PAGE
    else:

        st.markdown(
            "<div class='auth-title'>Create Account</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='auth-subtitle'>Join us to start tracking your health data securely</div>",
            unsafe_allow_html=True
        )

        new_user = st.text_input(
            "Email Address",
            placeholder="name@example.com"
        )

        new_pass = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 6 characters"
        )

        confirm_pass = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="••••••••"
        )

        st.markdown("<div class='main-btn'>", unsafe_allow_html=True)

        if st.button("Register"):

            if new_pass == confirm_pass:

                st.success("Account Created Successfully")
                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Passwords do not match")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class='bottom-text'>
            Already have an account?
            <span class='blue'> Sign In</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Back To Login"):
            st.session_state.show_signup = False
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ==========================================
# DASHBOARD
# ==========================================
st.markdown(
    "<div class='dashboard-title'>🩺 Diabetes Predictor</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='dashboard-subtitle'>AI Powered Diabetes Risk Analysis System</div>",
    unsafe_allow_html=True
)

preg = st.number_input("Pregnancies", 0, 20, 1)
glucose = st.number_input("Glucose Level", 50, 250, 120)
bp = st.number_input("Blood Pressure", 30, 150, 70)
skin = st.number_input("Skin Thickness", 0, 100, 20)
insulin = st.number_input("Insulin", 0, 900, 100)
bmi = st.number_input("BMI", 10.0, 60.0, 25.0)
dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
age = st.number_input("Age", 1, 100, 30)

if st.button("Predict Diabetes Risk"):

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

    input_raw['Glucose_BMI'] = input_raw['Glucose'] * input_raw['BMI']
    input_raw['Insulin_Glucose'] = input_raw['Insulin'] * input_raw['Glucose']
    input_raw['Age_BMI'] = input_raw['Age'] * input_raw['BMI']
    input_raw['BMI_Squared'] = input_raw['BMI'] ** 2

    input_encoded = pd.get_dummies(input_raw)

    input_df = input_encoded.reindex(columns=columns, fill_value=0)

    prediction = model.predict(input_df)

    if prediction[0] == 1:

        st.markdown(
            """
            <div class='result-high'>
            ⚠️ High Risk of Diabetes
            </div>
            """,
            unsafe_allow_html=True
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
