import streamlit as st
import sys
import os

# Add the parent 'project' directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.supabase_client import supabase
from auth.login import login

# Set page config
st.set_page_config(page_title="Sign In - IEM College", layout="centered")

# Background + overlay + styles
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
        .signin-container {
            position: relative;
            z-index: 1;
            padding-top: 30px;
            padding-bottom: 30px;
        }
        .signin-title {
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


# Content container
st.markdown('<div class="signin-container">', unsafe_allow_html=True)

# 🔷 Heading
st.markdown("<div class='signin-title'>Sign In to IEM College</div>", unsafe_allow_html=True)

# 🔐 Input Fields with custom labels
st.markdown("<div class='custom-label'>Email</div>", unsafe_allow_html=True)
email = st.text_input("Email", key="email", label_visibility="collapsed")

st.markdown("<div class='custom-label'>Password</div>", unsafe_allow_html=True)
password = st.text_input("Password", type="password", key="password", label_visibility="collapsed")

# 🔘 Sign In button
if st.button("Sign In"):
    sgn=login(email,password)
    if(sgn):
        st.success("Welcome To Chat Interface")
        st.switch_page("pages/dashboard.py")
    else:
        st.error("Signin failed!!!")

# ✨ Sign Up Prompt
st.markdown("""
    <div class='signup-prompt'>
        Don't have an account?
    </div>
""", unsafe_allow_html=True)

# ✅ Create a button that *looks like a hyperlink*
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    if st.button("Sign Up", key="signup_link"):
        st.switch_page("pages/signup.py")

# Close container
st.markdown('</div>', unsafe_allow_html=True)
