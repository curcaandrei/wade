from flask import Flask
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS, ALSModel
from flask import jsonify, request
from unzipper import unzip_model
from pyspark.sql.functions import col, explode
from pyspark.sql.types import StructType, StructField, LongType, DoubleType
from flask_cors import CORS
import requests
user_pf_url="http://127.0.0.1:5000/users/"
model=None
recommendations=None

app = Flask(__name__)
CORS(app)
sc = SparkSession.builder.appName("BookRecommender").getOrCreate()
schema = StructType([
    StructField("user_id_long", LongType(), nullable=True),
    StructField("book_id_long", LongType(), nullable=True),
    StructField("rating_double", DoubleType(), nullable=True)
])
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/predict/<user_id>',methods=['POST'])
def predict(user_id):
    user_id = int(user_id)
    response = requests.get(user_pf_url + f"interactions/{user_id}")
    if response.status_code == 404:
        response = requests.get(user_pf_url + f"/random-books")
        return response.json(), 200
    elif response.status_code == 200:
        data = get_recommendations(get_long_user_id(user_id))
        return jsonify(data), 200
    else:
        print(f"Unexpected status code: {response.status_code}")
    return jsonify("Something unexpected occurred"), 500

#we need this because algorithm is working with long ids not strings
def get_long_user_id(user_id):
    response = requests.get(user_pf_url + f"mapping/{user_id}")
    if response.status_code==200:
        data=response.json()
        user_id_long=int(data["user_id_long"])
        return user_id_long
    return 0

@app.route('/predict-new-user/<user_id>',methods=['POST'])
def predict_new_user(user_id):
    global recommendations
    global model
    user_id=int(user_id)
    json_data = request.json

    for item in json_data:
        item['user_id'] = user_id

    df = sc.createDataFrame(json_data, schema)
    model.transform(df)

    recommendations = model.recommendForAllUsers(5)
    data=get_recommendations(user_id)
    return jsonify(data)

def get_recommendations(user_id):
    global recommendations
    result=recommendations.where(recommendations.user_id_long==user_id)
    exploded_df = result.select(col("user_id_long"), explode("recommendations").alias("recommendation"))
    # Extract book_id and rating
    book_rating_df = exploded_df.select(
        col("recommendation.book_id_long").alias("book_id"),
        col("recommendation.rating").alias("rating")
    )
    collected_df = book_rating_df.collect()
    data_dicts = [row.asDict() for row in collected_df]
    return data_dicts

@app.route('/unzip-model',methods=['POST'])
def unzip():
    global model,recommendations
    response = unzip_model()
    model = ALSModel.load("static/als_model")
    recommendations = model.recommendForAllUsers(5)
    return response
@app.route('/load-model',methods=['POST'])
def load_model():
    global model,recommendations
    model = ALSModel.load("static/als_model")
    recommendations = model.recommendForAllUsers(5)
    return jsonify("Model loaded succesfully"),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
