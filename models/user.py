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

def write_requires(email,name,phone_number,direction,days):
    return common.sql_write("INSERT INTO requires(email,name,phone_number,direction,days) VALUES(%s,%s,%s,%s,%s);",[email,name,phone_number,direction,days])