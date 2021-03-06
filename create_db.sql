CREATE DATABASE receiptify;
CREATE USER 'receiptify'@'localhost' IDENTIFIED BY 'GZuzJh842yVXwwhB';
USE receiptify;
GRANT ALL ON receiptify.* TO 'receiptify'@'localhost';
CREATE TABLE receipts(id INT PRIMARY KEY AUTO_INCREMENT, filename VARCHAR(255) NOT NULL, data TEXT NOT NULL);
CREATE TABLE items_defs(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL);
CREATE TABLE items(id INT PRIMARY KEY AUTO_INCREMENT, item_id INT NOT NULL, amount FLOAT NOT NULL, date DATETIME);
