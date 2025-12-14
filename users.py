import db
from werkzeug.security import check_password_hash, generate_password_hash

#Search user information
def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id]) 
    return result[0] if result else None

#Search items added by user
def get_items(user_id, page, per_page):
    offset = (page - 1) * per_page
    sql = "SELECT id, title FROM datasets WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?"
    return db.query(sql, [user_id, per_page, offset])


#Create user account
def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

#Signing up
def check_login(username,password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
       return None
    
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

#Get count of datasets added by certain user
def get_item_count(user_id):
    sql = "SELECT COUNT(*) FROM datasets WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]
