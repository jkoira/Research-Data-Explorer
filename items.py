import db

def add_item(title, description, year, user_id):

    sql = "INSERT INTO datasets (title, description, year, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, year, user_id])