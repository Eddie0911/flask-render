import psycopg2
from models import common

#tour.py is controler 4 basic: C:CREATE R:READ U:UPDATE  D:DELETE
def insert_tour(name,price):
    common.sql_write("INSERT INTO tour(name,price) VALUES(%s,%s);",[name,price])

def convert_to_dictionary(item):
    return {"id": str(item[0]), "name": item[1], "price": item[2]}

def get_tour(id):
    item = common.sql_read("SELECT * FROM tour WHERE id=%s;", [id])[0]
    return convert_to_dictionary(item)

def get_all_tour():
    items = common.sql_read("SELECT * FROM tour;")
    return [convert_to_dictionary(item) for item in items]

def update_tour(id, name, price):
    common.sql_write(f"UPDATE tour SET name=%s,  price=%s WHERE id={id}", [name, price])

def delete_tour(id):
    common.sql_write(f"DELETE FROM tour WHERE id={id}", [id])