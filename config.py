import mysql.connector

def get_db_connection():
    # update host/user/password as needed
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your database  password",
        database="farm_db"
    )
