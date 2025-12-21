import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushant***", # Enter your workbencha password 
            database="Music_playerDB"
        )
        if conn.is_connected():
            # print("Connection is successful") # Uncomment for debugging
            pass
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")

        return None
