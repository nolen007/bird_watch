#!/usr/bin/env python

import mysql.connector
import os

# Define MySQL connection parameters
host = "host"
port = 3306
user = "root"
database_name = "bird_watch"
password = "password"
# Define the table name
table_name = "bird_data"

def process_txt_file(file_path):
    """Processes a single .txt file to create a table and insert data into MySQL."""
    try:
        with open(file_path, 'r') as f:
            header = f.readline().strip().split('\t')
            columns = [col.replace(' ', '') for col in header]

            # Determine appropriate data types and create column definitions
            column_definitions = []
            for col in columns:
                column_name = col.replace('(Hz)', '').replace('(s)', '')
                column_type = "VARCHAR(255)"
                if column_name in ["Selection", "Channel"]:
                    column_type = "INT"
                elif column_name in ["Begin_Time_s", "End_Time_s", "Low_Freq_Hz", "High_Freq_Hz", "Confidence", "File_Offset_s"]:
                    column_type = "FLOAT"
                column_definitions.append(f"{column_name} {column_type}")

            create_table_statement = f"CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ({', '.join(column_definitions)})"

            # Construct the INSERT statement
            insert_columns = ', '.join([col.replace('(Hz)', '').replace('(s)', '') for col in columns])
            placeholders = ', '.join(['%s'] * len(columns))
            insert_statement = f"INSERT INTO {database_name}.{table_name} ({insert_columns}) VALUES ({placeholders})"

            # Connect to MySQL
            mydb = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database_name
            )
            mycursor = mydb.cursor()

            # Execute the CREATE TABLE statement
            mycursor.execute(create_table_statement)
            mydb.commit()

            # Read and insert data rows
            for line in f:
                values = [v.strip() for v in line.strip().split('\t')]
                # Convert numeric values to appropriate types if needed
                converted_values = []
                for i, value in enumerate(values):
                    column_name = columns[i].replace(' ', '')
                    if column_name in ["Selection", "Channel"]:
                        try:
                            converted_values.append(int(value))
                        except ValueError:
                            converted_values.append(value)
                    elif column_name in ["Begin_Time_s", "End_Time_s", "Low_Freq_Hz", "High_Freq_Hz", "Confidence", "File_Offset_s"]:
                        try:
                            converted_values.append(float(value))
                        except ValueError:
                            converted_values.append(value)
                    else:
                        if '/' in value:
                            converted_values.append(value.rsplit('/', 1)[-1])
                        else:
                            converted_values.append(value)

                try:
                    mycursor.execute(insert_statement, converted_values)
                    mydb.commit()
                except mysql.connector.Error as err:
                    print(f"Error inserting row from file {file_path}: {err}")
                    print(f"Problematic data: {values}")

            print(f"Data insertion from file {file_path} complete.")

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except mysql.connector.Error as err:
        print(f"Error connecting or executing MySQL query: {err}")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()

if __name__ == "__main__":
    search_directory = "./output/"
    for filename in os.listdir(search_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(search_directory, filename)
            print(f"{file_path} read")
            process_txt_file(file_path)
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

    print("All data insertion processes completed.")
