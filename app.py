from flask import Flask, render_template , request ,redirect,session
from models import tour, user
import os
import bcrypt




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

#TODO homepage
@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/grouptour')
def grouptour():
    return render_template('grouptour.html',tour_items=tour.get_all_tour())

@app.route('/add')
def add_tour():
    if session.get("user_id",""):
        return render_template("add.html")
    else:
        return redirect("/login")

@app.route('/api/add', methods=["POST"])
def add_tour_docu():
    form = request.form

    tour.insert_tour(form.get("item_name"),form.get("item_price"))
    return redirect("/")

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
    return redirect("/")

@app.route('/delete/<id>')
def delete_tour_form(id):
  if session.get("user_id", ""):
    return render_template("delete.html", tour_item=tour.get_tour(id))
  else:
    return redirect("/login")

@app.route('/api/delete/<id>')
def delete_tour_docu():
    tour.delete_tour(request.form.get("id"))

    return redirect("/")

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
    return render_template('contactus.html')

@app.route('/contactus', methods=['POST'])
def clientInfo():
    email = request.form.get('email')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    direction = request.form.get('direction')
    days = request.form.get('days')

    user.write_requires(email,name,phone_number,direction,days)
    return "Thank you for your information"
@app.route("/logout")
def logout():
  session["user_id"] = None
  session["user_name"] = None
  return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
