import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from database import register_user, verify_user
from vertex_ai import VertexAIClient
from typing import List, Dict

def initialize_vertex_ai():
    """Initialize Vertex AI client if not already in session state"""
    if 'vertex_ai_client' not in st.session_state:
        try:
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            if not project_id:
                st.error("Google Cloud Project ID not found. Please set GOOGLE_CLOUD_PROJECT environment variable.")
                return None
            
            st.session_state.vertex_ai_client = VertexAIClient(project_id=project_id)
            return st.session_state.vertex_ai_client
        except Exception as e:
            st.error(f"Failed to initialize Vertex AI: {e}")
            return None

def chat_interface():
    """Display chat interface and handle interactions"""
    st.header("AI Chat Interface")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["author"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"author": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        client = st.session_state.get('vertex_ai_client')
        if client:
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = client.get_chat_response(st.session_state.messages)
                        ai_message = response["response"]["content"]
                        st.write(ai_message)
                        st.session_state.messages.append({"author": "assistant", "content": ai_message})
            except Exception as e:
                st.error(f"Error getting AI response: {e}")
        else:
            st.error("Vertex AI client not initialized. Please check your configuration.")

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
        # Initialize Vertex AI when user is logged in
        if initialize_vertex_ai():
            # Show chat interface
            chat_interface()
        
        if st.button("Logout", key="logout"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main() 