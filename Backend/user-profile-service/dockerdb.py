import mysql.connector
from mysql.connector import Error
from flask import jsonify
config = {
    'user': 'user',
    'password': 'user',
    'host': '35.198.178.41',
    'port': '3306',
    'database': 'users'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def get_users():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users_data limit 10")
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(users), 200
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching users:", e)
        return "Error fetching users", 500

def get_users_resources(resource,limit):
    limit = int(limit) if limit and limit.isdigit() else None
    try:
        connection = get_db_connection()
        if connection:
            query=get_resource(resource,limit)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(result), 200
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching users:", e)
        return "Error fetching users", 500

def get_resource(resourceName:str,limit:int):
    resources_dic={'skills':f"SELECT * FROM skills LIMIT {limit}",
               'cities':f"SELECT * FROM cities LIMIT {limit}",
               'companies':f"SELECT * FROM companies LIMIT {limit}"
               }
    return resources_dic[resourceName]

def get_user(user_id):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users_data WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                return jsonify(user), 200
            else:
                return "User not found", 404
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching user:", e)
        return "Error fetching user", 500

def add_user(data):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            user_id=data.get('id')
            user_name = data.get('name')
            email = data.get('email')
            locale = data.get('locale')
            city = data.get('city')
            company = data.get('company')
            is_known = True
            print(user_id)
            # Inserting data into the database
            cursor.execute("INSERT INTO users_data (user_id,user_name, email, locale, city, company, isKnown) VALUES (%s,%s, %s, %s, %s, %s, %s)",
                           (user_id,user_name, email, locale, city, company, is_known))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "User added successfully"}), 201
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error adding user:", e)
        return "Error adding user", 500

#Function used for pass or show firstTimecreen for user
def check_user(data):
    try:
        connection = get_db_connection()
        if connection:
            user_id=data.get('id')
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT isKnown FROM users_data WHERE user_id = %s ", (user_id,))
            user = cursor.fetchone()

            if user:
                is_known = user['isKnown']
                cursor.close()
                connection.close()
                return jsonify({"isKnown": is_known}), 200
            else:
                add_user(data)
                return jsonify({"isKnown": 0}), 200
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error processing request:", e)
        return "Error processing request", 500

def update_user(user_id,data):
    try:
        connection = get_db_connection()
        if connection:
            user_dict=set_user_data(data,user_id)
            cursor = connection.cursor(dictionary=True)
            cursor.execute("UPDATE users_data SET email=%s, city=%s, company=%s WHERE user_id = %s ; ",
                           (user_dict['email'],user_dict['city'],user_dict['company'],user_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'User information updated successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Error as e:
        print("Error processing request:", e)
        return "Error processing request", 500

def get_filtered_users(city,company,skill):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users_data where city=%s limit 10;",(city,))
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(users), 200
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching users:", e)
        return "Error fetching users", 500

def set_user_data(data,user_id):
    email = data.get('email')
    city = data.get('city')
    company = data.get('company')
    user_dict,status_code = get_user(user_id)
    user_dict=user_dict.json
    if len(user_dict) != 0:
        if email:
            user_dict['email'] = email
        if city:
            user_dict['city'] = city
        if company:
            user_dict['company'] = company
    return user_dict

def get_books(starting_id,number_of_books):
    try:
        starting_id=int(starting_id)
        number_of_books=int(number_of_books)
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = f"""
            SELECT books.book_id, books.title, books.average_rating, books.image_url, GROUP_CONCAT(authors.name SEPARATOR ', ') AS authors
            FROM books
            LEFT JOIN book_author ON books.book_id = book_author.book_id
            LEFT JOIN authors ON book_author.author_id = authors.author_id
            WHERE books.book_id>= {starting_id}
            GROUP BY books.book_id limit {number_of_books}
            """

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all rows from the result set
        books_with_authors = []
        for row in cursor.fetchall():
            book = {
                'book_id': row[0],
                'title': row[1],
                'rating': row[2],
                'image_url': row[3],
                'authors': row[4].split(', ') if row[4] else []
            }
            books_with_authors.append(book)

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the list of books with authors as JSON response
        return jsonify(books_with_authors)

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)})


def save_api_data(table_name, user_id, data):
    """
    Saves or updates the API data in the specified table in the database.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = (
            f"INSERT INTO {table_name} (user_id, data) "
            "VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE data = VALUES(data)"
        )
        cursor.execute(query, (user_id, data))
        connection.commit()
        print(f"Data for user_id {user_id} saved/updated in {table_name} successfully.")
    except Error as e:
        print(f"Error saving/updating data in {table_name}:", e)
    finally:
        if cursor:
            cursor.close()

def get_apidata_for_user_from_table(user_id, table_name):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM %s WHERE user_id = %s", (table_name,user_id))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            if data:
                return jsonify(data), 200
            else:
                return "User id not found", 404
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching spotify table:", e)
        return "Error fetching spotify table", 500

def get_mapper_id_of_user(user_id):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users_mapping_ids WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                return jsonify(user), 200
            else:
                return "User not found", 404
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching user mapping id:", e)
        return "Error fetching user mappinig id", 500