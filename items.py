import db

#Insert the dataset to database
def add_item(title, description, year, user_id):

    sql = "INSERT INTO datasets (title, description, year, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, year, user_id])

#Search information from the datasets table
def get_items():
    sql = "SELECT id, title FROM datasets ORDER by id DESC"
    return db.query(sql)


#Search information for the dataset description page
def get_item(item_id):
    sql = """SELECT datasets.id,
                    datasets.title, 
                    datasets.description,
                    datasets.year,
                    users.username
            FROM datasets, users
            WHERE datasets.user_id = users.id AND
                datasets.id = ?"""
    return db.query(sql, [item_id])[0]