import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import items
import users
import re

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

#Home page
@app.route("/")
def index():
    all_datasets = items.get_items()
    return render_template("index.html", items=all_datasets)

#User page
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    count = len(items)
    return render_template("show_user.html", user=user, items=items, count=count)

#Show the page where you can search datasets
@app.route("/find_dataset")
def find_dataset():
    query = request.args.get("query")
    if query:
        results = items.find_datasets(query)
    else:
        query = ""
        results = []
    return render_template("find_dataset.html", query=query, results=results)

#Show dataset description page
@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    feedback = items.get_feedback(item_id)
    return render_template("show_item.html", item=item, classes=classes, feedback=feedback)
    

#Add new dataset
@app.route("/new_dataset")
def new_dataset():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_dataset.html", classes = classes)


#Add dataset to database
@app.route("/create_dataset", methods=["POST"])
def create_dataset():
    require_login()
    title = request.form["title"].strip()
    if not title or len(title) > 80:
        abort(403) 
    description = request.form["description"]
    if not description or len(description) > 2000:
        abort(403)
    year = request.form["year"].strip()
    if not re.search(r"^\d{4}$", year):
        error = "Year must be a four-digit number."
        return render_template("new_dataset.html", 
                               error=error, 
                               title=title, 
                               description=description)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    
    items.add_item(title, description, year, user_id, classes)
    
    return redirect("/")

#Add feedback message
@app.route("/create_feedback", methods=["POST"])
def create_feedback():
    require_login()
 
    feedback = request.form["feedback"]
    if not feedback or len(feedback) > 1000:
        abort(403)

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    user_id = session["user_id"]
    
    items.add_feedback(item_id, user_id, feedback)
    
    return redirect("/item/" + str(item_id))

#Edit dataset
@app.route("/edit_dataset/<int:item_id>")
def edit_dataset(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)   
    if item["user_id"] != session["user_id"]:
        abort(403)

    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_dataset.html", item=item, classes=classes, all_classes=all_classes)

#Add edited dataset to database
@app.route("/update_dataset", methods=["POST"])
def update_dataset():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)  
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)  

    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403) 
    description = request.form["description"]
    if not description or len(description) > 2000:
        abort(403)
    year = request.form["year"]
    if not re.search(r"^\d{4}$", year):
        error = "Year must be a four-digit number."
        return render_template("new_dataset.html", 
                               error=error, 
                               title=title, 
                               description=description)
    
    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.update_item(item_id, title, description, year, classes)
    
    return redirect("/item/" + str(item_id))

#delete dataset
@app.route("/delete_dataset/<int:item_id>", methods=["GET", "POST"])
def delete_dataset(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
   
    if request.method == "GET":
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
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "ERROR: Username already taken"
    
    return redirect("/registered")

#Registration completed page
@app.route("/registered")
def registered():
    return render_template("registered.html")

#Signing up
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: Incorrect username or password"

#Log out from the app
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")