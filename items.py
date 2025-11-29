import db

#Finds all classes
def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

#Insert the dataset to database
def add_item(title, description, year, user_id, classes):

    sql = "INSERT INTO datasets (title, description, year, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, year, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO data_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

#Search classes from database
def get_classes(item_id):
    sql = "SELECT title, value FROM data_classes WHERE item_id = ?"
    return db.query(sql, [item_id])


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
    result = db.query(sql, [item_id]) 
    return result[0] if result else None

#Update dataset information in database
def update_item(item_id, title, description, year, classes):
    sql = """UPDATE datasets SET title = ?,
                                 description = ?,
                                 year = ?
                             WHERE id = ?"""
    db.execute(sql, [title, description, year, item_id])

    sql = "DELETE FROM data_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO data_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])


#Delete dataset information from database
def delete_dataset(item_id):
    sql = "DELETE FROM datasets WHERE id = ?"
    db.execute(sql, [item_id])


#Search datasets from database
def find_datasets(query):
    sql = """SELECT id, title
             FROM datasets
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])