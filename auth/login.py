from config.supabase_client import supabase
import streamlit as st


@st.cache_resource

def login(email, password):
    result = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password}
        )
    
    if result.user:
        st.session_state.user_id=result.user.id
        st.session_state["user"] = result.user
        st.session_state["access_token"] = result.session.access_token
        profile_response = supabase.table("profiles").select("role").eq("id", result.user.id).execute()
        role = profile_response.data[0]["role"]
        st.session_state["role"] = role
        return True
    return False