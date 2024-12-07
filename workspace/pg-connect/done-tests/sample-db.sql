-- Create the database
CREATE DATABASE FruitDatabase;

-- Connect to the database
-- FruitDatabase;

-- Create the table for fruits
CREATE TABLE Fruits (
    id SERIAL PRIMARY KEY,
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