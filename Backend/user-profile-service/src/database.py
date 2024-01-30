import pymysql
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector
import sqlalchemy

def access_secret_version(project_id, secret_id, version_id="latest"):
    secret_client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

PROJECT_ID = "diesel-nova-412314"
username = access_secret_version(PROJECT_ID, "DB_USERNAME")
password = access_secret_version(PROJECT_ID, "DB_PASSWORD")
database_name = 'wadedatabase'
instance_connection_name = 'diesel-nova-412314:europe-west3:wadeuserprofile'

connector = Connector()

def getconn() -> pymysql.connections.Connection:
    return connector.connect(
        instance_connection_name,
        "pymysql",
        user=username,
        password=password,
        db=database_name
    )

# Create connection pool
pool = sqlalchemy.create_engine("mysql+pymysql://", creator=getconn)

def save_api_data(table_name, user_id, data):
    """
    Saves or updates the API data in the specified table in the database.
    """
    query = sqlalchemy.text(
        f"""
        INSERT INTO {table_name} (id, data)
        VALUES (:id, :data)
        ON DUPLICATE KEY UPDATE
        data = VALUES(data)
        """
    )
    with pool.connect() as conn:
        conn.execute(query, {"id": user_id, "data": data})
