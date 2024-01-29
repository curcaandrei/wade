import mysql.connector
from mysql.connector import Error
from flask import jsonify
config = {
        'user': 'root',
        'password': 'secret',
        'host':'localhost',
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
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(users), 200
        else:
            return "Database connection error", 500
    except Error as e:
        print("Error fetching users:", e)
        return "Error fetching users", 500

def get_users_resources(resource):
    try:
        connection = get_db_connection()
        if connection:
            query=get_resource(resource)
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

def get_resource(resourceName:str):
    resources_dic={'skills':"SELECT * FROM skills",
               'cities':"SELECT * FROM cities",
               'companies':"SELECT * FROM companies"
               }
    return resources_dic[resourceName]

def get_user(user_id):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
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
            data = data
            print(data)
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