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
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_data_classes_item_id ON data_classes(item_id);

CREATE INDEX idx_data_classes_item_title ON data_classes(item_id, title);

CREATE INDEX idx_data_classes_title_value_item ON data_classes(title, value, item_id);

CREATE INDEX idx_datasets_user_id ON datasets(user_id);

CREATE INDEX idx_feedback_item_id ON feedback(item_id);




  
