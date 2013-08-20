DROP TABLE IF EXISTS items;
CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL UNIQUE,
  selling_price REAL,
  buying_price REAL,
  count INTEGER,
  category_id INTEGER,
  rank INTEGER);

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL UNIQUE,
  category_id INTEGER,
  rank INTEGER
  );

DROP TABLE IF EXISTS temp_items;
CREATE TABLE temp_items (
  selling_price REAL,
  count INTEGER default 0,
  item_id INTEGER
  );

DROP TABLE IF EXISTS carts;
CREATE TABLE carts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  datetime TEXT NOT NULL
  );

DROP TABLE IF EXISTS cart_items;
CREATE TABLE cart_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  selling_price REAL,
  buying_price REAL,
  count INTEGER,
  cart_id INTEGER
  );
