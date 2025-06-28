import streamlit as st
import json
import os
from utils.auth import login
from admin.dashboard import admin_dashboard
from client.dashboard import client_dashboard

TOKEN_FILE = "auth_token.json"

def save_login(user):
    with open(TOKEN_FILE, "w") as f:
        json.dump(user, f)

def load_login():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

def logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    st.session_state.user = None
    st.rerun()

def main():
    st.set_page_config(page_title="Store/Inventory Management System", layout="wide")

    if "user" not in st.session_state:
        st.session_state.user = load_login()

    if st.session_state.user is None:
        user = login()
        if user:
            st.session_state.user = user
            save_login(user)
            st.rerun()
        else:
            st.stop()

    user = st.session_state.user

    with st.sidebar:
        st.markdown("---")
        if st.button("Logout 🔓"):
            logout()

    st.success(f"Welcome, {user['email']} 👋")
    if user['role'] == 'admin':
        admin_dashboard()
    else:
        client_dashboard(user)

if __name__ == "__main__":
    main()















