import streamlit as st
import sys
import os

# Add the parent 'project' directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.supabase_client import supabase
from auth.signup import signup

# Page config
st.set_page_config(page_title="Sign Up - IEM College", layout="centered")

# CSS Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&display=swap');

        .stApp {
            background-color: #000000; /* Fully black background */
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .overlay {
            display: none;
        }
        .signup-container {
            position: relative;
            z-index: 1;
            padding-top: 30px;
            padding-bottom: 30px;
        }
        .signup-title {
            text-align: center;
            font-family: 'Playfair Display', serif;
            color: #ffffff;
            font-size: 36px;
            margin-bottom: 30px;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.1);
        }
        .custom-label, .signup-prompt {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 6px;
            color: #ffffff;
            text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.15);
        }
        label, .stTextInput>div>div>input {
            color: white !important;
        }
        .stTextInput>div>div>input {
            background-color: #111 !important;
            border: 1px solid #444 !important;
        }
        .stButton>button {
            background-color: #222 !important;
            color: white !important;
            border: 1px solid white;
        }
        .stButton>button:hover {
            background-color: #444 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Container
st.markdown('<div class="signup-container">', unsafe_allow_html=True)
# st.markdown("<div class='signup-title'>Create Your Account</div>", unsafe_allow_html=True)
st.markdown("<div class='signup-title'>Create Your Account</div>", unsafe_allow_html=True)
# Labels + Inputs
st.markdown("<div class='big-bold-label'>Full Name</div>", unsafe_allow_html=True)
name = st.text_input("Name", key="name", label_visibility="collapsed")

st.markdown("<div class='big-bold-label'>Date of Birth</div>", unsafe_allow_html=True)
dob = st.date_input("DDMMYYY", key="dob", label_visibility="collapsed")

st.markdown("<div class='big-bold-label'>Email</div>", unsafe_allow_html=True)
email = st.text_input("Email", key="email", label_visibility="collapsed")

st.markdown("<div class='big-bold-label'>Password</div>", unsafe_allow_html=True)
password = st.text_input("Password", type="password", key="password", label_visibility="collapsed")

st.markdown("<div class='big-bold-label'>Confirm Password</div>", unsafe_allow_html=True)
confirm_password = st.text_input("Confirm Password", type="password", key="confirm", label_visibility="collapsed")

if password != confirm_password:
    st.error("Passwords do not match.")


# Button Logic
if st.button("Sign Up"):
    if not name or not dob or not email or not password or not confirm_password:
        st.warning("Please fill in all fields.")
    elif password != confirm_password:
        st.error("Passwords do not match.")
    else:
        try:
            # Sign up user
            sgnup = signup(email,password)
            if(sgnup):
                st.success("Account Created SucessFully!!")
                st.success("Welcome to IEM admission Chat Interface")
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Signup Failed!!!")
        except Exception as e:
            st.error(f"Sign up failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)
