import json

# Load data from JSON file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Open SQL file for writing
with open('data.sql', 'w') as sql_file:
    # Write SQL commands to create the table
    sql_file.write('CREATE TABLE Fruits (\n')
    sql_file.write('    id SERIAL PRIMARY KEY,\n')
    sql_file.write('    name VARCHAR(50) NOT NULL,\n')
    sql_file.write('    origin VARCHAR(50) NOT NULL,\n')
    sql_file.write('    season VARCHAR(50) NOT NULL\n')
    sql_file.write(');\n\n')

    # Write SQL commands to insert data
    for entry in data:
        sql_file.write(f"INSERT INTO Fruits (name, origin, season) VALUES ('{entry['name']}', '{entry['origin']}', '{entry['season']}');\n")

print("Data has been exported to data.sql")



