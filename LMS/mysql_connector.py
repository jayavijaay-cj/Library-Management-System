import pymysql

try:
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="harinee@11",  # your updated password
        database="db"  # replace with your database name
    )
    print("Database connected")
except pymysql.MySQLError as e:
    print(f"Connection unsuccessful: {e}")