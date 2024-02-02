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
               'companies':"SELECT * FROM companies LIMIT {limit}"
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