from flask import Flask, render_template , request ,redirect,session
from models import tour, user
import os
import bcrypt
import psycopg2
from datetime import date 




app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY','default_secret_key')

# @app.route('/')
# def index():
#     # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
#     connection = psycopg2.connect(os.getenv("DATABASE_URL"))
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM mytable;")
#     results = cursor.fetchall()
#     connection.close()
#     return f"{results[0]}"

# Home page
@app.route('/')
def homepage():
    return render_template('home.html')

# grouptour page
@app.route('/grouptour')
def grouptour():
    return render_template('grouptour.html',tour_items=tour.get_all_tour())

# About us page
@app.route('/about')
def aboutus():
    return render_template('about.html')

# add page
@app.route('/add')
def add_tour():
    if session.get("user_id",""):
        return render_template("add.html")
    else:
        return redirect("/login")

# get the data from form
@app.route('/api/add', methods=["POST"])
def add_tour_docu():
    form = request.form
    # use tour from model to insert data into database 
    tour.insert_tour(form.get("item_name"),form.get("item_price"))
    return redirect("/")

#edit page and using session to check the user 
@app.route('/edit/<id>')
def edit_tour_form(id):
    if session.get("user_id", ""):
        return render_template("edit.html", tour_item=tour.get_tour(id))
    else:
        return redirect("/login")

@app.route('/api/edit/<id>', methods=["POST"])
def edit_tour_docu(id):
    form = request.form

    tour.update_tour(id,form.get("item_name"),form.get("item_price"))
    return redirect("/grouptour")

@app.route('/delete/<id>')
def delete_tour_form(id):
  if session.get("user_id", ""):
    return render_template("delete.html", tour_item=tour.get_tour(id))
  else:
    return redirect("/login")

@app.route('/api/delete',methods=["POST"])
def delete_tour_docu():
    tour.delete_tour(request.form.get("id"))

    return redirect('/grouptour')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route("/signup", methods=['POST'])
def signup():
    form = request.form
    pw = request.form.get('password')
    hashed_password = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    print(hashed_password)
    user.write_user(form.get("email"),form.get("name"),hashed_password)
    return redirect("/")

@app.route('/login')
def login_form():
  return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    pw = request.form.get('password')
    curr_user = user.get_user("WHERE email=%s", [email])
    password_hash = curr_user["password_hash"]


    if curr_user and bcrypt.checkpw(pw.encode(),password_hash.encode()):
        session["user_id"] = curr_user["id"]
        session["user_name"] = curr_user["name"]
        return redirect('/')
    else:
        return render_template("login_error.html")
    
@app.route('/contactus')
def contactus():
    return render_template("contactus.html")

@app.route('/api/contactus', methods=['POST'])
def clientInfo():
    email = request.form.get('email')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    start = request.form.get('start')
    end = request.form.get('end')
    partysize = request.form.get('partysize')
    budget = request.form.get('budget')
    today= date.today()

    user.write_requires(email,name,phone_number,start,end,partysize,budget,today)
    return render_template("Enquiry.html")

@app.route('/requires')
def requires_list():
    return render_template("Enquiry.html", requires_items=user.get_all_requires())


@app.route("/logout")
def logout():
  session["user_id"] = None
  session["user_name"] = None
  return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
