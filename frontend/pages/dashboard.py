import streamlit as st
import random,re
import time
from datetime import datetime
import os
import sys
# Add the parent 'project' directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.supabase_client import supabase
from utils.admission_rag_tool import AdmissionRAGTool
rag=AdmissionRAGTool()

# --------------------- Config & Setup ---------------------
st.set_page_config(page_title="IEM College Chatbot", page_icon="✨", layout="wide")

#-------------------------CSS-------------------------------

st.markdown("""
    <style>
        /* General Styling */
        html, body {
            background-color: #f6f9fc;
        }

        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: #002855;
            color: white;
            border-radius: 12px;
            margin-bottom: 1rem;
        }

        .chat-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .chat-icon {
            font-size: 1.5rem;
        }

        .welcome-container {
            text-align: center;
            padding: 2rem;
            color: #333;
        }

        .welcome-title {
            font-size: 1.6rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .welcome-subtitle {
            font-size: 1rem;
            color: #555;
        }

        .user-message, .bot-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            max-width: 75%;
            word-wrap: break-word;
            position: relative;
            color: black;
        }

        .user-message {
            background-color: #DCF8C6;
            align-self: flex-end;
            margin-left: auto;
            color: black;
        }

        .bot-message {
            background-color: #f1f0f0;
            align-self: flex-start;
        }

        .timestamp {
            font-size: 0.7rem;
            color: #999;
            margin-top: 0.5rem;
            text-align: right;
            color: black;
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }

        .typing-dot {
            height: 10px;
            width: 10px;
            background-color: #ccc;
            border-radius: 50%;
            margin: 0 2px;
            animation: blink 1.4s infinite both;
        }

        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes blink {
            0%, 80%, 100% { opacity: 0; }
            40% { opacity: 1; }
        }

        .file-upload-area {
            margin-top: 1rem;
            border: 2px dashed #ccc;
            padding: 1rem;
            border-radius: 8px;
        }

        .footer {
            text-align: center;
            padding: 1rem;
            color: #666;
            font-size: 0.85rem;
            margin-top: 2rem;
        }

        button[kind="primary"] {
            background-color: #002855 !important;
            color: white !important;
            border-radius: 8px !important;
        }

    </style>
""", unsafe_allow_html=True)


def init_session_state():
    defaults = {
        'messages': [],
        'show_file_upload': False,
        'is_typing': False,
        'uploaded_file': None,
        'text_input': ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --------------------- Utils ---------------------
def get_timestamp():
    return datetime.now().strftime("%I:%M %p")

def toggle_file_upload():
    st.session_state.show_file_upload = not st.session_state.show_file_upload

def sign_out():
    try:
        supabase.auth.sign_out()  # logs out user from Supabase
    except Exception as e:
        st.warning(f"Error signing out from Supabase: {e}")
    
    st.session_state.clear()
    st.success("Signed out successfully")
    time.sleep(1)
    st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_bot_response(user_text, file):
     # Check if user is starting the screening registration process
    if re.search(r"\b(start|begin|initiate)\b.*\b(screening|registration)\b", user_text.lower()):
        supabase.table("profiles").update({"STATE": "SCREENING_REGISTRATION"}).eq("user_id", st.session_state.user_id).execute()
        # Append a note to the response
        supabase.table("SCREENING_APPLICANT").insert({"user_id":st.session_state.user_id,"SCREENING_STATUS":"FILLING"}).execute()
        return "\n\n📝 You’ve entered the Screening Registration process.Get your class 12th marksheet image and tell me when you are ready!!"

    from crew.main import basefunction

    # Get the user_state from Supabase
    data_out = supabase.table("profiles").select("STATE").eq("user_id", st.session_state.user_id).single().execute()
    user_state = data_out.data.get('STATE')

    # Call the CrewAI logic
    response = basefunction(st.session_state.user_id,
        user_state,
        st.session_state.chat_history,
        user_text,
        file
    )

    # Append user's message to chat history
    st.session_state.chat_history.append(user_text)

    # Add default instruction message
    return response

# --------------------- UI Rendering ---------------------
def render_header():
    st.markdown("""
    <div class='chat-header'>
        <div class='chat-title'><div class='chat-icon'>✨</div><h1>IEM College Chatbot</h1></div>
        <div>
    """, unsafe_allow_html=True)
    if st.button("Sign out", key="signout-btn"):
        sign_out()
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_chat():
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
                <div class="welcome-container">
                    <div class="welcome-title">Welcome to IEM chatbot. What is your query?</div>
                    <div class="welcome-subtitle">Ask me about admission, courses, campus facilities, or anything else related to IEM College.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                css_class = "user-message" if msg['is_user'] else "bot-message"
                st.markdown(f"""
                    <div class="{css_class}">
                        {msg['text']}
                        <div class="timestamp">{msg['timestamp']}</div>
                    </div>
                """, unsafe_allow_html=True)

        if st.session_state.is_typing:
            st.markdown("""
            <div class="typing-indicator">
                <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>
                <span style="font-size: 12px; color: #666; margin-left: 5px;">IEM is typing...</span>
            </div>
            """, unsafe_allow_html=True)

def render_footer():
    st.markdown(f"""
    <div class="footer">
        © {datetime.now().year} IEM College - All rights reserved
    </div>
    """, unsafe_allow_html=True)

# --------------------- Input Form ---------------------
def input_section():
    input_col1, input_col2 = st.columns([0.9, 0.1])
    with input_col2:
        if st.button("Upload", key="plus_button"):
            toggle_file_upload()

    with st.form("chat_form", clear_on_submit=True):
        text = st.text_input("Type your question here...", key="text_input", label_visibility="collapsed")
        file = None
        if st.session_state.show_file_upload:
            st.markdown('<div class="file-upload-area">', unsafe_allow_html=True)
            file = st.file_uploader("Upload file", type=["pdf", "docx", "jpg", "png"], label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        send_button = st.form_submit_button("Send")

    return send_button, text.strip(), file

# --------------------- Main Execution ---------------------
render_header()
render_chat()
submit, text_input, uploaded_file = input_section()

if submit and (text_input or uploaded_file):
    st.session_state.messages.append({
        "text": text_input if text_input else f"📎 {uploaded_file.name}",
        "is_user": True,
        "timestamp": get_timestamp()
    })
    st.session_state.is_typing = True
    st.session_state["response_input"] = (text_input, uploaded_file)  # store for next rerun
    st.rerun()

# Respond after rerun
if st.session_state.is_typing and "response_input" in st.session_state:
    text_input, uploaded_file = st.session_state.response_input
    time.sleep(1)
    response = get_bot_response(text_input, uploaded_file)
    st.session_state.messages.append({
        "text": response,
        "is_user": False,
        "timestamp": get_timestamp()
    })
    st.session_state.is_typing = False
    del st.session_state["response_input"]
    st.rerun()

render_footer()