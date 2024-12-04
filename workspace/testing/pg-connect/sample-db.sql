-- Create the database
CREATE DATABASE FruitDatabase;

-- Use the database
USE FruitDatabase;

-- Create the table for fruits
CREATE TABLE Fruits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    origin VARCHAR(50) NOT NULL,
    season VARCHAR(50) NOT NULL
);

-- Insert some sample data
INSERT INTO Fruits (name, origin, season) VALUES
('Apple', 'USA', 'Fall'),
('Mango', 'India', 'Summer'),
('Orange', 'Spain', 'Winter'),
('Strawberry', 'France', 'Spring');