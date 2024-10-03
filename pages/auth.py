import streamlit as st
import mysql.connector
from db.db_connection import get_db_connection
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def sign_up():
    st.title("Sign Up")

    # Input form for sign-up
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Hash the password before saving
        hashed_password = hash_password(password)

        try:
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
            """, (username, email, hashed_password))
            connection.commit()
            st.success("Sign-up successful! You can now log in.")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            connection.close()

def login():
    st.title("Login")

    # Input form for login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch user by username
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        connection.close()

        if user:
            # Verify the password
            if verify_password(password, user['password'].encode('utf-8')):
                st.success(f"Welcome {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
            else:
                st.error("Incorrect password")
        else:
            st.error("User not found")

def auth():
    st.sidebar.title("Authentication")
    choice = st.sidebar.radio("Choose", ["Login", "Sign Up"])

    if choice == "Sign Up":
        sign_up()
    else:
        login()
