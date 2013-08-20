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
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Růže',14,8,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Tulipan',5,8,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Keř',10,8,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Kytka',145,4,4,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Orchidej',4,45,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Marcipán',54,4,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Kořen',15,5,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Štěrk',0,5,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Tráva',5,4,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Hnojivo',10,5,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Cement',10,5,2,0,0);
INSERT INTO items (title, count, selling_price, buying_price, category_id, rank) VALUES('Vápno',10,5,2,1,0);
INSERT INTO categories (title, category_id, rank) VALUES('Stromy',0,0);
INSERT INTO categories (title, category_id, rank) VALUES('Keře',0,0);
INSERT INTO categories (title, category_id, rank) VALUES('Jehlicnate',1,0);
