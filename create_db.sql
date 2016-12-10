CREATE DATABASE receiptify;
CREATE USER 'receiptify'@'localhost' IDENTIFIED BY 'GZuzJh842yVXwwhB';
USE receiptify;
GRANT ALL ON receiptify.* TO 'receiptify'@'localhost';
CREATE TABLE receipts_unprocessed(id INT PRIMARY KEY AUTO_INCREMENT, filename VARCHAR(255) NOT NULL, data TEXT NOT NULL);

