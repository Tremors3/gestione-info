import pg8000

# Connect to PostgreSQL
conn = pg8000.connect(
    database="FruitDatabase",
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port=5432
)

# Create a cursor object
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM fruitsdatabase")

# Fetch and print the results
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()