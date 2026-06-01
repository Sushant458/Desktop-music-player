<<<<<<< HEAD
import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushant@458",  # Recommendation: Use environment variables for security
            database="Music_playerDB"
        )
        if conn.is_connected():
            # print("Connection is successful") # Uncomment for debugging
            pass
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
=======
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
>>>>>>> b7b53d00ed6f75fe95d39350186ca96275e315b0
