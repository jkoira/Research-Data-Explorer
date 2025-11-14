CREATE TABLE collection_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE data_formats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE scientific_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    data_formats_id INTEGER,
    collection_method_id INTEGER,
    scientific_field_id INTEGER,
    year INTEGER,
    user_id INTEGER,
    request TEXT,
    FOREIGN KEY (data_formats_id) REFERENCES data_formats(id),
    FOREIGN KEY (collection_method_id) REFERENCES collection_methods(id),
    FOREIGN KEY (scientific_field_id) REFERENCES scientific_fields(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
  
