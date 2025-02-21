CREATE TABLE Fruits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    origin VARCHAR(50) NOT NULL,
    season VARCHAR(50) NOT NULL
);

INSERT INTO Fruits (name, origin, season) VALUES ('Apple', 'USA', 'Fall');
INSERT INTO Fruits (name, origin, season) VALUES ('Mango', 'India', 'Summer');
INSERT INTO Fruits (name, origin, season) VALUES ('Orange', 'Spain', 'Winter');
INSERT INTO Fruits (name, origin, season) VALUES ('Strawberry', 'France', 'Spring');