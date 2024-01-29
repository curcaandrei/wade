from flask import Flask,request
import sys
sys.path.append('src')
import dockerdb
from mysql.connector import Error
app = Flask(__name__)



@app.route('/')
def hello():
    return "user-profile-service hello"


@app.route('/users', methods=['GET'])
def get_users():
    return dockerdb.get_users()

@app.route('/users', methods=['POST'])
def add_user():
    data=request.get_json()
    return dockerdb.add_user(data)

@app.route('/users/<resource>', methods=['GET'])
def get_users_resources(resource):
    return dockerdb.get_users_resources(resource)

@app.route('/users/check-user', methods=['POST'])
def check_user():
    data = request.json
    return dockerdb.check_user(data)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return dockerdb.get_user(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
