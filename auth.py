import streamlit as st

def check_auth():
    """Handles the login interface and session state."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 Forensic Command Center")
        st.subheader("Authorized Personnel Only")
        
        user = st.text_input("Investigator Username")
        password = st.text_input("Access Key", type="password")
        
        if st.button("Initialize System"):
            # Professional Default Credentials
            if user == "admin" and password == "forensic_2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")
        return False
    return True