import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from db.db_connection import get_db_connection

def qr_generator():
    st.title("Custom QR Code Generator")

    # Select type of QR code
    qr_type = st.selectbox("Select QR Code Type", ["URL", "Text"])

    # Input field for QR code data
    if qr_type == "URL":
        data = st.text_input("Enter URL")
    elif qr_type == "Text":
        data = st.text_input("Enter Text")

    # QR code customization options
    st.write("### Customization Options")
    box_size = st.slider("Box Size", 1, 10, 5)
    border_size = st.slider("Border Size", 1, 10, 4)
    qr_color = st.color_picker("QR Code Color", "#000000")
    bg_color = st.color_picker("Background Color", "#ffffff")

    # Add logo upload option
    logo = st.file_uploader("Upload Logo (Optional)", type=["jpg", "png"])

    # Generate QR code when user clicks the button
    if st.button("Generate QR Code"):
        if data:
            # Create a QR code
            qr = qrcode.QRCode(
                version=1,
                box_size=box_size,
                border=border_size
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill=qr_color, back_color=bg_color)

            # Add logo to the QR code if uploaded
            if logo:
                logo_img = Image.open(logo)
                qr_width, qr_height = img.size
                logo_size = min(qr_width, qr_height) // 4  # Resize logo
                logo_img = logo_img.resize((logo_size, logo_size))

                # Add the logo to the center of the QR code
                img = img.convert("RGBA")
                logo_img = logo_img.convert("RGBA")
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                img.paste(logo_img, pos, mask=logo_img)

            # Convert the image to display on Streamlit
            buffer = BytesIO()
            img.save(buffer)
            img = Image.open(buffer)

            # Display the QR code
            st.image(img, caption="Generated QR Code")

            # Provide a download link
            img.save(buffer, format="PNG")
            buffer.seek(0)
            st.download_button(label="Download QR Code", data=buffer, file_name="qr_code_with_logo.png", mime="image/png")

            # Save the QR code data to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            user_id = st.session_state.get('user_id')  # Get the logged-in user's ID

            cursor.execute("""
                INSERT INTO qr_codes (user_id, data, qr_type, box_size, border_size, qr_color, bg_color)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, data, qr_type, box_size, border_size, qr_color, bg_color))

            connection.commit()
            connection.close()

            st.success("QR code saved successfully!")
        else:
            st.error("Please enter valid data to generate a QR code.")
