from flask import Flask, render_template , request ,redirect,session,flash,url_for
import urllib.request
from werkzeug.utils import secure_filename
from models import tour, user
import os
import bcrypt
import psycopg2
import psycopg2.extras
from datetime import date 




app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY','default_secret_key')
conn = psycopg2.connect(dbname=os.getenv("DB_NAME"),user=os.getenv("USER"),password=os.getenv("PASSWORD"),host=os.getenv("HOST"),port=os.getenv("DB_PORT"))
#conn = psycopg2.connect(dbname="travel")
#Set 'static/uploads/' as my upload folder
UPLOAD_FOLDER = 'static/uploads/'
#sets the configuration property of the Flask application to use the UPLOAD_FOLDER as the destination directory for uploaded files.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#limits the maximum size of a file that can be uploaded to 16 megabytes.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#set specifies the file extensions that are allowed to be uploaded. Only files with extensions in this set will be allowed to be uploaded. In this case, the allowed extensions are 'png', 'jpg', 'jpeg', and 'gif'.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#The allowed_file function is a helper function that checks if a given filename has an allowed extension. It returns True if the filename has an extension that is in the ALLOWED_EXTENSIONS set and False otherwise.
def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
# @app.route('/api/add', methods=["POST"])
# def add_tour_docu():
#     form = request.form
#     # use tour from model to insert data into database 
#     tour.insert_tour(form.get("item_name"),form.get("item_price"))
#     return redirect("/")

#Use post method to get the data and upload the images from add page
@app.route('/upload', methods=['POST'])
def upload_image():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    name = request.form.get("item_name")
    price = request.form.get("item_price")
    print(name)
    print(price)
# First, it checks if the request contains a file in the 'file' field. If not, it redirects the user to the same URL and displays a flash message saying 'No file part'.
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
#it gets the file from the request using request.files['file']. If the filename is an empty string, it redirects the user to the same URL and displays a flash message saying 'No image selected for uploading'.
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
#t checks if the file has an allowed extension using the allowed_file function. If the file has an allowed extension, it generates a secure filename using secure_filename(file.filename.strip()) to avoid any malicious filenames and saves the file to the upload folder using file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)).
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename.strip())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
 
        cursor.execute("INSERT INTO tour(name,price,filename) VALUES (%s,%s,%s)", [name,price,filename])
        conn.commit()
 
        flash('Image successfully uploaded and displayed below')
        return render_template('grouptour.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)   
    
#edit page and using session to check the user 
@app.route('/edit/<id>')
def edit_tour_form(id):
    if session.get("user_id", ""):
        return render_template("edit.html", tour_item=tour.get_tour(id))
    else:
        return redirect("/login")

#edit all the item from tour table by ID
@app.route('/api/edit/<id>', methods=["POST"])
def edit_tour_docu(id):
    form = request.form

    tour.update_tour(id,form.get("item_name"),form.get("item_price"))
    return redirect("/grouptour")

#delete tour item from tour table by ID
@app.route('/delete/<id>')
def delete_tour_form(id):
  if session.get("user_id", ""):
    return render_template("delete.html", tour_item=tour.get_tour(id))
  else:
    return redirect("/login")

#to delete data and go back grouptour page
@app.route('/api/delete',methods=["POST"])
def delete_tour_docu():
    tour.delete_tour(request.form.get("id"))

    return redirect('/grouptour')

#Sign up page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

#Sign up form to create a new user
@app.route("/signup", methods=['POST'])
def signup():
    form = request.form
    pw = request.form.get('password')
    hashed_password = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    print(hashed_password)
    user.write_user(form.get("email"),form.get("name"),hashed_password)
    return redirect("/")

#Login page
@app.route('/login')
def login_form():
  return render_template("login.html")

#A login page with hashed password and cookies for check the email and password
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

#Contact us page for the form of customer demands    
@app.route('/contactus')
def contactus():
    return render_template("contactus.html")

#For get all the demands by click the submit link and save the data into table
@app.route('/api/contactus', methods=['POST'])
def clientInfo():
    email = request.form.get('email')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    start = request.form.get('start')
    end = request.form.get('end')
    partysize = request.form.get('partysize')
    budget = request.form.get('budget')
    days = request.form.get('days')
    today= date.today()

    user.write_requires(email,name,phone_number,start,end,partysize,budget,days,today)
    return redirect('/requires')

#Enquiry page that shows all the customer demands
@app.route('/requires')
def requires_list():
    return render_template("Enquiry.html", requires_items=user.get_all_requires())

#Logout page click the link back to home page
@app.route("/logout")
def logout():
  session["user_id"] = None
  session["user_name"] = None
  return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
