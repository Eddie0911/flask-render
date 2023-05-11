import psycopg2
import os

def sql_read(query, parameters=[]):
    connection = psycopg2.connect(dbname=os.getenv("DB_NAME"),user=os.getenv("USER"),password=os.getenv("PASSWORD"),host=os.getenv("HOST"),port=os.getenv("DB_PORT"))
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results

def sql_write(query, parameters=[]):
    connection = psycopg2.connect(dbname=os.getenv("DB_NAME"),user=os.getenv("USER"),password=os.getenv("PASSWORD"),host=os.getenv("HOST"),port=os.getenv("DB_PORT"))
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()


