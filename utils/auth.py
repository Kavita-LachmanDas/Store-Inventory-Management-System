# import streamlit as st
# from database.users import authenticate_user, register_user

# def login():
#     st.sidebar.title("Login / Signup")
#     choice = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])

#     email = st.sidebar.text_input("Email")
#     password = st.sidebar.text_input("Password", type="password")

#     if choice == "Signup":
#         role = st.sidebar.selectbox("Role", ["client"])
#         if st.sidebar.button("Create Account"):
#             if register_user(email, password, role):
#                 st.sidebar.success("Account created!")
#             else:
#                 st.sidebar.error("Email already exists.")
#     else:
#         if st.sidebar.button("Login"):
#             if email == "admin@gmail.com" and password == "12345678":
#                 return {"email": email, "role": "admin"}
#             user = authenticate_user(email, password)
#             if user:
#                 return user
#             else:
#                 st.sidebar.error("Invalid credentials")
#     return None
import streamlit as st
from database.users import authenticate_user, register_user

def login():
    st.sidebar.title("Login / Signup")
    choice = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Signup":
        role = st.sidebar.selectbox("Role", ["client"])
        if st.sidebar.button("Create Account"):
            if register_user(email, password, role):
                st.sidebar.success("Account created!")
                return {"email": email, "password": password, "role": role}
            else:
                st.sidebar.error("Email already exists.")
    else:
        if st.sidebar.button("Login"):
            if email == "admin@gmail.com" and password == "12345678":
                return {"email": email, "role": "admin"}
            user = authenticate_user(email, password)
            if user:
                return user
            else:
                st.sidebar.error("Invalid credentials")

    return None
