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
                    users.username,
                    users.id user_id
            FROM datasets, users
            WHERE datasets.user_id = users.id AND
                datasets.id = ?"""
    return db.query(sql, [item_id])[0]

#Update dataset information in database
def update_item(item_id, title, description, year):
    sql = """UPDATE datasets SET title = ?,
                                 description = ?,
                                 year = ?
                             WHERE id = ?"""
    db.execute(sql, [title, description, year, item_id])


#Delete dataset information from database
def delete_dataset(item_id):
    sql = "DELETE FROM datasets WHERE id = ?"
    db.execute(sql, [item_id])