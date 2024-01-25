import pymysql
from google.cloud.sql.connector import Connector
import sqlalchemy

# Configure your database connection here
username = 'root'
password = 'tZch0?6sG4Cr7>8='
database_name = 'wadedatabase'
instance_connection_name = 'diesel-nova-412314:europe-west3:wadeuserprofile'  # usually in the format: project:region:instance

connector = Connector()

def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        instance_connection_name,
        "pymysql",
        user=username,
        password=password,
        db=database_name
    )
    return conn

# Create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Create table (if it doesn't exist)
create_table_stmt = sqlalchemy.text("""
    CREATE TABLE IF NOT EXISTS my_table (
        id VARCHAR(50),
        title VARCHAR(255),
        PRIMARY KEY (id)
    )
""")

with pool.connect() as db_conn:
    db_conn.execute(create_table_stmt)

    # Insert into database
    insert_stmt = sqlalchemy.text(
        "INSERT INTO my_table (id, title) VALUES (:id, :title)"
    )
    db_conn.execute(insert_stmt, parameters={"id": "book1", "title": "Book One"})

    # Query database
    result = db_conn.execute(sqlalchemy.text("SELECT * FROM my_table")).fetchall()
    db_conn.commit()

    # Do something with the results
    for row in result:
        print(row)

connector.close()
