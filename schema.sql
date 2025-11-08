CREATE TABLE collection_methods (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE data_formats (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE scientific_fields (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE datasets(
  id INT,
  title TEXT,
  description TEXT,
  data_formats_id INT,
  collection_method_id INT,
  scientific_field_id INT,
  year INT,
  user_id INT,
  request TEXT
);
CREATE TABLE IF NOT EXISTS "users" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password_hash TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
