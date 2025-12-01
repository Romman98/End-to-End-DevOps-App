import mysql.connector

# Query Function
import mysql.connector
from mysql.connector import Error

def queryFunc(query):
    try:
        cnx = mysql.connector.connect(
            user="root",
            password="password",
            host="localhost",
            database="testdatabase"
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
    queryFunc("""CREATE TABLE IF NOT EXISTS Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) unique,
    rating int TINYINT
    );
""")

# DATABASE_INIT()
# print(queryFunc('insert into Reviews (name,rating) values ("jojo",4);'))

def checkEntry(name):
    if queryFunc(f'select * from Reviews where name = "{name}"'):
        return True,

