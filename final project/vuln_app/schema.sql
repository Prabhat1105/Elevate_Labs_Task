
CREATE DATABASE IF NOT EXISTS sqli_playground;
USE sqli_playground;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  password VARCHAR(255)
);
INSERT INTO users (username, password) VALUES ('alice','alicepass');
INSERT INTO users (username, password) VALUES ('bob','bobpass');

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  description TEXT,
  price DECIMAL(10, 2)
);
INSERT INTO products (name, description, price) VALUES
('Laptop','Powerful laptop',700.00),
('Mouse','Wireless mouse',20.00),
('Keyboard','Mechanical keyboard',80.00),
('Monitor','24 inch monitor',150.00);