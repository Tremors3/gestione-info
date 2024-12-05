import pg8000.native

# Connect to the database with user name postgres

con = pg8000.native.Connection("postgres", password="cpsnow")

# Create a temporary table

con.run("CREATE TEMPORARY TABLE book (id SERIAL, title TEXT)")

# Populate the table

for title in ("Ender's Game", "The Magus"):
    con.run("INSERT INTO book (title) VALUES (:title)", title=title)

# Print all the rows in the table

for row in con.run("SELECT * FROM book"):
    print(row)

con.close()