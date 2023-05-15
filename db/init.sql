USE db;
CREATE TABLE products(product_id VARCHAR(36) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));
CREATE TABLE offers(offer_id VARCHAR(36) PRIMARY KEY, product_id VARCHAR(36), price INT, items_in_stock INT, FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE);
CREATE TABLE tokens(id INT PRIMARY KEY, token VARCHAR(255), expired TIMESTAMP);
