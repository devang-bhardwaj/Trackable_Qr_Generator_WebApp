import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DVNG@dvng@181204",
        database="qr_generator"
    )
    return connection

def create_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DVNG@dvng@181204"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS qr_generator")
    connection.close()

# Creating the database
create_database()

def create_users_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255)
        )
    """)
    connection.commit()
    connection.close()
    
def create_qr_codes_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            data TEXT,
            qr_type VARCHAR(10),
            box_size INT,
            border_size INT,
            qr_color VARCHAR(7),
            bg_color VARCHAR(7),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    connection.commit()
    connection.close()

# Call this function to create the qr_codes table
create_qr_codes_table()
