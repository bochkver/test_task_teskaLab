CREATE DATABASE containers_db;
USE containers_db;
CREATE TABLE containers_info (container_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), created_at BIGINT, status VARCHAR(255), cpu INT, memory_usage INT );
CREATE TABLE containers_addresses (id INT AUTO_INCREMENT PRIMARY KEY, container_id INT, address VARCHAR(255)); 
