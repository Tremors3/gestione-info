import pg8000

# Connect to PostgreSQL
conn = pg8000.connect(
    database="graboid_rfc",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

# Create a cursor object
cur = conn.cursor()

#! Ricordarsi di fare commit per appliccare le modifiche
cur.execute("CREATE TABLE testing_table (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL); COMMIT;")

cur.execute("INSERT INTO testing_table (name) VALUES ('testing'); COMMIT;")


# E' possibile scegliere quale tipo di index usare (default: B-tree): B-tree, Hash, GiST, SP-GiST, GIN, BRIN.  (https://www.postgresql.org/docs/current/indexes-types.html)
# cur.execute("CREATE INDEX <nome_index> ON <tabella> (<colonna>)")
# cur.execute("CREATE INDEX <nome_index_multicolonna> ON <tabella> (<colonna_primaria>, <colonna_secondaria>)")

cur.execute("SELECT * FROM testing_table")

# Fetch and print the results
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()


# printf 'CREATE DATABASE gestione_info WITH ENCODING="UTF8" OWNER=postgres;\n' | psql -U postgres
# docker exec -i db bash < create_database.sh