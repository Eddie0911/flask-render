from flask import redirect, render_template, session
from models import common

def get_user(filter_clause, params):
  results = common.sql_read(f"SELECT * FROM users {filter_clause};", params)
  if len(results):
    user = results[0]
    return { "id": user[0], "email": user[1], "name": user[2] ,"password_hash": user[3]}
  return None

def write_user(email,name,hashed_password): 
    return common.sql_write("INSERT INTO users(email,name,password_hash) VALUES(%s,%s,%s);",[email,name,hashed_password])

def write_requires(email,name,phone_number,start,end,partysize,budget,today):
    return common.sql_write("INSERT INTO requires(email,name,phone_number,startdate,enddate,partysize,budget,today) VALUES(,%s,%s,%s,%s,%s,%s,%s,%s);",[email,name,phone_number,start,end,partysize,budget,today])

def convert_to_dictionary(item):
    return {"id": str(item[0]), "email": str(item[1]), "name": item[2], "phone_number": item[3], "direction": item[4], "days": item[5]}

def get_requires(id):
    item = common.sql_read("SELECT * FROM requires WHERE id=%s;", [id])[0]
    return convert_to_dictionary(item)

def get_all_requires():
    items = common.sql_read("SELECT * FROM requires;")
    return [convert_to_dictionary(item) for item in items]