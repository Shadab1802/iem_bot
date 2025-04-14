import streamlit as st

# Set page configuration
st.set_page_config(page_title="IEM College", layout="wide")

# Inject background + overlay + button styles
st.markdown("""
    <style>
        .overlay::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(255, 255, 255, 0.6);
            z-index: -1;
        }

        .stApp {
            background-image: url('https://cdn.britannica.com/65/237365-138-03A2AF7F/did-you-know-The-School-of-Athens-Raphael.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .bottom-center-button {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }

        .bottom-center-button button {
            padding: 35px 80px;
            font-size: 50px;
            font-weight: bold;
            border-radius: 10px;
        }

        .title-text {
            font-size: 100px !important;
            font-weight: bold;
            color: black;
            text-align: center;
            text-shadow: 0 0 5px white, 0 0 15px white, 0 0 25px white;
            z-index: 2;
        }
    </style>

    <div class="overlay"></div>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title-text'>Welcome to IEM College</h1>", unsafe_allow_html=True)

# Bottom center button logic
st.markdown('<div class="bottom-center-button">', unsafe_allow_html=True)
if st.button("Chat with us"):
    st.switch_page("pages/signin.py")  # path to your chat module
st.markdown('</div>', unsafe_allow_html=True)


