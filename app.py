import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import items

app = Flask(__name__)
app.secret_key = config.secret_key

#Home page
@app.route("/")
def index():
    all_datasets = items.get_items()
    return render_template("index.html", items=all_datasets)

#Show dataset description page
@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    return render_template("show_item.html", item=item)
    

#Add new dataset
@app.route("/new_dataset")
def new_dataset():
    return render_template("new_dataset.html")


#Add dataset to database
@app.route("/create_dataset", methods=["POST"])
def create_dataset():
    title = request.form["title"]
    description = request.form["description"]
    year = request.form["year"]
    user_id = session["user_id"]

    items.add_item(title, description, year, user_id)
    
    return redirect("/")

#Edit dataset
@app.route("/edit_dataset/<int:item_id>")
def edit_dataset(item_id):
    item = items.get_item(item_id)
    return render_template("edit_dataset.html", item=item)

#Add edited dataset to database
@app.route("/update_dataset", methods=["POST"])
def update_dataset():
    item_id = request.form["item_id"]
    title = request.form["title"]
    description = request.form["description"]
    year = request.form["year"]

    items.update_item(item_id, title, description, year)
    
    return redirect("/item/" + str(item_id))

#delete dataset
@app.route("/delete_dataset/<int:item_id>", methods=["GET", "POST"])
def delete_dataset(item_id):
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("delete_dataset.html", item=item)
    if request.method == "POST":
        if "delete" in request.form:
            items.delete_dataset(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


#Create account
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: Passwords do not match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: Username already taken"

    return "Your account has been created"

#Signing up
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: Incorrect username or password"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)