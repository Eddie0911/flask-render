import psycopg2

def sql_read(query, parameters=[]):
    connection = psycopg2.connect(dbname="travel")
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results

def sql_write(query, parameters=[]):
    connection = psycopg2.connect(dbname="travel")
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()
