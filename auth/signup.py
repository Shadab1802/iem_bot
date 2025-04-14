from config.supabase_client import supabase
import streamlit as st

def signup(email: str, password: str) -> bool:
    try:
        # Sign up the user
        result = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # Check if sign up succeeded
        if result.user:
            user_id = result.user.id

            # Optional: Add user to `profiles` table
            supabase.table("profiles").insert({
                "id": user_id,
                "email": email,
            }).execute()

            st.success("Account created! Please verify your email.")
            return True

        # If sign-up failed and error is available
        elif result.error:
            st.error("Sign up failed: " + result.error.message)
            return False

    except Exception as e:
        st.error(f"Sign up failed: {str(e)}")

    return False