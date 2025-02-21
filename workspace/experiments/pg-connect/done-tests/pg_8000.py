import pg8000

# Connect to PostgreSQL
conn = pg8000.connect(
    database="testing",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

# Create a cursor object
cur = conn.cursor()

# Execute a query
cur.execute("CREATE TABLE testing_table (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL);")

cur.execute("INSERT INTO testing_table (name) VALUES ('testing')")

cur.execute("SELECT * FROM testing_table")

# Fetch and print the results
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()