import psycopg2

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        dbname="fruitdatabase",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Execute a test query
    cursor.execute("SELECT * FROM fruits")

    # Fetch and print the result of the query
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except Exception as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")