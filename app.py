import streamlit as st
from pages.qr_generation import qr_generator
from pages.stats import qr_stats
from pages.auth import auth

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    auth()
else:
    # Sidebar for navigation
    st.sidebar.title("QR Generator WebApp")
    choice = st.sidebar.radio("Navigate", ["QR Generator", "Statistics"])

    # Navigation between pages
    if choice == "QR Generator":
        qr_generator()
    elif choice == "Statistics":
        qr_stats()

    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()
