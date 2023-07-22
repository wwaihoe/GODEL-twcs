DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS chat;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);

CREATE TABLE chat (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  chatbot TEXT NOT NULL, 
  chat_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  query TEXT NOT NULL,
  response TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);