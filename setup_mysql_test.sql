-- Create db if it is null
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Create user if is null
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grant usage
GRANT USAGE ON *.* TO 'hbnb_test'@'localhost';
-- Grant all privilages
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';
-- Grant select privilege on the database performance_schema.
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';
