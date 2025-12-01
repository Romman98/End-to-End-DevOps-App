import mysql.connector
from mysql.connector import Error
import os

# Import Env Vars

env_user = os.getenv("MYSQL_USER")
env_password = os.getenv("MYSQL_PASSWORD")
env_database = os.getenv("MYSQL_DATABASE")
env_host = os.getenv("MYSQL_HOST")


# Query Function
def queryFunc(query):
    try:
        cnx = mysql.connector.connect(
            user=env_user,
            password=env_password,
            host=env_host,
            database=env_database
        )
        cursor = cnx.cursor()
        cursor.execute(query)
        # SELECT / SHOW queries
        if query.strip().lower().startswith(("select", "show")):
            result = cursor.fetchall()
            return result
        # Non-select queries → commit
        cnx.commit()
        return {"result": "OK"}
    except Error as err:
        # Return the MySQL error instead of crashing
        return {"error": str(err), "result": None}
    finally:
        # Close connection safely
        try:
            cursor.close()
            cnx.close()
        except:
            pass


def DATABASE_INIT():
    result = queryFunc("""CREATE TABLE IF NOT EXISTS Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) unique,
    rating TINYINT
    );"""
    )
    if result == {'result': 'OK'}:
        return "Database Created Successfully!"
    return "Error in creating the DB!"


print(DATABASE_INIT())

def checkEntry(name):
    if queryFunc(f'select * from Reviews where name = "{name}"'):
        return True
