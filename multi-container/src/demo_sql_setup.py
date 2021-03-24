import mysql.connector


def main():
    host = "localhost"

    # Connect to mysql

    mydb = mysql.connector.connect(
        host=host,
        user="root",
        password="my-secret-pw"
    )

    # Create a database
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE mydatabase")
    cursor.close()

    # Create a table

    mydb = mysql.connector.connect(
        host=host,
        user="root",
        password="my-secret-pw",
        database="mydatabase"
    )

    cursor = mydb.cursor()
    cursor.execute("CREATE TABLE friends (name1 VARCHAR(255), name2 VARCHAR(255))")
    cursor.close()


if __name__ == '__main__':
    main()
