import db

#Finds all classes
def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes.setdefault(title, []).append(value)

    return classes      
    

#Insert the dataset to database
def add_item(title, description, year, user_id, classes):

    sql = "INSERT INTO datasets (title, description, year, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, year, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO data_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])
        
    return item_id

#Search classes from database
def get_classes(item_id):
    sql = "SELECT title, value FROM data_classes WHERE item_id = ?"
    return db.query(sql, [item_id])


#Search information from the datasets table
def get_items():
    sql = """SELECT datasets.id, 
                    datasets.title, 
                    datasets.year, 
                    sf.value AS scientific_field, 
                    dt.value AS data_type
             FROM datasets, data_classes dt, data_classes sf 
             WHERE dt.item_id = datasets.id
                AND dt.title = 'Data type'
                AND sf.item_id = datasets.id
                AND sf.title = 'Scientific field'
             ORDER BY datasets.id DESC"""
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
def find_datasets(query, data_type, scientific_field):
    params = []
    conditions = []
    sql = """SELECT DISTINCT datasets.id, 
                             datasets.title,
                             datasets.description,
                             datasets.year,
                             users.username,
                             users.id AS user_id
             FROM datasets
             JOIN users ON users.id = datasets.user_id
             LEFT JOIN data_classes dc1 ON dc1.item_id = datasets.id AND dc1.title = "Data type"
             LEFT JOIN data_classes dc2 ON dc2.item_id = datasets.id AND dc2.title = "Scientific field"
             """
    #search by words
    if query:
        like = "%" + query + "%"
        conditions.append("(datasets.title LIKE ? OR datasets.description LIKE ?)")
        params.extend([like, like])

    #Search by data type
    if data_type:
        conditions.append("dc1.value = ?")
        params.append(data_type)

    #Search by scientific field
    if scientific_field:
        conditions.append("dc2.value = ?")
        params.append(scientific_field)
    
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    
    sql += " ORDER BY datasets.id DESC"

    return db.query(sql, params)


#Add feedback message to the database
def add_feedback(item_id, user_id, message):
    sql = """INSERT INTO feedback (item_id, user_id, message)
             VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, user_id, message])

#Search feedback messages linked to the dataset
def get_feedback(item_id):
    sql = """SELECT feedback.id,
                    feedback.item_id,
                    feedback.message,
                    feedback.created_at,
                    users.id AS user_id,
                    users.username
             FROM feedback
             JOIN users ON feedback.user_id = users.id
             WHERE feedback.item_id = ?
             ORDER BY feedback.id DESC"""
    return db.query(sql, [item_id])

#Search certain feedback message by id
def get_feedback_by_id(feedback_id):
    sql = """SELECT feedback.id, 
                    feedback.item_id, 
                    feedback.user_id, 
                    feedback.message, 
                    feedback.created_at,
                    users.username
             FROM feedback 
             JOIN users ON users.id = feedback.user_id
             WHERE feedback.id = ?"""
    result = db.query(sql, [feedback_id])
    return result[0] if result else None

def delete_feedback(feedback_id):
    sql = "DELETE FROM feedback WHERE id = ?"
    db.execute(sql, [feedback_id])
     
