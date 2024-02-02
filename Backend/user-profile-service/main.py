from flask import Flask,request
import sys
sys.path.append('src')
import dockerdb
from src.populatedb import populate
app = Flask(__name__)



@app.route('/')
def hello():
    return "user-profile-service hello"

@app.route('/data' , methods=['POST'])
def populatedb():
   return populate()

@app.route('/users', methods=['GET'])
def get_users():
    return dockerdb.get_users()

@app.route('/users-filter', methods=['GET'])
def get_filtered_users():
    city = request.args.get('city')
    company = request.args.get('company')
    skill= request.args.get('skill')
    return dockerdb.get_filtered_users(city,company,skill)

@app.route('/users', methods=['POST'])
def add_user():
    data=request.get_json()
    return dockerdb.add_user(data)
"""
Retrieve cities, companies, skilss using this method
"""
@app.route('/users/resources/<resource>', methods=['GET'])
def get_users_resources(resource):
    limit = request.args.get('limit')
    return dockerdb.get_users_resources(resource,limit)

@app.route('/users/check-user', methods=['POST'])
def check_user():
    data = request.json
    return dockerdb.check_user(data)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    return dockerdb.get_user(user_id)
@app.route('/users/<string:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.json
    return dockerdb.update_user(user_id,data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
