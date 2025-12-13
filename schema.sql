CREATE TABLE datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    year INTEGER,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    value TEXT

);

CREATE TABLE data_classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER REFERENCES datasets(id) ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime("now"))
);



  
