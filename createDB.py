import mysql.connector

def create_bird_database_mysql(host, user, password):
    """Creates a MySQL database named 'bird_watch' and a table named 'bird_detections'."""
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        mycursor = mydb.cursor()

        # Check if the database exists and create it if not
        mycursor.execute("CREATE DATABASE IF NOT EXISTS bird_watch")
        print("Database 'bird_watch' created or already exists.")

        # Switch to the 'bird_data' database
        mycursor.execute("USE bird_watch")

        # Create the 'bird_detections' table
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS bird_data (
                Selection INT(11),
                View VARCHAR(255),
                Channel INT(11),
                BeginTime VARCHAR(255),
                EndTime VARCHAR(255),
                LowFreq VARCHAR(255),
                HighFreq VARCHAR(255),
                CommonName VARCHAR(255),
                SpeciesCode VARCHAR(255),
                Confidence FLOAT,
                BeginPath VARCHAR(255),
                FileOffset VARCHAR(255)
            )
        """)

        mydb.commit()
        print("Table 'bird_data' created successfully in 'bird_watch' database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    # Replace with your MySQL connection details
    mysql_host = "localhost"
    mysql_user = "your_user"
    mysql_password = "your_password"

    create_bird_database_mysql(mysql_host, mysql_user, mysql_password)
