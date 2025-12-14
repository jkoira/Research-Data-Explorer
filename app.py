import re
import secrets
import math
import sqlite3
import markupsafe
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import config
import items
import users




app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

#Home page
@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    per_page = 10
    item_count = items.get_item_count()
    page_count = math.ceil(item_count / per_page)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_datasets = items.get_items(page, per_page)
    return render_template("index.html", items=all_datasets, page=page, page_count=page_count)

#User page
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    page = request.args.get("page", 1, type=int)
    per_page = 10

    item_count = users.get_item_count(user_id)
    page_count = math.ceil(item_count / per_page)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/user/{user_id}?page=1")
    if page > page_count:
        return redirect(f"/user/{user_id}?page={page_count}")

    items_page = users.get_items(user_id, page, per_page)

    return render_template(
        "show_user.html",
        user=user,
        items=items_page,
        page=page,
        page_count=page_count,
        count=item_count
    )


#Show the page where you can search datasets
@app.route("/find_dataset")
def find_dataset():
    query = request.args.get("query")
    data_type = request.args.get("data_type")
    scientific_field = request.args.get("scientific_field")

    page = request.args.get("page", 1, type=int)
    per_page = 10

    all_classes = items.get_all_classes()

    if not (query or data_type or scientific_field):
        return render_template(
            "find_dataset.html",
            classes=all_classes,
            page=1,
            page_count=0,
            count=0
        )

    item_count = items.find_datasets_count(
        query or None,
        data_type or None,
        scientific_field or None
    )

    page_count = math.ceil(item_count / per_page)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/find_dataset?query={query}&data_type={data_type}&scientific_field={scientific_field}&page=1")
    if page > page_count:
        return redirect(
            f"/find_dataset?query={query}&data_type={data_type}&scientific_field={scientific_field}&page={page_count}"
        )

    results = items.find_datasets(
        query or None,
        data_type or None,
        scientific_field or None,
        page,
        per_page
    )

    return render_template(
        "find_dataset.html",
        query=query,
        data_type=data_type,
        scientific_field=scientific_field,
        classes=all_classes,
        results=results,
        page=page,
        page_count=page_count,
        count=item_count
    )

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
    check_csrf()

    title = request.form["title"].strip()
    if not title or len(title) > 100:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 2100:
        abort(403)
    year = request.form["year"].strip()
    if not re.search(r"^\d{4}$", year):
        error = "Year must be a four-digit number."
        all_classes = items.get_all_classes()
        return render_template("new_dataset.html",
                               error=error,
                               title=title,
                               description=description,
                               classes=all_classes)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    seen_titles = set()

    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
            seen_titles.add(class_title)

    required_titles = {"Scientific field", "Data type"}
    missing = required_titles - seen_titles

    if missing:
        return render_template("new_dataset.html",
                               title=title,
                               description=description,
                               year=year,
                               classes=all_classes
                               )

    item_id = items.add_item(title, description, year, user_id, classes)

    return redirect("/item/" + str(item_id))

#Add feedback message
@app.route("/create_feedback", methods=["POST"])
def create_feedback():
    require_login()
    check_csrf()

    feedback = request.form["feedback"]
    if not feedback or len(feedback) > 600:
        abort(403)

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    user_id = session["user_id"]

    items.add_feedback(item_id, user_id, feedback)

    return redirect("/item/" + str(item_id))

#Delete feedback message
@app.route("/delete_feedback/<int:feedback_id>", methods=["GET", "POST"])
def delete_feedback(feedback_id):
    require_login()

    feedback = items.get_feedback_by_id(feedback_id)
    if not feedback:
        abort(404)
    if feedback["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        item = items.get_item(feedback["item_id"])
        return render_template("delete_feedback.html", feedback=feedback, item=item)

    if request.method == "POST":
        check_csrf()
        if "delete" in request.form:
            items.delete_feedback(feedback_id)
        return redirect(f"/item/{feedback['item_id']}")



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
    check_csrf()

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
        return render_template("edit_dataset.html",
                               error=error,
                               title=title,
                               description=description)

    all_classes = items.get_all_classes()

    classes = []
    seen_titles = set()
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
            seen_titles.add(class_title)
    required_titles = {"Scientific field", "Data type"}

    missing = required_titles - seen_titles
    if missing:
        return render_template("edit_dataset.html",
                               title=title,
                               description=description,
                               year=year,
                               all_classes=all_classes)

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
        check_csrf()
        if "delete" in request.form:
            items.delete_dataset(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


#Create account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    error = None
    filled = {"username": username}

    if not username.strip():
        error = "Username cannot be empty"

    if len(username) > 16:
        error = "Username must be at most 16 characters long"

    if not password1:
        error = "ERROR: Password cannot be empty"

    if re.search(r"\s", password1):
        error = "ERROR: Password cannot contain spaces"

    if password1 != password2:
        error = "ERROR: Passwords do not match"

    if error:
        flash(error)
        return render_template("register.html", filled=filled)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: Username already taken")
        return redirect("/register")

    flash("Success! Your account has been created.")
    return redirect("/login")


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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: Incorrect username or password")
            return redirect("/login")

#Log out from the app
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")

#Line breaks in user input
@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)
