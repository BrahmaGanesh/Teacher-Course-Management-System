import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="brahmaganesh@99K",
        database="Teacher_Course_Management"
    )
