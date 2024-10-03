import streamlit as st
from db.db_connection import get_db_connection

def qr_stats():
    st.title("QR Code Statistics")

    # Fetch the user's generated QR codes from the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    user_id = st.session_state.get('user_id')

    # Add search and filter options
    search_query = st.text_input("Search by Data or Type")
    filter_by_date = st.date_input("Filter by Creation Date", [])
    
    query = "SELECT * FROM qr_codes WHERE user_id = %s"
    params = [user_id]
    
    # Add conditions for search and filter
    if search_query:
        query += " AND (data LIKE %s OR qr_type LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    
    if filter_by_date:
        query += " AND DATE(created_at) = %s"
        params.append(filter_by_date)

    cursor.execute(query, tuple(params))
    qr_codes = cursor.fetchall()
    connection.close()

    # Display the list of generated QR codes
    if qr_codes:
        for qr_code in qr_codes:
            st.write(f"QR Code Data: {qr_code['data']}")
            st.write(f"Type: {qr_code['qr_type']}")
            st.write(f"Box Size: {qr_code['box_size']}, Border Size: {qr_code['border_size']}")
            st.write(f"QR Color: {qr_code['qr_color']}, Background Color: {qr_code['bg_color']}")
            st.write(f"Generated on: {qr_code['created_at']}")
            st.write("---")
    else:
        st.write("No QR codes found matching the criteria.")
