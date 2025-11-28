CREATE TABLE datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    year INTEGER,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE data_classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER REFERENCES datasets(id) ON DELETE CASCADE,
    title TEXT,
    value TEXT
);



  
