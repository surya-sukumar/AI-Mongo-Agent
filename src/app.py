import streamlit as st
from database import register_user, verify_user

def main():
    st.set_page_config(page_title="AI Mongo Agent", layout="centered")
    st.title("AI Mongo Agent")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.header("Login")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                if login_email and login_password:
                    success, message = verify_user(login_email, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields")

        with tab2:
            st.header("Register")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
            
            if st.button("Register"):
                if reg_email and reg_password and reg_confirm_password:
                    if reg_password != reg_confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = register_user(reg_email, reg_password)
                        if success:
                            st.success(message)
                            st.info("Please proceed to login")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")
    else:
        st.success("Welcome to AI Mongo Agent!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main() 