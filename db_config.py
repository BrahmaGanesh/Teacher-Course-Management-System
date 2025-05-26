import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load .env file variables locally
load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            port=int(os.environ['DB_PORT'])
        )
        if conn.is_connected():
            print("Connected to MySQL database")
        return conn
    except KeyError as e:
        print(f"Environment variable {e} not set.")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None
